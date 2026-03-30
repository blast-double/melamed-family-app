# Last Edited: 2026-03-26 00:00
"""
Personal task classifier — takes raw task data and returns Asana-ready
structured output (description, tags, section, assignee).

Adapted from Itero's shared classifier. Simplified for personal use:
no company signals, no meeting fields, no confidence/triage.
"""
from __future__ import annotations

from typing import List, Optional

from execution.taskops.asana_client import (
    _load_tag_config,
    ensure_tag,
    list_workspace_tags,
)
from execution.taskops.router import get_asana_constants


PROJECT_DISPLAY = {
    "home": "Home",
    "travel": "Travel",
    "finance": "Finance",
    "social": "Social",
    "health": "Health",
    "baby": "Baby",
    "mateo": "Mateo",
}

ASSIGNEE_NAMES = {
    "aaron": "Aaron",
    "eugenia": "Eugenia",
}

PRIORITY_TAGS = {
    "high": "Priority: High",
    "medium": "Priority: Medium",
    "low": "Priority: Low",
}

SOURCE_TAG_MAP = {
    "manual": "Source: Manual",
}


def _normalize_priority(raw: str) -> Optional[str]:
    """Normalize priority input to 'high', 'medium', 'low', or None."""
    lower = raw.strip().lower()
    if lower in PRIORITY_TAGS:
        return lower
    return "medium"


def _resolve_assignee(assignee_raw: Optional[str], constants: dict) -> tuple:
    """Resolve assignee string to (display_name, gid) or (None, None)."""
    if not assignee_raw:
        return None, None
    key = assignee_raw.strip().lower()
    if key == "aaron":
        return "Aaron", constants.get("aaron_gid")
    if key == "eugenia":
        return "Eugenia", constants.get("eugenia_gid")
    return None, None


def classify(task: dict) -> dict:
    """Classify and enrich a raw task into Asana-ready structured output.

    Args:
        task: dict with keys:
            title (str, required)
            context (str, optional)
            project (str, required) — project key
            priority (str, optional, default medium)
            due_date (str, optional) — ISO date
            source (str, required) — manual
            assignee (str, optional) — "aaron" or "eugenia"
            tag_hints (list[str], optional) — extra tag names
            section (str, optional) — override section name

    Returns:
        dict with keys: title, description, section, tags, tag_gids,
        priority, due_date, assignee_gid
    """
    title = task.get("title", "Untitled")
    context = task.get("context") or ""
    project = task.get("project", "home")
    priority = _normalize_priority(task.get("priority", "medium"))
    source = task.get("source", "manual")
    section = task.get("section", "To Do")
    due_date = task.get("due_date")
    tag_hints = task.get("tag_hints") or []

    constants = get_asana_constants()
    assignee_name, assignee_gid = _resolve_assignee(task.get("assignee"), constants)

    description = _build_description(
        context=context,
        project=project,
        priority=priority,
        assignee_name=assignee_name,
        source=source,
    )

    tag_config = _load_tag_config()
    tags_spec = _resolve_tag_specs(project, priority, source, tag_hints, tag_config)

    workspace_gid = constants.get("workspace_gid", "")
    cache = list_workspace_tags(workspace_gid)

    tag_gids = []
    for name, color in tags_spec:
        gid = ensure_tag(workspace_gid, name, color, _cache=cache)
        tag_gids.append(gid)
        cache[name.lower().strip()] = {"gid": gid, "name": name, "color": color}

    return {
        "title": title,
        "description": description,
        "section": section,
        "tags": [{"name": n, "color": c} for n, c in tags_spec],
        "tag_gids": tag_gids,
        "priority": priority,
        "due_date": due_date,
        "assignee_gid": assignee_gid,
    }


def _build_description(
    context: str,
    project: str,
    priority: str,
    assignee_name: Optional[str],
    source: str,
) -> str:
    """Build a structured Asana task description."""
    parts = []

    if context and context.strip():
        parts.append(f"Context: {context.strip()}")
    else:
        parts.append("Context: Manual task — no additional context provided.")
    parts.append("")

    parts.append("---")

    project_display = PROJECT_DISPLAY.get(project.lower(), project.title())
    parts.append(f"Project: {project_display}")

    if assignee_name:
        parts.append(f"Assignee: {assignee_name}")

    priority_display = PRIORITY_TAGS.get(priority, "Medium").replace("Priority: ", "")
    parts.append(f"Priority: {priority_display}")

    source_label = SOURCE_TAG_MAP.get(source, f"Source: {source.title()}")
    parts.append(source_label)

    return "\n".join(parts)


def _resolve_tag_specs(
    project: str,
    priority: str,
    source: str,
    tag_hints: List[str],
    tag_config: dict,
) -> List[tuple]:
    """Resolve all tags into (name, color) pairs without hitting Asana API."""
    categories = tag_config.get("categories", {})
    specs = []

    project_name = PROJECT_DISPLAY.get(project.lower(), project.title())
    project_colors = categories.get("project", {}).get("tags", {})
    specs.append((project_name, project_colors.get(project_name, "none")))

    if priority and priority in PRIORITY_TAGS:
        priority_name = PRIORITY_TAGS[priority]
        priority_colors = categories.get("priority", {}).get("tags", {})
        specs.append((priority_name, priority_colors.get(priority_name, "light-orange")))

    source_name = SOURCE_TAG_MAP.get(source, f"Source: {source.title()}")
    source_colors = categories.get("source", {}).get("tags", {})
    specs.append((source_name, source_colors.get(source_name, "light-warm-gray")))

    person_default = categories.get("person", {}).get("default_color", "light-teal")
    for hint in tag_hints:
        hint = hint.strip()
        if hint:
            specs.append((hint, person_default))

    return specs
