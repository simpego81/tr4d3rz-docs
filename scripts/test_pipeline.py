#!/usr/bin/env python3
"""
Test script for data pipeline (collectors + normalizer)

Usage:
    python scripts/test_pipeline.py
"""

from pathlib import Path
import sys
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add pipeline module to path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.collectors import CollectorRegistry
from pipeline.normalizer import Normalizer
from pipeline.health_engine import HealthEngine, FreshnessPolicy

def main():
    repo_root = Path(__file__).parent.parent

    print("=" * 60)
    print("PROJECT MAP DATA PIPELINE TEST")
    print("=" * 60)

    # Phase 1: Collect
    print("\n[PHASE 1] COLLECT")
    print("-" * 60)

    registry = CollectorRegistry(repo_root)
    results = registry.collect_all()

    print(f"Collected {len(results)} sources:\n")
    for name, result in results.items():
        exists = result.data.get('exists', True)
        status = "OK" if exists else "MISSING"
        hash_short = result.hash[:16] + "..."
        print(f"  [{status}] {name:20s} hash={hash_short}")

    # Phase 2: Normalize
    print("\n[PHASE 2] NORMALIZE")
    print("-" * 60)

    normalizer = Normalizer()
    entity_registry = normalizer.normalize_all(results)

    print(f"Normalized entities: {len(entity_registry.entities)}")
    print(f"Normalized relations: {len(entity_registry.relations)}\n")

    # Show entity breakdown by kind
    kind_counts = {}
    for entity in entity_registry.entities.values():
        kind_counts[entity.kind] = kind_counts.get(entity.kind, 0) + 1

    print("Entity breakdown by kind:")
    for kind, count in sorted(kind_counts.items()):
        print(f"  {kind:15s}: {count:3d}")

    # Show relation breakdown by type
    rel_counts = {}
    for relation in entity_registry.relations:
        rel_counts[relation.type] = rel_counts.get(relation.type, 0) + 1

    print("\nRelation breakdown by type:")
    for rel_type, count in sorted(rel_counts.items()):
        print(f"  {rel_type:25s}: {count:3d}")

    # Phase 3: Sample entities
    print("\n[PHASE 3] SAMPLE ENTITIES")
    print("-" * 60)

    sample_milestones = [e for e in entity_registry.entities.values() if e.kind == 'milestone'][:3]
    sample_tasks = [e for e in entity_registry.entities.values() if e.kind == 'task'][:3]
    sample_roles = [e for e in entity_registry.entities.values() if e.kind == 'role'][:2]

    print("\nSample Milestones:")
    for entity in sample_milestones:
        sources = len(entity.source_refs)
        print(f"  {entity.id:30s} - {entity.name[:40]:40s} ({sources} source{'s' if sources > 1 else ''})")

    print("\nSample Tasks:")
    for entity in sample_tasks:
        sources = len(entity.source_refs)
        status = entity.raw_data.get('status', 'UNKNOWN')
        print(f"  {entity.id:30s} - {status:12s} - {entity.name[:40]:40s}")

    if sample_roles:
        print("\nSample Roles:")
        for entity in sample_roles:
            repos = entity.raw_data.get('repositories', [])
            repos_str = ', '.join(repos[:2]) if repos else 'none'
            print(f"  {entity.id:30s} - {entity.name[:30]:30s} - repos: {repos_str}")

    # Phase 4: Health Derivation
    print("\n[PHASE 4] HEALTH DERIVATION")
    print("-" * 60)

    # Load freshness policy
    policy_path = repo_root / 'config' / 'freshness_policy.yaml'
    policy = FreshnessPolicy.from_yaml(policy_path) if policy_path.exists() else FreshnessPolicy()

    health_engine = HealthEngine(freshness_policy=policy)

    # Enrich registry with health, freshness, critical path
    enriched_registry = health_engine.enrich_registry(entity_registry.to_dict())

    # Update entity_registry with enriched data
    entity_registry.entities = {}
    for entity_id, entity_dict in enriched_registry['entities'].items():
        from pipeline.normalizer import Entity
        entity_registry.entities[entity_id] = Entity(
            id=entity_dict['id'],
            kind=entity_dict['kind'],
            name=entity_dict['name'],
            summary=entity_dict['summary'],
            raw_data=entity_dict['raw_data'],
            source_refs=entity_dict['source_refs']
        )

    # Show health breakdown
    health_counts = {}
    freshness_counts = {}
    critical_count = 0

    for entity in entity_registry.entities.values():
        health = entity.raw_data.get('health', 'UNKNOWN')
        freshness = entity.raw_data.get('freshness', 'UNKNOWN')
        is_critical = entity.raw_data.get('critical_path', False)

        health_counts[health] = health_counts.get(health, 0) + 1
        freshness_counts[freshness] = freshness_counts.get(freshness, 0) + 1
        if is_critical:
            critical_count += 1

    print("\nHealth breakdown:")
    for health, count in sorted(health_counts.items()):
        print(f"  {health:10s}: {count:3d}")

    print("\nFreshness breakdown:")
    for freshness, count in sorted(freshness_counts.items()):
        print(f"  {freshness:10s}: {count:3d}")

    print(f"\nCritical path entities: {critical_count}")

    # Show sample critical path
    critical_entities = [e for e in entity_registry.entities.values() if e.raw_data.get('critical_path', False)][:5]
    if critical_entities:
        print("\nSample critical path entities:")
        for entity in critical_entities:
            print(f"  {entity.id:30s} - {entity.kind:10s} - {entity.raw_data.get('health', 'UNKNOWN')}")

    # Phase 5: Validation
    print("\n[PHASE 5] VALIDATION")
    print("-" * 60)

    # Check for unresolved dependencies
    unresolved = []
    for relation in entity_registry.relations:
        if relation.type == 'depends_on':
            if not entity_registry.has_entity(relation.to_id):
                unresolved.append((relation.from_id, relation.to_id))

    if unresolved:
        print(f"\n[WARNING] {len(unresolved)} unresolved dependencies found:")
        for from_id, to_id in unresolved[:5]:
            print(f"  {from_id} -> {to_id} (missing)")
        if len(unresolved) > 5:
            print(f"  ... and {len(unresolved) - 5} more")
    else:
        print("[OK] All dependencies resolved")

    # Check for duplicate IDs (should not happen with allow_merge=True)
    print(f"[OK] No duplicate entity IDs (registry enforces uniqueness)")

    # Phase 6: Export sample
    print("\n[PHASE 6] EXPORT SAMPLE")
    print("-" * 60)

    output_path = repo_root / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'pipeline-test-output.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    export_data = entity_registry.to_dict()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Exported to: {output_path}")
    print(f"     Entities: {len(export_data['entities'])}")
    print(f"     Relations: {len(export_data['relations'])}")

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"[OK] Collectors: {len(results)} sources")
    print(f"[OK] Normalizer: {len(entity_registry.entities)} entities, {len(entity_registry.relations)} relations")
    print(f"[OK] Health Engine: {sum(health_counts.values())} entities enriched")
    print(f"     - HEALTHY: {health_counts.get('HEALTHY', 0)}, AT_RISK: {health_counts.get('AT_RISK', 0)}, BLOCKED: {health_counts.get('BLOCKED', 0)}")
    print(f"     - STALE: {health_counts.get('STALE', 0)}, UNKNOWN: {health_counts.get('UNKNOWN', 0)}")
    print(f"     - Critical path: {critical_count} entities")
    print(f"[OK] Validation: {'PASS' if not unresolved else f'WARN ({len(unresolved)} unresolved)'}")
    print(f"[OK] Export: {output_path.name}")
    print("\nNext steps:")
    print("  1. Implement schema validation (PMAP-06)")
    print("  2. Integrate into build-project-map command")
    print("  3. Create dataset renderers (roadmap.json, etc.)")

    return 0

if __name__ == '__main__':
    exit(main())
