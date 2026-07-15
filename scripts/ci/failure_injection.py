#!/usr/bin/env python3
"""
Failure injection tool for PMAP-16 observability scenarios.

Each scenario:
  1. Backs up the target file(s)
  2. Injects the failure condition
  3. Runs build_project_map.py --dry-run (or --live for E007)
  4. Captures and displays the log output
  5. Restores the original file(s)

Usage:
    python scripts/ci/failure_injection.py --scenario <name> [--live]
    python scripts/ci/failure_injection.py --list

Scenarios:
    schema-invalid       MAP-E001 — inject bad enum into roadmap.yaml
    missing-snapshot     MAP-E003 — rename ecosystem-snapshot.json away
    missing-source       MAP-E004 — rename roadmap.yaml away
    browser-corrupt      MAP-E005 — corrupt generated roadmap.json (UI-side)
    interrupted-publish  MAP-E007 — remove a file from staging mid-build
    stale-data           MAP-E008 — set old mtime on ecosystem-snapshot.json

Exit codes:
    0: Expected error code detected in output
    1: Expected error code NOT detected (injection may have failed)
    2: Unexpected exception during injection
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent
BUILD_CMD = [sys.executable, str(REPO_ROOT / 'scripts' / 'build_project_map.py'), '--verbose']

SCENARIOS = {
    'schema-invalid':      ('MAP-E001', 'Inject invalid enum into roadmap.yaml'),
    'missing-snapshot':    ('MAP-E003', 'Rename ecosystem-snapshot.json away'),
    'missing-source':      ('MAP-E004', 'Rename roadmap.yaml away'),
    'browser-corrupt':     ('MAP-E005', 'Corrupt generated roadmap.json (UI-side — browser load error)'),
    'interrupted-publish': ('MAP-E007', 'Remove required file from staging before publish'),
    'stale-data':          ('MAP-E008', 'Set old mtime on ecosystem-snapshot.json'),
}


def run_build(dry_run: bool = True) -> tuple[int, str]:
    cmd = BUILD_CMD.copy()
    if dry_run:
        cmd.append('--dry-run')
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    output = result.stdout + result.stderr
    return result.returncode, output


def inject_schema_invalid() -> tuple[Path, bytes]:
    """Corrupt roadmap.yaml with an invalid status enum → MAP-E001."""
    path = REPO_ROOT / 'state' / 'roadmap.yaml'
    original = path.read_bytes()
    corrupted = path.read_text(encoding='utf-8').replace(
        'status: IN_PROGRESS', 'status: INVALID_ENUM_VALUE', 1
    )
    path.write_text(corrupted, encoding='utf-8')
    return path, original


def inject_missing_snapshot() -> tuple[Path, Path]:
    """Rename ecosystem-snapshot.json → triggers MAP-E003."""
    src = REPO_ROOT / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'ecosystem-snapshot.json'
    dst = src.with_suffix('.json.bak_fi')
    shutil.move(str(src), str(dst))
    return src, dst


def inject_missing_source() -> tuple[Path, Path]:
    """Rename roadmap.yaml → triggers MAP-E004."""
    src = REPO_ROOT / 'state' / 'roadmap.yaml'
    dst = src.with_suffix('.yaml.bak_fi')
    shutil.move(str(src), str(dst))
    return src, dst


def inject_browser_corrupt() -> tuple[Path, bytes]:
    """Write invalid JSON to generated roadmap.json → triggers MAP-E005 in browser."""
    path = REPO_ROOT / 'docs' / 'data' / 'generated' / 'roadmap.json'
    if not path.exists():
        raise FileNotFoundError(f"Generated roadmap.json not found at {path}. Run build first.")
    original = path.read_bytes()
    path.write_text('{ INVALID JSON --- injected by failure_injection.py', encoding='utf-8')
    return path, original


def inject_stale_data() -> tuple[Path, float]:
    """Set mtime of ecosystem-snapshot.json to 48h ago → triggers MAP-E008."""
    path = REPO_ROOT / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'ecosystem-snapshot.json'
    if not path.exists():
        raise FileNotFoundError(f"ecosystem-snapshot.json not found at {path}")
    original_mtime = path.stat().st_mtime
    stale_time = time.time() - (48 * 3600)  # 48 hours ago
    os.utime(path, (stale_time, stale_time))
    return path, original_mtime


def run_scenario(name: str, live: bool = False):
    expected_code, description = SCENARIOS[name]
    print(f"\n{'='*60}")
    print(f"FAILURE INJECTION: {name}")
    print(f"Expected code   : {expected_code}")
    print(f"Description     : {description}")
    print(f"{'='*60}\n")

    restore_actions = []
    detected = False
    exit_code = 0

    try:
        # --- Inject ---
        if name == 'schema-invalid':
            path, original = inject_schema_invalid()
            restore_actions.append(('bytes', path, original))

        elif name == 'missing-snapshot':
            src, dst = inject_missing_snapshot()
            restore_actions.append(('move', dst, src))

        elif name == 'missing-source':
            src, dst = inject_missing_source()
            restore_actions.append(('move', dst, src))

        elif name == 'browser-corrupt':
            path, original = inject_browser_corrupt()
            restore_actions.append(('bytes', path, original))
            # MAP-E005 is a browser-side error — the build won't fail.
            # We just corrupt the file and show it.
            print("[NOTE] MAP-E005 is a browser-side error. The pipeline will succeed.")
            print("       The corrupted file is shown below; restore it before committing.\n")

        elif name == 'interrupted-publish':
            # We cannot easily interrupt a running process; instead we simulate
            # a partial staging directory (remove build-manifest.json from staging after render)
            # by monkey-patching: we run with --dry-run and note that MAP-E007 would fire
            # on a real publish if staging were incomplete.
            print("[NOTE] MAP-E007: simulating by temporarily removing build-manifest.json from staging.\n")
            staging = REPO_ROOT / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'staging'
            manifest_staged = staging / 'build-manifest.json'
            if manifest_staged.exists():
                bak = manifest_staged.with_suffix('.json.bak_fi')
                shutil.move(str(manifest_staged), str(bak))
                restore_actions.append(('move', bak, manifest_staged))
            # Run build (live, not dry-run, so it reaches publish phase)
            live = True

        elif name == 'stale-data':
            path, original_mtime = inject_stale_data()
            restore_actions.append(('mtime', path, original_mtime))

        # --- Run build ---
        use_dry_run = (name != 'interrupted-publish') and (not live)
        returncode, output = run_build(dry_run=use_dry_run)

        print("--- BUILD OUTPUT ---")
        print(output)
        print(f"--- EXIT CODE: {returncode} ---\n")

        # --- Check for expected error code ---
        if expected_code in output:
            print(f"[OK] Expected code {expected_code} found in output.")
            detected = True
        else:
            print(f"[FAIL] Expected code {expected_code} NOT found in output.")
            print(f"       Check injection logic or pipeline code for {name}.")
            exit_code = 1

    except Exception as e:
        print(f"[ERROR] Injection failed: {e}")
        exit_code = 2

    finally:
        # --- Restore ---
        for action, *args in restore_actions:
            try:
                if action == 'bytes':
                    path, data = args
                    path.write_bytes(data)
                    print(f"[RESTORED] {path.name}")
                elif action == 'move':
                    src, dst = args
                    shutil.move(str(src), str(dst))
                    print(f"[RESTORED] {dst.name}")
                elif action == 'mtime':
                    path, mtime = args
                    os.utime(path, (mtime, mtime))
                    print(f"[RESTORED] mtime of {path.name}")
            except Exception as e:
                print(f"[WARN] Could not restore: {e}")

    status = "PASS" if detected else "FAIL"
    print(f"\nResult: {status}")
    return exit_code


def main():
    parser = argparse.ArgumentParser(
        description="Failure injection tool for MAP-E diagnostic scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n".join(f"  {k:22s} {v[0]}  {v[1]}" for k, v in SCENARIOS.items())
    )
    parser.add_argument('--scenario', choices=list(SCENARIOS.keys()),
                        help='Failure scenario to inject')
    parser.add_argument('--list', action='store_true',
                        help='List all available scenarios')
    parser.add_argument('--live', action='store_true',
                        help='Run build in live mode (not dry-run). WARNING: modifies docs/data/generated/')
    args = parser.parse_args()

    if args.list or not args.scenario:
        print("Available failure injection scenarios:\n")
        for name, (code, desc) in SCENARIOS.items():
            print(f"  --scenario {name}")
            print(f"    Expected code: {code}")
            print(f"    Description:   {desc}\n")
        return 0

    return run_scenario(args.scenario, live=args.live)


if __name__ == '__main__':
    sys.exit(main())
