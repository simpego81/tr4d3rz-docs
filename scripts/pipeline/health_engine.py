#!/usr/bin/env python3
"""
Health, freshness and dependency derivation engine

Implements the priority-based health derivation rules from ADR-PROJECT-MAP-001:

Priority | Condition | Derived Health
---------|-----------|---------------
1        | Status BLOCKED OR critical blocker active | BLOCKED
2        | Source exceeds freshness threshold AND status not terminal | STALE
3        | Required dependency BLOCKED/UNKNOWN/unresolved OR high risk unmitigated | AT_RISK
4        | Status consistent, sources valid, dependencies satisfied, evidence present | HEALTHY
5        | Insufficient or conflicting data | UNKNOWN

Also derives:
- Freshness status (FRESH/STALE/UNKNOWN)
- Critical path for roadmap (milestones/tasks on longest dependency chain)
- Blocker propagation (blocked dependency → dependent becomes AT_RISK)
"""

from typing import Dict, List, Any, Set, Tuple
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class FreshnessPolicy:
    """Configurable freshness thresholds by source type"""
    roadmap_hours: int = 168  # 7 days
    archimate_hours: int = 720  # 30 days
    ecosystem_hours: int = 24  # 1 day
    project_state_hours: int = 168  # 7 days
    default_hours: int = 168  # 7 days

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'FreshnessPolicy':
        """Load policy from YAML file"""
        if not yaml_path.exists():
            return cls()  # Use defaults

        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return cls(
            roadmap_hours=data.get('roadmap_hours', 168),
            archimate_hours=data.get('archimate_hours', 720),
            ecosystem_hours=data.get('ecosystem_hours', 24),
            project_state_hours=data.get('project_state_hours', 168),
            default_hours=data.get('default_hours', 168)
        )

    def get_threshold(self, source_type: str) -> int:
        """Get freshness threshold in hours for source type"""
        mapping = {
            'roadmap': self.roadmap_hours,
            'archimate': self.archimate_hours,
            'ecosystem_snapshot': self.ecosystem_hours,
            'project_state': self.project_state_hours
        }
        return mapping.get(source_type, self.default_hours)

