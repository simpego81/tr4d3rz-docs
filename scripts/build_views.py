#!/usr/bin/env python3
"""
build_views.py — Generate docs/data/ JSON files from state/ sources.

Reads:
  - state/roadmap.yaml         → milestone + task definitions (SSOT)
  - docs/data/agent_activity.json → agent activity log

Writes:
  - docs/data/stakeholder_data.json   → milestone KPIs for view overlays
  - docs/data/roadmap_data.json       → full task/milestone data for D3 roadmap view
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = REPO_ROOT / "state"
DATA_DIR = REPO_ROOT / "docs" / "data"

ROADMAP_YAML = STATE_DIR / "roadmap.yaml"
AGENT_ACTIVITY = DATA_DIR / "agent_activity.json"
STAKEHOLDER_OUT = DATA_DIR / "stakeholder_data.json"
ROADMAP_OUT = DATA_DIR / "roadmap_data.json"

STATUS_WEIGHT = {
    "COMPLETED": 1.0,
    "READY": 0.0,
    "IN_PROGRESS": 0.5,
    "BLOCKED": 0.0,
    "PLANNED": 0.0,
}

ACTIVE_STATUSES = {"READY", "IN_PROGRESS"}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def compute_milestone_stats(milestone: dict, all_tasks: list[dict]) -> dict:
    task_ids = set(milestone.get("tasks", []))
    m_tasks = [t for t in all_tasks if t["id"] in task_ids]

    total = len(m_tasks)
    if total == 0:
        return {"total_tasks": 0, "completed_tasks": 0, "completion_pct": 0, "active_task_ids": []}

    completed = sum(1 for t in m_tasks if t.get("status") == "COMPLETED")
    # Partial credit for IN_PROGRESS tasks
    weighted = sum(STATUS_WEIGHT.get(t.get("status", "PLANNED"), 0.0) for t in m_tasks)
    pct = round((weighted / total) * 100)

    active = [t["id"] for t in m_tasks if t.get("status") in ACTIVE_STATUSES]

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_pct": pct,
        "active_task_ids": active,
    }


def build_stakeholder_data(roadmap: dict, activity: dict) -> dict:
    milestones = roadmap.get("milestones", [])
    tasks = roadmap.get("tasks", [])

    # Last activity from agent_activity.json
    activities = activity.get("activities", [])
    last_activity = max((a["timestamp"] for a in activities), default=None)

    milestone_summaries = []
    total_weight = 0.0
    total_count = 0

    for m in milestones:
        stats = compute_milestone_stats(m, tasks)
        milestone_summaries.append({
            "id": m["id"],
            "name": m["name"],
            "status": m.get("status", "PLANNED"),
            "summary": m.get("summary", ""),
            "completion_pct": stats["completion_pct"],
            "total_tasks": stats["total_tasks"],
            "completed_tasks": stats["completed_tasks"],
            "active_task_ids": stats["active_task_ids"],
            "critical_path": m.get("critical_path", False),
            "start_date": m.get("start_date"),
            "end_date": m.get("end_date"),
            "dependencies": m.get("dependencies", []),
        })
        if stats["total_tasks"] > 0:
            total_weight += stats["completion_pct"] * stats["total_tasks"]
            total_count += stats["total_tasks"]

    overall_pct = round(total_weight / total_count) if total_count > 0 else 0

    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "project": roadmap.get("metadata", {}).get("project", "TR4D3RZ"),
        "current_milestone": roadmap.get("metadata", {}).get("current_milestone"),
        "last_activity": last_activity,
        "overall_completion_pct": overall_pct,
        "milestones": milestone_summaries,
    }


def build_roadmap_data(roadmap: dict) -> dict:
    milestones = roadmap.get("milestones", [])
    tasks = roadmap.get("tasks", [])

    task_index = {t["id"]: t for t in tasks}

    milestone_out = []
    for m in milestones:
        stats = compute_milestone_stats(m, tasks)
        task_ids = m.get("tasks", [])
        m_tasks = []
        for tid in task_ids:
            t = task_index.get(tid)
            if t:
                m_tasks.append({
                    "id": t["id"],
                    "name": t["name"],
                    "summary": t.get("summary", ""),
                    "status": t.get("status", "PLANNED"),
                    "estimated_effort": t.get("estimated_effort"),
                    "actual_completion_date": t.get("actual_completion_date"),
                    "dependencies": t.get("dependencies", []),
                    "blockers": t.get("blockers", []),
                    "owners": t.get("owners", []),
                    "detail_url": t.get("detail_url"),
                })
        milestone_out.append({
            "id": m["id"],
            "name": m["name"],
            "summary": m.get("summary", ""),
            "status": m.get("status", "PLANNED"),
            "start_date": m.get("start_date"),
            "end_date": m.get("end_date"),
            "critical_path": m.get("critical_path", False),
            "dependencies": m.get("dependencies", []),
            "completion_pct": stats["completion_pct"],
            "total_tasks": stats["total_tasks"],
            "completed_tasks": stats["completed_tasks"],
            "tasks": m_tasks,
        })

    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "project": roadmap.get("metadata", {}).get("project", "TR4D3RZ"),
        "current_milestone": roadmap.get("metadata", {}).get("current_milestone"),
        "milestones": milestone_out,
    }


def main() -> int:
    errors = []

    if not ROADMAP_YAML.exists():
        errors.append(f"Missing: {ROADMAP_YAML}")
    if not AGENT_ACTIVITY.exists():
        errors.append(f"Missing: {AGENT_ACTIVITY}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    roadmap = load_yaml(ROADMAP_YAML)
    activity = load_json(AGENT_ACTIVITY)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    stakeholder_data = build_stakeholder_data(roadmap, activity)
    roadmap_data = build_roadmap_data(roadmap)

    STAKEHOLDER_OUT.write_text(
        json.dumps(stakeholder_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    ROADMAP_OUT.write_text(
        json.dumps(roadmap_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    current_m_id = roadmap.get("metadata", {}).get("current_milestone", "—")
    current_m = next(
        (m for m in stakeholder_data["milestones"] if m["id"] == current_m_id), None
    )
    pct = current_m["completion_pct"] if current_m else "?"

    print(f"OK  stakeholder_data.json — current milestone: {pct}% complete")
    print(f"OK  roadmap_data.json     — {len(roadmap_data['milestones'])} milestones, "
          f"{sum(len(m['tasks']) for m in roadmap_data['milestones'])} tasks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
