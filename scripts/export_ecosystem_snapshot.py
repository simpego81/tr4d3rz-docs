#!/usr/bin/env python3
"""
Export sanitized ecosystem snapshot from C:/projects/seq/.ecosystem

This exporter reads agent boards and rules, strips private content (free-text
notes, detailed assumptions, open questions), and produces a publishable JSON
snapshot for the project map.

Usage:
    python scripts/export_ecosystem_snapshot.py

Output:
    artifacts/features/FEATURE-DOCS-PROJECT-MAP/ecosystem-snapshot.json
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Allowlist of publishable board fields
ALLOWED_BOARD_FIELDS = {
    'agent_id',
    'last_update',
    'current_task',
    'role',
    'repositories',
    'confidence_level',
    'blockers',
    'vetos_issued_count',
    'vetos_received_count'
}

# Fields to EXCLUDE (private/sensitive)
EXCLUDED_FIELDS = [
    'context_assumptions',       # May contain internal assumptions
    'recent_decisions',          # May reveal strategic reasoning
    'open_questions',            # May expose uncertainty to stakeholders
    'uncertainty_sources',       # Private diagnostic info
    'collaboration_surface',     # Inter-agent communication details
    'key_dependencies'           # May be sensitive
]

def compute_directory_hash(dir_path: Path) -> str:
    """Compute SHA-256 hash of directory state (file names + sizes)"""
    hasher = hashlib.sha256()

    # Sort files for deterministic hash
    files = sorted(dir_path.rglob('*'))

    for file_path in files:
        if file_path.is_file():
            rel_path = file_path.relative_to(dir_path)
            hasher.update(str(rel_path).encode('utf-8'))
            hasher.update(str(file_path.stat().st_size).encode('utf-8'))

    return hasher.hexdigest()

def parse_agent_board(board_path: Path) -> Dict[str, Any]:
    """
    Parse agent board markdown file and extract ONLY allowed fields.

    Returns sanitized dict with:
    - agent_id (from filename)
    - last_update (from header)
    - current_task (from Current Intent section)
    - role (hardcoded mapping)
    - confidence_level (from Confidence Level section)
    - blockers (from Active Constraints → Blockers)
    - vetos_issued_count, vetos_received_count (counts only)
    """

    with open(board_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract agent_id from filename (e.g., "claude_code_board.md" → "claude-code")
    agent_id = board_path.stem.replace('_board', '').replace('_', '-')

    # Role mapping (hardcoded - safe for public)
    ROLE_MAP = {
        'claude-code': 'Implementation Agent',
        'manus': 'Chief Architect',
        'antigravity': 'Visualization Agent',
        'github-copilot': 'QA Validator',
        'hra': 'Human Relation Agent'
    }

    # Repository mapping (from AGENTS.md knowledge)
    REPO_MAP = {
        'claude-code': ['tr4d3rz-core', 'tr4d3rz-messaging', 'tr4d3rz-evolution', 'tr4d3rz-persistence'],
        'manus': ['tr4d3rz-docs'],
        'antigravity': ['tr4d3rz-observatory'],
        'github-copilot': ['tr4d3rz-embedded'],
        'hra': []
    }

    sanitized = {
        'agent_id': agent_id,
        'role': ROLE_MAP.get(agent_id, 'Unknown'),
        'repositories': REPO_MAP.get(agent_id, [])
    }

    # Extract Last Update (safe)
    last_update_match = re.search(r'\*\*Last Update\*\*:\s*(.+)', content)
    if last_update_match:
        try:
            # Try to parse as ISO date
            update_str = last_update_match.group(1).strip()
            # Simple ISO conversion (may need refinement for actual format)
            sanitized['last_update'] = datetime.fromisoformat(update_str.replace(' UTC', '+00:00')).isoformat()
        except Exception:
            sanitized['last_update'] = datetime.utcnow().isoformat() + 'Z'
    else:
        sanitized['last_update'] = datetime.utcnow().isoformat() + 'Z'

    # Extract Current Intent → current_task (sanitized to task ID only)
    intent_section = re.search(r'## 1\. Current Intent\n\n\*\*What am I doing right now\?\*\*\n\n(.+?)(?=\n\n\*\*|---|\Z)', content, re.DOTALL)
    if intent_section:
        intent_text = intent_section.group(1).strip()
        # Try to extract task ID (e.g., "M1-T3", "PMAP-02")
        task_match = re.search(r'\b([A-Z0-9]+-T?[0-9A-Z-]+)\b', intent_text)
        if task_match:
            sanitized['current_task'] = task_match.group(1)
        else:
            sanitized['current_task'] = None
    else:
        sanitized['current_task'] = None

    # Extract Confidence Level (safe - it's a metric)
    confidence_match = re.search(r'\*\*Overall Task Confidence\*\*:\s*(\d+)%', content)
    if confidence_match:
        sanitized['confidence_level'] = int(confidence_match.group(1))
    else:
        sanitized['confidence_level'] = None

    # Extract Blockers (from Active Constraints section - sanitized)
    blockers = []
    blockers_section = re.search(r'\*\*Blockers\*\*\s*\(waiting on\):\n(.+?)(?=\n\n---|\Z)', content, re.DOTALL)
    if blockers_section:
        blocker_lines = blockers_section.group(1).strip().split('\n')
        for line in blocker_lines:
            # Format: "- {Blocker 1}: {owner} — {status}"
            blocker_match = re.match(r'-\s*(.+?):\s*(.+?)\s*—\s*(.+)', line)
            if blocker_match:
                blockers.append({
                    'description': blocker_match.group(1).strip(),
                    'owner': blocker_match.group(2).strip(),
                    'status': blocker_match.group(3).strip().lower()
                })

    sanitized['blockers'] = blockers

    # Extract Veto counts (counts only - no details)
    vetos_issued_section = re.search(r'\*\*Vetos I issued\*\*:\n(.+?)(?=\n\n\*\*|\Z)', content, re.DOTALL)
    vetos_received_section = re.search(r'\*\*Vetos received\*\*:\n(.+?)(?=\n\n\*\*|\Z)', content, re.DOTALL)

    vetos_issued = len(re.findall(r'^-\s', vetos_issued_section.group(1), re.MULTILINE)) if vetos_issued_section else 0
    vetos_received = len(re.findall(r'^-\s', vetos_received_section.group(1), re.MULTILINE)) if vetos_received_section else 0

    sanitized['vetos_issued_count'] = vetos_issued
    sanitized['vetos_received_count'] = vetos_received

    return sanitized

def extract_rules_summary(ecosystem_dir: Path) -> Dict[str, Any]:
    """Extract high-level rules summary (veto gates, handoff protocol, HRA)"""

    # Hardcoded summary based on .ecosystem/README.md knowledge
    # This avoids parsing complex Markdown and exposing implementation details

    return {
        'veto_gates': [
            {
                'name': 'Pre-Commit Check',
                'enforcer': 'Librarian Agent',
                'trigger': 'Before task completion'
            },
            {
                'name': 'Protocol Integrity',
                'enforcer': 'Chief Architect',
                'trigger': 'Before protocol/contract change'
            },
            {
                'name': 'Demo Validation',
                'enforcer': 'QA Validator',
                'trigger': 'Before merge without observable demo'
            },
            {
                'name': 'Debuggability Gate',
                'enforcer': 'Debug Intelligence Agent',
                'trigger': 'Before merge without <2min diagnosis capability'
            }
        ],
        'artifact_handoff': {
            'enabled': True,
            'artifact_path': 'artifacts/features/FEATURE-XXX/'
        },
        'hra_protocol': {
            'enabled': True,
            'cadence': 'daily morning (09:00) + evening (18:00), weekly convergence (Friday 17:00)'
        }
    }

def export_snapshot(ecosystem_dir: Path, output_path: Path) -> Dict[str, Any]:
    """Export sanitized ecosystem snapshot"""

    if not ecosystem_dir.exists():
        raise FileNotFoundError(f".ecosystem directory not found at {ecosystem_dir}")

    agents_dir = ecosystem_dir / 'agents'
    if not agents_dir.exists():
        raise FileNotFoundError(f"agents directory not found at {agents_dir}")

    # Compute directory hash
    source_hash = compute_directory_hash(ecosystem_dir)

    # Parse agent boards
    agents = []
    for board_path in agents_dir.glob('*_board.md'):
        if board_path.stem == 'TEMPLATE_agent' or 'TEMPLATE' in board_path.stem:
            continue  # Skip template

        try:
            sanitized_board = parse_agent_board(board_path)
            # Skip if agent_id contains 'template' (case-insensitive)
            if 'template' in sanitized_board['agent_id'].lower():
                continue
            agents.append(sanitized_board)
        except Exception as e:
            print(f"Warning: Failed to parse {board_path.name}: {e}")
            continue

    # Extract rules summary
    rules_summary = extract_rules_summary(ecosystem_dir)

    # Build snapshot
    snapshot = {
        'schema_version': '1.0.0',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'source_hash': source_hash,
        'agents': agents,
        'rules_summary': rules_summary,
        'excluded_fields': EXCLUDED_FIELDS
    }

    return snapshot

def main():
    """Main entry point"""
    import sys
    # Fix Windows console encoding
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    repo_root = Path(__file__).parent.parent
    ecosystem_dir = Path('C:/projects/seq/.ecosystem')
    output_path = repo_root / 'artifacts' / 'features' / 'FEATURE-DOCS-PROJECT-MAP' / 'ecosystem-snapshot.json'

    print(f"Exporting sanitized ecosystem snapshot...")
    print(f"  Source: {ecosystem_dir}")
    print(f"  Output: {output_path}")

    try:
        snapshot = export_snapshot(ecosystem_dir, output_path)

        # Write snapshot
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Snapshot exported:")
        print(f"  Schema version: {snapshot['schema_version']}")
        print(f"  Generated at: {snapshot['generated_at']}")
        print(f"  Source hash: {snapshot['source_hash'][:16]}...")
        print(f"  Agents: {len(snapshot['agents'])}")
        print(f"  Veto gates: {len(snapshot['rules_summary']['veto_gates'])}")
        print(f"  Excluded fields: {len(snapshot['excluded_fields'])}")

        # Show agent summary
        print(f"\nAgent summary:")
        for agent in snapshot['agents']:
            task = agent.get('current_task') or 'idle'
            conf = agent.get('confidence_level')
            conf_str = f"{conf}%" if conf is not None else "N/A"
            print(f"  - {agent['agent_id']}: {task} (confidence: {conf_str})")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nNote: .ecosystem is a local directory and may not exist on CI.")
        print("This is expected. The committed snapshot will be used instead.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
