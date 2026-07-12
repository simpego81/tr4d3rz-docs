"""
Project Map Data Pipeline

This package implements the deterministic data pipeline for the GitHub Pages
project map, transforming SSOT sources into validated JSON datasets.

Pipeline phases:
1. Collect: Read SSOT sources (roadmap.yaml, ArchiMate, ecosystem snapshot, Git)
2. Normalize: Convert to canonical entity/relation model with stable IDs
3. Validate: Apply JSON Schema, check refs, enums, required fields (PMAP-06)
4. Derive: Calculate health, freshness, critical path (PMAP-05)
5. Render: Generate JSON datasets + HTML detail pages (PMAP-06)
6. Publish: Atomic replacement of docs/data/generated/ (PMAP-06)

Usage:
    from pipeline.collectors import CollectorRegistry
    from pipeline.normalizer import Normalizer

    registry = CollectorRegistry(repo_root)
    results = registry.collect_all()

    normalizer = Normalizer()
    entities = normalizer.normalize_all(results)
"""

__version__ = "1.0.0"
__all__ = ['collectors', 'normalizer']
