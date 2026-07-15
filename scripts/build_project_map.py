#!/usr/bin/env python3
"""
Build Project Map — Main pipeline command

Orchestrates the complete data pipeline:
1. Collect: Read SSOT sources
2. Normalize: Convert to canonical entities/relations
3. Derive: Calculate health, freshness, critical path
4. Validate: Apply JSON Schema validation
5. Render: Generate JSON datasets
6. Publish: Atomic replacement of docs/data/generated/

Usage:
    python scripts/build_project_map.py [--dry-run] [--verbose]

Exit codes:
    0: Success
    1: Critical error (schema validation failed, missing required sources)
    2: Warning (stale sources, optional sources missing)
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple
import argparse

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.collectors import CollectorRegistry
from pipeline.normalizer import Normalizer
from pipeline.health_engine import HealthEngine, FreshnessPolicy

class BuildError(Exception):
    """Critical build error"""
    def __init__(self, code: str, message: str, phase: str, file: str = None):
        self.code = code
        self.message = message
        self.phase = phase
        self.file = file
        super().__init__(f"[{code}] {message}")

class BuildWarning:
    """Non-fatal build warning"""
    def __init__(self, code: str, message: str, file: str = None):
        self.code = code
        self.message = message
        self.file = file

class ProjectMapBuilder:
    """Main builder orchestrating all pipeline phases"""

    def __init__(self, repo_root: Path, dry_run: bool = False, verbose: bool = False):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.verbose = verbose
        self.errors: List[BuildError] = []
        self.warnings: List[BuildWarning] = []
        self.phase_durations: Dict[str, float] = {}
        self.start_time = datetime.now(timezone.utc)

    def log(self, message: str, level: str = "INFO"):
        """Log message with level"""
        prefix_map = {
            "INFO": "[·]",
            "WARN": "[!]",
            "ERROR": "[✗]",
            "OK": "[✓]"
        }
        prefix = prefix_map.get(level, "[·]")
        print(f"{prefix} {message}")

    def log_phase(self, phase: str):
        """Log phase header"""
        print(f"\n{'='*60}")
        print(f"PHASE: {phase}")
        print(f"{'='*60}")

    def time_phase(self, phase_name: str):
        """Context manager for timing phases"""
        class PhaseTimer:
            def __init__(self, builder, name):
                self.builder = builder
                self.name = name
                self.start = None

            def __enter__(self):
                self.start = datetime.now(timezone.utc)
                return self

            def __exit__(self, *args):
                duration = (datetime.now(timezone.utc) - self.start).total_seconds()
                self.builder.phase_durations[self.name] = duration
                if self.builder.verbose:
                    self.builder.log(f"Phase '{self.name}' completed in {duration:.2f}s", "INFO")

        return PhaseTimer(self, phase_name)

    def phase_collect(self) -> Dict[str, Any]:
        """Phase 1: Collect SSOT sources"""
        self.log_phase("1. COLLECT")

        with self.time_phase("collect"):
            registry = CollectorRegistry(self.repo_root)
            results = registry.collect_all()

            self.log(f"Collected {len(results)} sources", "OK")

            # Check for missing required sources
            required = ['roadmap']
            for req in required:
                if req not in results or not results[req].data.get('exists', True):
                    raise BuildError(
                        code="MAP-E004",
                        message=f"Required source '{req}' not found or unparsable",
                        phase="collect",
                        file=str(results[req].source_path) if req in results else "unknown"
                    )

            # Ecosystem snapshot: emit MAP-E003 specifically (collaborative system data)
            snap = results.get('ecosystem_snapshot')
            if snap and not snap.data.get('exists', True):
                self.warnings.append(BuildWarning(
                    code="MAP-E003",
                    message="Ecosystem snapshot absent — collaborative system data unavailable. Freshness badge will show STALE.",
                    file=str(snap.source_path)
                ))

            # Warn about other optional missing sources
            optional = ['archimate', 'project_state']
            for opt in optional:
                if opt in results and not results[opt].data.get('exists', True):
                    self.warnings.append(BuildWarning(
                        code="MAP-W001",
                        message=f"Optional source '{opt}' not found, using empty data",
                        file=str(results[opt].source_path)
                    ))

            # Check source freshness (MAP-E008)
            self._check_source_freshness(results)

            return results

    def _check_source_freshness(self, results: Dict[str, Any]):
        """Emit MAP-E008 if any source file exceeds its configured staleness threshold."""
        import os
        from datetime import datetime, timezone, timedelta

        policy_path = self.repo_root / 'config' / 'freshness_policy.yaml'
        if not policy_path.exists():
            return

        try:
            import yaml
            with open(policy_path, encoding='utf-8') as f:
                policy = yaml.safe_load(f) or {}
        except Exception:
            return

        thresholds = {
            'roadmap':            policy.get('roadmap_hours', 168),
            'project_state':      policy.get('project_state_hours', 168),
            'ecosystem_snapshot': policy.get('ecosystem_hours', 24),
            'archimate':          policy.get('archimate_hours', 720),
        }
        now = datetime.now(timezone.utc)

        for name, hours in thresholds.items():
            result = results.get(name)
            if result is None or not result.source_path.exists():
                continue
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(result.source_path), tz=timezone.utc)
                age_hours = (now - mtime).total_seconds() / 3600
                if age_hours > hours:
                    self.warnings.append(BuildWarning(
                        code="MAP-E008",
                        message=(
                            f"Source '{name}' is stale: last modified {age_hours:.0f}h ago "
                            f"(threshold: {hours}h). Dataset freshness badge will show STALE."
                        ),
                        file=str(result.source_path)
                    ))
            except OSError:
                pass

    def phase_normalize(self, collector_results: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Normalize to canonical model"""
        self.log_phase("2. NORMALIZE")

        with self.time_phase("normalize"):
            normalizer = Normalizer()
            entity_registry = normalizer.normalize_all(collector_results)

            self.log(f"Normalized {len(entity_registry.entities)} entities", "OK")
            self.log(f"Normalized {len(entity_registry.relations)} relations", "OK")

            return entity_registry.to_dict()

    def phase_derive(self, registry: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Derive health, freshness, critical path"""
        self.log_phase("3. DERIVE")

        with self.time_phase("derive"):
            policy_path = self.repo_root / 'config' / 'freshness_policy.yaml'
            policy = FreshnessPolicy.from_yaml(policy_path) if policy_path.exists() else FreshnessPolicy()

            health_engine = HealthEngine(freshness_policy=policy)
            enriched_registry = health_engine.enrich_registry(registry)

            # Count health statuses
            health_counts = {}
            for entity in enriched_registry['entities'].values():
                health = entity['raw_data'].get('health', 'UNKNOWN')
                health_counts[health] = health_counts.get(health, 0) + 1

            self.log(f"Health: HEALTHY={health_counts.get('HEALTHY', 0)}, BLOCKED={health_counts.get('BLOCKED', 0)}, AT_RISK={health_counts.get('AT_RISK', 0)}, UNKNOWN={health_counts.get('UNKNOWN', 0)}", "OK")

            # Warn if many UNKNOWN
            if health_counts.get('UNKNOWN', 0) > len(enriched_registry['entities']) * 0.5:
                self.warnings.append(BuildWarning(
                    code="MAP-W002",
                    message=f"{health_counts['UNKNOWN']} entities have UNKNOWN health (>50% of total)"
                ))

            return enriched_registry

    def phase_validate(self, registry: Dict[str, Any]):
        """Phase 4: Validate entity registry"""
        self.log_phase("4. VALIDATE")

        with self.time_phase("validate"):
            # Check for duplicate IDs (should not happen, but verify)
            entity_ids = set()
            for entity_id in registry['entities'].keys():
                if entity_id in entity_ids:
                    raise BuildError(
                        code="MAP-E002",
                        message=f"Duplicate entity ID: {entity_id}",
                        phase="validate"
                    )
                entity_ids.add(entity_id)

            # Check for unresolved dependencies
            unresolved = []
            for relation in registry['relations']:
                if relation['type'] == 'depends_on':
                    if relation['to_id'] not in registry['entities']:
                        unresolved.append((relation['from_id'], relation['to_id']))

            if unresolved:
                self.warnings.append(BuildWarning(
                    code="MAP-W003",
                    message=f"{len(unresolved)} unresolved dependencies found"
                ))
                if self.verbose:
                    for from_id, to_id in unresolved[:5]:
                        self.log(f"  {from_id} -> {to_id} (missing)", "WARN")

            self.log(f"Validated {len(registry['entities'])} entities", "OK")
            self.log(f"Validated {len(registry['relations'])} relations", "OK")

    @staticmethod
    def _flatten_entity(e: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten entity from normalizer format (raw_data nested) to schema-conformant flat format."""
        raw = e.get('raw_data', {})
        base = {
            'id': e['id'],
            'kind': e['kind'],
            'name': e['name'],
            'summary': e.get('summary') or raw.get('summary', ''),
            'status': raw.get('status', 'UNKNOWN'),
            'health': raw.get('health', 'UNKNOWN'),
            'owners': raw.get('owners', []),
            'dependencies': raw.get('dependencies', []),
            'blockers': raw.get('blockers', []),
            'updated_at': raw.get('updated_at') or '1970-01-01T00:00:00Z',
            'evidence': raw.get('evidence', []),
            'source_refs': e.get('source_refs', []),
            'detail_url': raw.get('detail_url', f"details/roadmap/{e['id']}.html"),
        }
        if e['kind'] == 'milestone':
            base.update({
                'outcome': raw.get('outcome') or raw.get('summary', ''),
                'start_date': raw.get('start_date', None),
                'end_date': raw.get('end_date', None),
                'tasks': raw.get('tasks', []),
                'critical_path': bool(raw.get('critical_path', False)),
            })
        elif e['kind'] == 'task':
            base.update({
                'milestone_id': raw.get('milestone_id', ''),
                'acceptance_criteria': raw.get('acceptance_criteria') or ['(no criteria defined)'],
                'outputs': raw.get('outputs') or ['(no outputs defined)'],
                'estimated_effort': raw.get('estimated_effort', None),
                'actual_completion_date': raw.get('actual_completion_date', None),
            })
        return base

    def phase_render(self, registry: Dict[str, Any], sources_manifest: List[Dict], git_commit: str = 'unknown') -> Dict[str, Path]:
        """Phase 5: Render JSON datasets"""
        self.log_phase("5. RENDER")

        with self.time_phase("render"):
            staging_dir = self.repo_root / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'staging'
            staging_dir.mkdir(parents=True, exist_ok=True)

            rendered_files = {}

            # Render roadmap.json — flatten entities to schema-conformant flat structure
            roadmap_entities = {
                eid: e for eid, e in registry['entities'].items()
                if e['kind'] in ['milestone', 'task']
            }

            roadmap_data = {
                'schema_version': '1.0.0',
                'milestones': [self._flatten_entity(e) for e in roadmap_entities.values() if e['kind'] == 'milestone'],
                'tasks': [self._flatten_entity(e) for e in roadmap_entities.values() if e['kind'] == 'task']
            }

            roadmap_path = staging_dir / 'roadmap.json'
            with open(roadmap_path, 'w', encoding='utf-8') as f:
                json.dump(roadmap_data, f, indent=2, ensure_ascii=False)
            rendered_files['roadmap.json'] = roadmap_path

            # Render build-manifest.json — omit null optional fields
            def _warning_dict(w):
                d = {'code': w.code, 'message': w.message}
                if w.file is not None:
                    d['file'] = w.file
                return d

            def _error_dict(err):
                d = {'code': err.code, 'message': err.message, 'phase': err.phase}
                if err.file is not None:
                    d['file'] = err.file
                return d

            manifest = {
                'schema_version': '1.0.0',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '1.0.0',
                'git_commit': git_commit,
                'sources': sources_manifest,
                'datasets': [
                    {
                        'filename': 'roadmap.json',
                        'entity_count': len(roadmap_data['milestones']) + len(roadmap_data['tasks']),
                        'schema_version': '1.0.0'
                    }
                ],
                'errors': [_error_dict(e) for e in self.errors],
                'warnings': [_warning_dict(w) for w in self.warnings],
                'last_valid_snapshot': None,
                'phase_durations': self.phase_durations,
                'freshness_status': 'STALE' if any(w.code in ('MAP-E003', 'MAP-E008') for w in self.warnings) else 'FRESH'
            }

            manifest_path = staging_dir / 'build-manifest.json'
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            rendered_files['build-manifest.json'] = manifest_path

            self.log(f"Rendered {len(rendered_files)} datasets to staging", "OK")
            return rendered_files

    def phase_validate_generated(self, rendered_files: Dict[str, Path]):
        """Phase 5b: Validate generated datasets against JSON schemas (MAP-E001)"""
        self.log_phase("5b. VALIDATE GENERATED")

        try:
            import jsonschema
            from jsonschema import RefResolver
        except ImportError:
            self.log("jsonschema not installed — skipping schema validation of generated datasets", "WARN")
            return

        schemas_dir = self.repo_root / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'schemas'
        pairs = [
            ('roadmap.json', 'roadmap.schema.json'),
            ('build-manifest.json', 'build-manifest.schema.json'),
        ]

        for dataset_name, schema_name in pairs:
            dataset_path = rendered_files.get(dataset_name)
            schema_path = schemas_dir / schema_name
            if not dataset_path or not dataset_path.exists() or not schema_path.exists():
                continue
            try:
                with open(dataset_path, encoding='utf-8') as f:
                    data = json.load(f)
                with open(schema_path, encoding='utf-8') as f:
                    schema = json.load(f)
                # Pre-load all schemas into store to avoid HTTP fetches for $ref resolution
                store = {}
                for sf in schemas_dir.glob('*.schema.json'):
                    with open(sf, encoding='utf-8') as fsf:
                        s = json.load(fsf)
                    if '$id' in s:
                        store[s['$id']] = s
                    store[sf.as_uri()] = s
                resolver = RefResolver(base_uri=schema_path.as_uri(), referrer=schema, store=store)
                jsonschema.validate(instance=data, schema=schema, resolver=resolver)
                self.log(f"Schema valid: {dataset_name}", "OK")
            except jsonschema.ValidationError as e:
                path_str = ' -> '.join(str(p) for p in e.absolute_path) or '(root)'
                raise BuildError(
                    code="MAP-E001",
                    message=f"Generated '{dataset_name}' fails schema validation at {path_str}: {e.message}",
                    phase="validate",
                    file=str(dataset_path)
                )
            except Exception as e:
                self.warnings.append(BuildWarning(
                    code="MAP-W004",
                    message=f"Could not validate '{dataset_name}' against schema: {e}"
                ))

    def phase_publish(self, rendered_files: Dict[str, Path]):
        """Phase 6: Atomic publish to docs/data/generated/"""
        self.log_phase("6. PUBLISH")

        with self.time_phase("publish"):
            target_dir = self.repo_root / 'docs' / 'data' / 'generated'

            if self.dry_run:
                self.log(f"DRY RUN: Would publish {len(rendered_files)} files to {target_dir}", "INFO")
                for filename in rendered_files.keys():
                    self.log(f"  - {filename}", "INFO")
                return

            # Atomic publish: replace entire directory
            if target_dir.exists():
                backup_dir = target_dir.parent / 'generated.bak'
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                shutil.move(str(target_dir), str(backup_dir))

            target_dir.mkdir(parents=True, exist_ok=True)

            # Guard: all required outputs must be present before atomic rename (MAP-E007)
            required_outputs = ['roadmap.json', 'build-manifest.json']
            missing = [r for r in required_outputs if r not in rendered_files or not rendered_files[r].exists()]
            if missing:
                raise BuildError(
                    code="MAP-E007",
                    message=f"Incomplete staging — missing: {', '.join(missing)}. Publish aborted to prevent partial output.",
                    phase="publish"
                )

            # Copy staged files
            for filename, staged_path in rendered_files.items():
                target_path = target_dir / filename
                shutil.copy2(str(staged_path), str(target_path))

            self.log(f"Published {len(rendered_files)} datasets to {target_dir}", "OK")

    def build(self) -> int:
        """Run complete build pipeline"""
        try:
            print("\n" + "="*60)
            print("PROJECT MAP BUILD PIPELINE")
            print("="*60)
            print(f"Repository: {self.repo_root}")
            print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
            print(f"Verbose: {self.verbose}")

            # Phase 1: Collect
            collector_results = self.phase_collect()

            # Phase 2: Normalize
            registry = self.phase_normalize(collector_results)

            # Phase 3: Derive
            enriched_registry = self.phase_derive(registry)

            # Phase 4: Validate
            self.phase_validate(enriched_registry)

            # Phase 5: Render
            sources_manifest = CollectorRegistry(self.repo_root).collect_sources_manifest(collector_results)
            git_commit = collector_results.get('git_metadata')
            git_hash = git_commit.data.get('commit_hash', 'unknown') if git_commit else 'unknown'
            rendered_files = self.phase_render(enriched_registry, sources_manifest, git_hash)

            # Phase 5b: Validate generated datasets against schemas (MAP-E001)
            self.phase_validate_generated(rendered_files)

            # Phase 6: Publish
            self.phase_publish(rendered_files)

            # Summary
            total_duration = (datetime.now(timezone.utc) - self.start_time).total_seconds()

            print("\n" + "="*60)
            print("BUILD SUMMARY")
            print("="*60)
            print(f"Status: {'DRY RUN COMPLETED' if self.dry_run else 'SUCCESS'}")
            print(f"Duration: {total_duration:.2f}s")
            print(f"Errors: {len(self.errors)}")
            print(f"Warnings: {len(self.warnings)}")

            if self.warnings:
                print("\nWarnings:")
                for w in self.warnings:
                    print(f"  [{w.code}] {w.message}")

            if self.errors:
                print("\nErrors:")
                for e in self.errors:
                    print(f"  [{e.code}] {e.message} (phase: {e.phase})")
                return 1

            return 2 if self.warnings else 0

        except BuildError as e:
            self.errors.append(e)
            print(f"\n[CRITICAL ERROR] [{e.code}] {e.message}")
            print(f"  Phase: {e.phase}")
            if e.file:
                print(f"  File: {e.file}")
            return 1

        except Exception as e:
            print(f"\n[UNEXPECTED ERROR] {e}")
            import traceback
            traceback.print_exc()
            return 1

def main():
    parser = argparse.ArgumentParser(description="Build TR4D3RZ project map datasets")
    parser.add_argument('--dry-run', action='store_true', help='Run without publishing')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent

    builder = ProjectMapBuilder(repo_root, dry_run=args.dry_run, verbose=args.verbose)
    exit_code = builder.build()

    return exit_code

if __name__ == '__main__':
    exit(main())
