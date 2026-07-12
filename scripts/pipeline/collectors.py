#!/usr/bin/env python3
"""
Source collectors for project map data pipeline

Each collector is responsible for:
1. Reading a specific SSOT source (roadmap.yaml, ArchiMate data, Git metadata, etc.)
2. Extracting raw data in a source-specific format
3. Computing SHA-256 hash for provenance tracking
4. Returning structured data + metadata for normalization

Collectors are pure functions: no side effects, no normalization.
"""

import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class CollectorResult:
    """Result from a collector with provenance metadata"""
    def __init__(self, source_path: Path, data: Any, extracted_at: Optional[datetime] = None):
        self.source_path = source_path
        self.data = data
        self.extracted_at = extracted_at or datetime.utcnow()
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute SHA-256 hash of source file"""
        if not self.source_path.exists():
            return "0" * 64  # Placeholder for missing files

        with open(self.source_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def to_source_ref(self) -> Dict[str, str]:
        """Convert to source_refs entry for entities"""
        return {
            'path': str(self.source_path.relative_to(self.source_path.parents[2])),  # Relative to repo root
            'hash': self.hash,
            'extracted_at': self.extracted_at.isoformat() + 'Z'
        }

class RoadmapCollector:
    """Collects roadmap data from state/roadmap.yaml"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.roadmap_path = repo_root / 'state' / 'roadmap.yaml'

    def collect(self) -> CollectorResult:
        """
        Collect roadmap YAML data.

        Returns:
            CollectorResult with raw YAML data (milestones + tasks)
        """
        if not self.roadmap_path.exists():
            raise FileNotFoundError(f"Roadmap not found at {self.roadmap_path}")

        with open(self.roadmap_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return CollectorResult(
            source_path=self.roadmap_path,
            data=data
        )

class ArchimateCollector:
    """Collects ArchiMate data from docs/archimate_data.json"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.archimate_path = repo_root / 'docs' / 'archimate_data.json'

    def collect(self) -> CollectorResult:
        """
        Collect ArchiMate data (conceptual and physical entities).

        Returns:
            CollectorResult with ArchiMate nodes and relationships
        """
        if not self.archimate_path.exists():
            raise FileNotFoundError(f"ArchiMate data not found at {self.archimate_path}")

        with open(self.archimate_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return CollectorResult(
            source_path=self.archimate_path,
            data=data
        )

class TaskQueueCollector:
    """Collects task queue data from COMMUNICATION/TASK_QUEUE.md"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.task_queue_path = repo_root / 'COMMUNICATION' / 'TASK_QUEUE.md'

    def collect(self) -> CollectorResult:
        """
        Collect task queue markdown (for M1 task status cross-reference).

        Returns:
            CollectorResult with raw markdown text
        """
        if not self.task_queue_path.exists():
            raise FileNotFoundError(f"Task queue not found at {self.task_queue_path}")

        with open(self.task_queue_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return CollectorResult(
            source_path=self.task_queue_path,
            data={'content': content}
        )

class ProjectStateCollector:
    """Collects project state from state/project_state.md"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.state_path = repo_root / 'state' / 'project_state.md'

    def collect(self) -> CollectorResult:
        """
        Collect project state markdown (for health indicators).

        Returns:
            CollectorResult with raw markdown text
        """
        if not self.state_path.exists():
            # Project state is optional - may not exist yet
            return CollectorResult(
                source_path=self.state_path,
                data={'content': '', 'exists': False}
            )

        with open(self.state_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return CollectorResult(
            source_path=self.state_path,
            data={'content': content, 'exists': True}
        )

class EcosystemSnapshotCollector:
    """Collects sanitized ecosystem snapshot from artifacts/"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.snapshot_path = repo_root / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'ecosystem-snapshot.json'

    def collect(self) -> CollectorResult:
        """
        Collect ecosystem snapshot (agent collaboration state).

        Returns:
            CollectorResult with snapshot JSON
        """
        if not self.snapshot_path.exists():
            # Snapshot is optional - may not exist on first build
            return CollectorResult(
                source_path=self.snapshot_path,
                data={'agents': [], 'rules_summary': {}, 'exists': False}
            )

        with open(self.snapshot_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data['exists'] = True
        return CollectorResult(
            source_path=self.snapshot_path,
            data=data
        )

class GitMetadataCollector:
    """Collects Git metadata (commit hash, repo state) via git commands"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def collect(self) -> CollectorResult:
        """
        Collect Git metadata.

        Returns:
            CollectorResult with git commit hash and branch
        """
        import subprocess

        try:
            # Get current commit hash
            commit_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_root,
                text=True
            ).strip()

            # Get current branch
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.repo_root,
                text=True
            ).strip()

            # Get commit date
            commit_date = subprocess.check_output(
                ['git', 'log', '-1', '--format=%cI'],
                cwd=self.repo_root,
                text=True
            ).strip()

            data = {
                'commit_hash': commit_hash,
                'branch': branch,
                'commit_date': commit_date,
                'exists': True
            }

        except (subprocess.CalledProcessError, FileNotFoundError):
            # Not in a git repo or git not available
            data = {
                'commit_hash': 'unknown',
                'branch': 'unknown',
                'commit_date': datetime.utcnow().isoformat() + 'Z',
                'exists': False
            }

        # Use a pseudo-path for Git metadata
        pseudo_path = self.repo_root / '.git' / 'HEAD'
        return CollectorResult(
            source_path=pseudo_path,
            data=data
        )

class CollectorRegistry:
    """Registry of all available collectors"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.collectors = {
            'roadmap': RoadmapCollector(repo_root),
            'archimate': ArchimateCollector(repo_root),
            'task_queue': TaskQueueCollector(repo_root),
            'project_state': ProjectStateCollector(repo_root),
            'ecosystem_snapshot': EcosystemSnapshotCollector(repo_root),
            'git_metadata': GitMetadataCollector(repo_root)
        }

    def collect_all(self) -> Dict[str, CollectorResult]:
        """
        Run all collectors and return results keyed by collector name.

        Returns:
            Dict mapping collector name to CollectorResult
        """
        results = {}
        errors = []

        for name, collector in self.collectors.items():
            try:
                results[name] = collector.collect()
            except FileNotFoundError as e:
                errors.append(f"{name}: {e}")
                # Continue with other collectors
            except Exception as e:
                errors.append(f"{name}: Unexpected error: {e}")

        if errors:
            print(f"Collector warnings:")
            for err in errors:
                print(f"  - {err}")

        return results

    def collect_sources_manifest(self, results: Dict[str, CollectorResult]) -> List[Dict[str, str]]:
        """
        Generate sources manifest for build-manifest.json

        Args:
            results: Dict of CollectorResult from collect_all()

        Returns:
            List of source metadata dicts
        """
        manifest = []

        for name, result in results.items():
            manifest.append({
                'path': str(result.source_path.relative_to(self.repo_root)) if result.source_path.exists() else f"pseudo:{name}",
                'hash': result.hash,
                'read_at': result.extracted_at.isoformat() + 'Z',
                'status': 'ok' if result.data.get('exists', True) else 'missing'
            })

        return manifest