class HealthEngine:
    """Derives health, freshness and critical path from entity registry"""

    def __init__(self, freshness_policy: FreshnessPolicy = None):
        self.policy = freshness_policy or FreshnessPolicy()
        self.now = datetime.now(timezone.utc)

    def derive_health(self, entity: Dict[str, Any], registry: Dict[str, Any]) -> str:
        """
        Derive health status for an entity using priority rules.

        Args:
            entity: Entity dict from normalized registry
            registry: Full entity registry for dependency lookups

        Returns:
            Health status: HEALTHY, AT_RISK, BLOCKED, STALE, UNKNOWN
        """
        raw_data = entity.get('raw_data', {})
        status = raw_data.get('status', 'UNKNOWN')

        # Priority 1: BLOCKED status or critical blocker
        if status == 'BLOCKED':
            return 'BLOCKED'

        blockers = raw_data.get('blockers', [])
        critical_blockers = [b for b in blockers if b.get('severity') == 'CRITICAL']
        if critical_blockers:
            return 'BLOCKED'

        # Priority 2: STALE (source exceeds freshness threshold AND status not terminal)
        terminal_statuses = ['COMPLETED', 'DEPRECATED']
        if status not in terminal_statuses:
            freshness = self.check_freshness(entity)
            if freshness == 'STALE':
                return 'STALE'

        # Priority 3: AT_RISK (dependency issues or high risk)
        if self.has_risky_dependencies(entity, registry):
            return 'AT_RISK'

        high_blockers = [b for b in blockers if b.get('severity') == 'HIGH']
        if high_blockers:
            return 'AT_RISK'

        # Priority 4: HEALTHY (all conditions satisfied)
        if status in ['COMPLETED', 'IN_PROGRESS', 'READY'] and self.has_evidence(entity):
            return 'HEALTHY'

        # Priority 5: UNKNOWN (insufficient data)
        return 'UNKNOWN'

    def check_freshness(self, entity: Dict[str, Any]) -> str:
        """
        Check if entity sources are fresh.

        Returns:
            FRESH, STALE, or UNKNOWN
        """
        source_refs = entity.get('source_refs', [])
        if not source_refs:
            return 'UNKNOWN'

        for source_ref in source_refs:
            extracted_at_str = source_ref.get('extracted_at')
            if not extracted_at_str:
                continue

            try:
                extracted_at = datetime.fromisoformat(extracted_at_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                continue

            # Infer source type from path
            path = source_ref.get('path', '')
            source_type = self.infer_source_type(path)
            threshold_hours = self.policy.get_threshold(source_type)
            threshold = timedelta(hours=threshold_hours)

            age = self.now - extracted_at
            if age > threshold:
                return 'STALE'

        return 'FRESH'

    def infer_source_type(self, path: str) -> str:
        """Infer source type from file path"""
        if 'roadmap.yaml' in path:
            return 'roadmap'
        elif 'archimate' in path:
            return 'archimate'
        elif 'ecosystem-snapshot' in path:
            return 'ecosystem_snapshot'
        elif 'project_state' in path:
            return 'project_state'
        else:
            return 'unknown'

    def has_risky_dependencies(self, entity: Dict[str, Any], registry: Dict[str, Any]) -> bool:
        """
        Check if entity has risky dependencies.

        A dependency is risky if:
        - It's BLOCKED
        - It's UNKNOWN
        - It's unresolved (doesn't exist in registry)
        """
        raw_data = entity.get('raw_data', {})
        dependencies = raw_data.get('dependencies', [])
        entities = registry.get('entities', {})

        for dep_id in dependencies:
            # Unresolved dependency
            if dep_id not in entities:
                return True

            # Check dependency health/status
            dep_entity = entities[dep_id]
            dep_raw = dep_entity.get('raw_data', {})
            dep_status = dep_raw.get('status', 'UNKNOWN')

            if dep_status in ['BLOCKED', 'UNKNOWN']:
                return True

        return False

    def has_evidence(self, entity: Dict[str, Any]) -> bool:
        """Check if entity has evidence (for COMPLETED status)"""
        raw_data = entity.get('raw_data', {})
        status = raw_data.get('status', 'UNKNOWN')

        # COMPLETED requires evidence
        if status == 'COMPLETED':
            evidence = raw_data.get('evidence', [])
            return len(evidence) > 0

        # Other statuses don't require evidence for HEALTHY
        return True

    def derive_critical_path(self, registry: Dict[str, Any]) -> Set[str]:
        """
        Derive critical path through roadmap (longest dependency chain).

        Returns:
            Set of entity IDs on the critical path
        """
        entities = registry.get('entities', {})
        relations = registry.get('relations', [])

        # Build dependency graph
        graph = {}
        for entity_id in entities.keys():
            graph[entity_id] = []

        for relation in relations:
            if relation['type'] == 'depends_on':
                from_id = relation['from_id']
                to_id = relation['to_id']
                if from_id in graph:
                    graph[from_id].append(to_id)

        # Compute longest path from each node (DFS with memoization)
        memo = {}

        def longest_path(node_id: str) -> int:
            if node_id in memo:
                return memo[node_id]

            if node_id not in graph or not graph[node_id]:
                memo[node_id] = 0
                return 0

            max_length = 0
            for dep_id in graph[node_id]:
                if dep_id in graph:  # Only if dependency exists
                    length = 1 + longest_path(dep_id)
                    max_length = max(max_length, length)

            memo[node_id] = max_length
            return max_length

        # Compute longest path for all nodes
        for node_id in graph.keys():
            longest_path(node_id)

        # Find maximum length
        if not memo:
            return set()

        max_length = max(memo.values())

        # Collect all nodes on paths of maximum length
        critical = set()

        def collect_critical(node_id: str):
            if memo.get(node_id, 0) == max_length:
                critical.add(node_id)
            for dep_id in graph.get(node_id, []):
                if dep_id in memo and memo[dep_id] == max_length - 1:
                    critical.add(dep_id)
                    collect_critical(dep_id)

        # Start from nodes with max length
        for node_id, length in memo.items():
            if length == max_length:
                collect_critical(node_id)

        return critical

    def enrich_entity(self, entity: Dict[str, Any], registry: Dict[str, Any], critical_path: Set[str]) -> Dict[str, Any]:
        """
        Enrich entity with derived health, freshness and critical path flag.

        Args:
            entity: Entity dict to enrich
            registry: Full registry for dependency lookups
            critical_path: Set of entity IDs on critical path

        Returns:
            Enriched entity dict
        """
        enriched = entity.copy()
        raw_data = enriched.get('raw_data', {})

        # Derive health
        health = self.derive_health(entity, registry)
        raw_data['health'] = health

        # Check freshness
        freshness = self.check_freshness(entity)
        raw_data['freshness'] = freshness

        # Mark critical path
        raw_data['critical_path'] = entity['id'] in critical_path

        enriched['raw_data'] = raw_data
        return enriched

    def enrich_registry(self, registry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich entire registry with health, freshness and critical path.

        Args:
            registry: Entity registry from normalizer

        Returns:
            Enriched registry
        """
        enriched_registry = {
            'entities': {},
            'relations': registry.get('relations', [])
        }

        # Derive critical path once
        critical_path = self.derive_critical_path(registry)

        # Enrich each entity
        for entity_id, entity in registry.get('entities', {}).items():
            enriched_registry['entities'][entity_id] = self.enrich_entity(
                entity,
                registry,
                critical_path
            )

        return enriched_registry
