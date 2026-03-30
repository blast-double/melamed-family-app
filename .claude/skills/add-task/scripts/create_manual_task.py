#!/usr/bin/env python3
# Last Edited: 2026-03-27 00:00
"""
Create a task in Asana for the personal workspace.

Uses the shared task_classifier for description and tags. Checks for
semantic duplicates via Gemini before creating.

Usage:
    python3 .claude/skills/add-task/scripts/create_manual_task.py \
        --title "Buy groceries" \
        --project home \
        --priority medium \
        --section "To Do" \
        --due 2026-03-28 \
        --assignee aaron \
        --description "Need milk and eggs"
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add workspace root to path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from dotenv import load_dotenv
load_dotenv(WORKSPACE_ROOT / ".env")

from execution.taskops.router import get_project_gid
from execution.taskops.asana_client import create_task, update_task, find_section
from execution.taskops.task_classifier import classify
from execution.taskops.dedup import find_existing_task


def main():
    parser = argparse.ArgumentParser(description="Create a personal task in Asana")
    parser.add_argument("--title", required=True, help="Task title (action-verb-first)")
    parser.add_argument("--project", default="home", help="Project key (home, travel, finance, social, health, baby, mateo)")
    parser.add_argument("--priority", default="medium", help="low/medium/high")
    parser.add_argument("--section", default="To Do", help="Section name")
    parser.add_argument("--due", default=None, help="ISO date (YYYY-MM-DD)")
    parser.add_argument("--assignee", default=None, help="aaron or eugenia")
    parser.add_argument("--description", default=None, help="Task context")
    parser.add_argument("--tags", default=None, help="Comma-separated extra tag names (person tags, etc.)")
    args = parser.parse_args()

    asana_project_gid = get_project_gid(args.project)
    if not asana_project_gid or asana_project_gid == "PLACEHOLDER":
        print(json.dumps({"status": "error", "message": f"No Asana GID found for project '{args.project}'. Run setup_workspace.py first."}))
        sys.exit(1)

    extra_tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    classified = classify({
        "title": args.title,
        "context": args.description or "",
        "project": args.project,
        "priority": args.priority,
        "due_date": args.due,
        "source": "manual",
        "assignee": args.assignee,
        "tag_hints": extra_tags,
        "section": args.section,
    })

    # Dedup check: does a matching task already exist?
    existing = find_existing_task(asana_project_gid, classified["title"], classified["description"])
    if existing:
        now = datetime.now(timezone.utc).isoformat()
        new_notes = existing["notes"] + "\n\n---\nUpdate ({}):\n{}".format(
            now[:10], classified["description"]
        )
        update_task(existing["gid"], {"notes": new_notes})

        result = {
            "status": "updated",
            "asana_task_gid": existing["gid"],
            "asana_url": f"https://app.asana.com/0/0/{existing['gid']}",
            "existing_task_name": existing["name"],
        }
        print(json.dumps(result, indent=2))
        return

    # Create new task
    section_gid = find_section(asana_project_gid, classified["section"])
    task_gid = create_task(
        project_gid=asana_project_gid,
        name=classified["title"],
        notes=classified["description"],
        due_date=args.due,
        assignee_gid=classified["assignee_gid"],
        section_gid=section_gid,
        tag_gids=classified["tag_gids"],
    )

    applied_tags = [t["name"] for t in classified["tags"]]

    result = {
        "status": "created",
        "asana_task_gid": task_gid,
        "asana_url": f"https://app.asana.com/0/0/{task_gid}",
        "section": classified["section"],
        "tags": applied_tags,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
