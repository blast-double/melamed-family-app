#!/usr/bin/env python3
"""
Cross-meeting task deduplication.

Before creating a new Asana task, checks if a semantically equivalent task
already exists in the target project. If so, returns the match so the caller
can update it instead of creating a duplicate.

Uses: Asana project task listing for candidates + Gemini for semantic confirmation.
Prompt: config/prompts/task_dedup.md
"""
import json
import re
from pathlib import Path
from typing import Optional, List

from execution.taskops.asana_client import list_project_tasks, get_task
from execution.utils.gemini_rest import generate_content


WORKSPACE_ROOT = Path(__file__).parent.parent.parent
PROMPT_PATH = WORKSPACE_ROOT / "config" / "prompts" / "task_dedup.md"


def _load_prompt() -> str:
    with open(PROMPT_PATH) as f:
        return f.read()


def _extract_keywords(title: str) -> List[str]:
    """Extract meaningful keywords from a task title."""
    stop_words = {
        "the", "a", "an", "to", "for", "and", "or", "in", "on", "at", "of",
        "with", "from", "by", "is", "are", "was", "were", "be", "been",
        "this", "that", "it", "its", "up", "out", "about", "into",
    }
    words = re.findall(r'\b[a-zA-Z]{2,}\b', title.lower())
    return [w for w in words if w not in stop_words][:4]


def _keyword_overlap(keywords: List[str], task_name: str) -> bool:
    """Check if any keyword appears in the task name (case-insensitive)."""
    name_lower = task_name.lower()
    return any(kw in name_lower for kw in keywords)


def find_existing_task(
    project_gid: str,
    new_title: str,
    new_context: str,
) -> Optional[dict]:
    """
    Search for an existing task that matches this action item.

    Uses list_project_tasks (free-tier compatible) instead of the premium
    search API. Filters locally by keyword overlap, then confirms via Gemini.

    Returns {"gid": str, "name": str, "notes": str} if a confident match
    is found, or None if no match.
    """
    keywords = _extract_keywords(new_title)
    if not keywords:
        return None

    # List all incomplete tasks in the project
    try:
        all_tasks = list_project_tasks(project_gid, opt_fields="name,completed")
    except Exception:
        return None

    # Filter to incomplete tasks with keyword overlap
    candidates = [
        t for t in all_tasks
        if not t.get("completed") and _keyword_overlap(keywords, t.get("name", ""))
    ]

    if not candidates:
        return None

    # Fetch notes for candidates (list endpoint doesn't return notes)
    enriched = []
    for c in candidates[:10]:
        try:
            full = get_task(c["gid"], opt_fields="name,notes")
            enriched.append(full)
        except Exception:
            enriched.append({"gid": c["gid"], "name": c["name"], "notes": ""})

    # Build the existing tasks block for the prompt
    existing_lines = []
    for i, t in enumerate(enriched, 1):
        notes_preview = (t.get("notes") or "")[:200].replace("\n", " ")
        existing_lines.append(f'{i}. [{t["gid"]}] "{t["name"]}" — {notes_preview}')
    existing_block = "\n".join(existing_lines)

    # Load and fill prompt
    prompt_template = _load_prompt()
    prompt = prompt_template.replace("{new_title}", new_title)
    prompt = prompt.replace("{new_context}", new_context[:500])
    prompt = prompt.replace("{existing_tasks}", existing_block)

    try:
        raw = generate_content(prompt, model="gemini-2.0-flash", response_mime_type="application/json")
        result = json.loads(raw)
    except Exception:
        return None

    match_gid = result.get("match_gid")
    confidence = result.get("confidence", 0)

    if not match_gid or confidence < 0.8:
        return None

    # Return the matched task's full data
    for t in enriched:
        if t["gid"] == match_gid:
            return {"gid": t["gid"], "name": t["name"], "notes": t.get("notes", "")}

    return None
