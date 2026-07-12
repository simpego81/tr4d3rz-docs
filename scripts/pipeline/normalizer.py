#!/usr/bin/env python3
"""
Canonical normalizer for project map data pipeline

The normalizer converts raw collector data into a canonical entity/relation model:

Entity:
  - id (stable, kebab-case)
  - kind (concept, component, role, milestone, task, etc.)
  - name (human-readable)
  - summary
  - raw_data (source-specific fields)
  - source_refs (list of source file provenance)

Relation:
  - from_id
  - to_id
  - type (depends_on, implements, owns, etc.)
  - source_refs

This module is pure: no I/O, only data transformation.
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Entity:
    """Canonical entity in the project map"""
    id: str
    kind: str
    name: str
    summary: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
    source_refs: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'kind': self.kind,
            'name': self.name,
            'summary': self.summary,
            'raw_data': self.raw_data,
            'source_refs': self.source_refs
        }

@dataclass
class Relation:
    """Canonical relation between entities"""
    from_id: str
    to_id: str
    type: str
    source_refs: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'from_id': self.from_id,
            'to_id': self.to_id,
            'type': self.type,
            'source_refs': self.source_refs
        }

class EntityRegistry:
    """Registry to track entities and detect duplicates"""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []

    def add_entity(self, entity: Entity, allow_merge: bool = False) -> bool:
        """
        Add entity to registry.

        Args:
            entity: Entity to add
            allow_merge: If True and entity exists, merge source_refs; if False, raise error

        Returns:
            True if added, False if merged

        Raises:
            ValueError if duplicate ID and allow_merge=False
        """
        if entity.id in self.entities:
            if not allow_merge:
                raise ValueError(f"Duplicate entity ID: {entity.id}")

            # Merge source_refs
            existing = self.entities[entity.id]
            existing.source_refs.extend(entity.source_refs)
            return False

        self.entities[entity.id] = entity
        return True

    def add_relation(self, relation: Relation):
        """Add relation to registry"""
        self.relations.append(relation)

    def get_entity(self, entity_id: str) -> Entity:
        """Get entity by ID or raise KeyError"""
        return self.entities[entity_id]

    def has_entity(self, entity_id: str) -> bool:
        """Check if entity exists"""
        return entity_id in self.entities

    def to_dict(self) -> Dict[str, Any]:
        """Convert registry to dictionary"""
        return {
            'entities': {eid: e.to_dict() for eid, e in self.entities.items()},
            'relations': [r.to_dict() for r in self.relations]
        }

class RoadmapNormalizer:
    """Normalize roadmap.yaml data to canonical entities"""

    @staticmethod
    def normalize(roadmap_data: Dict[str, Any], source_ref: Dict[str, str]) -> Tuple[List[Entity], List[Relation]]:
        """
        Normalize roadmap YAML to entities and relations.

        Args:
            roadmap_data: Raw roadmap.yaml data from RoadmapCollector
            source_ref: Source provenance metadata

        Returns:
            (entities, relations) tuple
        """
        entities = []
        relations = []

        milestones = roadmap_data.get('milestones', [])
        tasks = roadmap_data.get('tasks', [])

        # Normalize milestones
        for milestone in milestones:
            entity = Entity(
                id=milestone['id'],
                kind='milestone',
                name=milestone['name'],
                summary=milestone.get('summary', ''),
                raw_data=milestone,
                source_refs=[source_ref]
            )
            entities.append(entity)

            # Create dependency relations
            for dep_id in milestone.get('dependencies', []):
                relations.append(Relation(
                    from_id=milestone['id'],
                    to_id=dep_id,
                    type='depends_on',
                    source_refs=[source_ref]
                ))

        # Normalize tasks
        for task in tasks:
            entity = Entity(
                id=task['id'],
                kind='task',
                name=task['name'],
                summary=task.get('summary', ''),
                raw_data=task,
                source_refs=[source_ref]
            )
            entities.append(entity)

            # Create dependency relations
            for dep_id in task.get('dependencies', []):
                relations.append(Relation(
                    from_id=task['id'],
                    to_id=dep_id,
                    type='depends_on',
                    source_refs=[source_ref]
                ))

            # Create milestone relation
            if 'milestone_id' in task:
                relations.append(Relation(
                    from_id=task['id'],
                    to_id=task['milestone_id'],
                    type='belongs_to_milestone',
                    source_refs=[source_ref]
                ))

        return entities, relations

class ArchimateNormalizer:
    """Normalize ArchiMate data to canonical entities"""

    @staticmethod
    def normalize(archimate_data: Dict[str, Any], source_ref: Dict[str, str]) -> Tuple[List[Entity], List[Relation]]:
        """
        Normalize ArchiMate JSON to entities and relations.

        Args:
            archimate_data: Raw archimate_data.json from ArchimateCollector
            source_ref: Source provenance metadata

        Returns:
            (entities, relations) tuple
        """
        entities = []
        relations = []

        nodes = archimate_data.get('nodes', [])
        links = archimate_data.get('links', [])

        # Normalize nodes
        for node in nodes:
            # Derive kind from ArchiMate layer
            layer = node.get('layer', 'unknown')
            kind_map = {
                'Technology': 'component',
                'Application': 'component',
                'Business': 'concept',
                'Motivation': 'concept'
            }
            kind = kind_map.get(layer, 'concept')

            # Stable ID from ArchiMate ID (convert to kebab-case)
            stable_id = re.sub(r'[^a-z0-9-]', '-', node.get('id', '').lower()).strip('-')

            entity = Entity(
                id=stable_id or f"archimate-{node.get('id', 'unknown')}",
                kind=kind,
                name=node.get('name', 'Unnamed'),
                summary=node.get('documentation', ''),
                raw_data=node,
                source_refs=[source_ref]
            )
            entities.append(entity)

        # Normalize relationships
        for link in links:
            source_id = re.sub(r'[^a-z0-9-]', '-', link.get('source', '').lower()).strip('-')
            target_id = re.sub(r'[^a-z0-9-]', '-', link.get('target', '').lower()).strip('-')
            rel_type = link.get('type', 'related_to').lower().replace(' ', '_')

            relations.append(Relation(
                from_id=source_id or f"archimate-{link.get('source', 'unknown')}",
                to_id=target_id or f"archimate-{link.get('target', 'unknown')}",
                type=rel_type,
                source_refs=[source_ref]
            ))

        return entities, relations

class EcosystemNormalizer:
    """Normalize ecosystem snapshot to canonical entities"""

    @staticmethod
    def normalize(snapshot_data: Dict[str, Any], source_ref: Dict[str, str]) -> Tuple[List[Entity], List[Relation]]:
        """
        Normalize ecosystem snapshot to entities and relations.

        Args:
            snapshot_data: Raw ecosystem snapshot from EcosystemSnapshotCollector
            source_ref: Source provenance metadata

        Returns:
            (entities, relations) tuple
        """
        entities = []
        relations = []

        if not snapshot_data.get('exists', True):
            # Snapshot doesn't exist - return empty
            return entities, relations

        agents = snapshot_data.get('agents', [])

        # Normalize agents as role entities
        for agent in agents:
            entity = Entity(
                id=f"role-{agent['agent_id']}",
                kind='role',
                name=agent.get('role', 'Unknown Role'),
                summary=f"{agent.get('role', 'Unknown')} - {agent['agent_id']}",
                raw_data=agent,
                source_refs=[source_ref]
            )
            entities.append(entity)

            # Create ownership relations for repositories
            for repo in agent.get('repositories', []):
                repo_id = repo.replace('_', '-')
                relations.append(Relation(
                    from_id=f"role-{agent['agent_id']}",
                    to_id=f"component-{repo_id}",
                    type='owns',
                    source_refs=[source_ref]
                ))

        return entities, relations

class Normalizer:
    """Main normalizer that coordinates all source-specific normalizers"""

    def __init__(self):
        self.registry = EntityRegistry()

    def normalize_all(self, collector_results: Dict[str, Any]) -> EntityRegistry:
        """
        Normalize all collector results to canonical entities/relations.

        Args:
            collector_results: Dict of CollectorResult from CollectorRegistry.collect_all()

        Returns:
            EntityRegistry with all normalized entities and relations
        """
        # Normalize roadmap
        if 'roadmap' in collector_results:
            roadmap_result = collector_results['roadmap']
            entities, relations = RoadmapNormalizer.normalize(
                roadmap_result.data,
                roadmap_result.to_source_ref()
            )
            for entity in entities:
                self.registry.add_entity(entity, allow_merge=True)
            for relation in relations:
                self.registry.add_relation(relation)

        # Normalize ArchiMate data
        if 'archimate' in collector_results:
            archimate_result = collector_results['archimate']
            entities, relations = ArchimateNormalizer.normalize(
                archimate_result.data,
                archimate_result.to_source_ref()
            )
            for entity in entities:
                self.registry.add_entity(entity, allow_merge=True)
            for relation in relations:
                self.registry.add_relation(relation)

        # Normalize ecosystem snapshot
        if 'ecosystem_snapshot' in collector_results:
            snapshot_result = collector_results['ecosystem_snapshot']
            entities, relations = EcosystemNormalizer.normalize(
                snapshot_result.data,
                snapshot_result.to_source_ref()
            )
            for entity in entities:
                self.registry.add_entity(entity, allow_merge=True)
            for relation in relations:
                self.registry.add_relation(relation)

        return self.registry
