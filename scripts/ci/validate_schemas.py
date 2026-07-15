#!/usr/bin/env python3
"""
CI schema validation script for PMAP-15.

Validates:
1. Schema files are valid JSON
2. Generated roadmap.json conforms to roadmap.schema.json
3. Generated build-manifest.json conforms to build-manifest.schema.json

Exit codes:
  0: All validations passed
  1: One or more validations failed
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
except ImportError:
    print("[ERROR] jsonschema package not installed. Run: pip install jsonschema")
    sys.exit(1)


def load_json(path: Path, label: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] {label}: file not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] {label}: invalid JSON — {e}")
        return None


def validate_schema_file(schema_path: Path) -> bool:
    data = load_json(schema_path, schema_path.name)
    if data is None:
        return False
    try:
        jsonschema.Draft202012Validator.check_schema(data)
        print(f"[OK]    Schema valid: {schema_path.name}")
        return True
    except SchemaError as e:
        print(f"[ERROR] Schema invalid: {schema_path.name} — {e.message}")
        return False


def build_schema_store(schemas_dir: Path) -> dict:
    """Pre-load all schemas keyed by $id to avoid HTTP fetches for $ref resolution."""
    store = {}
    for f in schemas_dir.glob("*.schema.json"):
        with open(f, encoding="utf-8") as fp:
            s = json.load(fp)
        if "$id" in s:
            store[s["$id"]] = s
        # Also register by local file URI so relative $ref works both ways
        store[f.as_uri()] = s
    return store


def validate_dataset(dataset_path: Path, schema_path: Path, label: str, schemas_dir: Path = None) -> bool:
    data = load_json(dataset_path, label)
    schema = load_json(schema_path, schema_path.name)
    if data is None or schema is None:
        return False

    # Pre-load all schemas to avoid HTTP fetches when resolving $ref
    store = build_schema_store(schemas_dir or schema_path.parent)
    resolver = jsonschema.RefResolver(
        base_uri=schema_path.as_uri(),
        referrer=schema,
        store=store,
    )
    try:
        validate(instance=data, schema=schema, resolver=resolver)
        print(f"[OK]    Dataset valid: {label}")
        return True
    except ValidationError as e:
        print(f"[ERROR] Dataset invalid: {label}")
        print(f"        Path: {' -> '.join(str(p) for p in e.absolute_path) or '(root)'}")
        print(f"        {e.message}")
        return False


def main() -> int:
    repo_root = Path(__file__).parent.parent.parent
    schemas_dir = repo_root / "artifacts" / "features" / "FEATURE-DOCS-PROJECT-MAP" / "schemas"
    generated_dir = repo_root / "docs" / "data" / "generated"

    failures = 0

    print("=" * 60)
    print("SCHEMA VALIDATION")
    print("=" * 60)

    # 1. Validate each schema file is itself valid JSON Schema
    schema_files = list(schemas_dir.glob("*.schema.json"))
    if not schema_files:
        print(f"[WARN] No schema files found in {schemas_dir}")
    for schema_file in sorted(schema_files):
        if not validate_schema_file(schema_file):
            failures += 1

    print()
    print("=" * 60)
    print("DATASET VALIDATION")
    print("=" * 60)

    # 2. Validate generated datasets
    pairs = [
        (generated_dir / "roadmap.json", schemas_dir / "roadmap.schema.json", "roadmap.json"),
        (generated_dir / "build-manifest.json", schemas_dir / "build-manifest.schema.json", "build-manifest.json"),
    ]
    for dataset_path, schema_path, label in pairs:
        if not dataset_path.exists():
            print(f"[WARN]  Dataset not found (skipping): {label}")
            continue
        if not validate_dataset(dataset_path, schema_path, label, schemas_dir=schemas_dir):
            failures += 1

    print()
    print("=" * 60)
    if failures == 0:
        print(f"RESULT: PASS (0 failures)")
    else:
        print(f"RESULT: FAIL ({failures} failure(s))")
    print("=" * 60)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
