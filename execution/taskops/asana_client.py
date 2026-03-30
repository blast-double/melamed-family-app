#!/usr/bin/env python3
"""
Asana REST API client for serverless task creation.

Uses the Personal Access Token (ASANA_PAT) for auth — simpler than OAuth
for server-to-server calls. The MCP proxy handles interactive sessions;
this module handles automated task creation from the webhook pipeline.
"""
import os
import time
from typing import Optional, List, Dict
from pathlib import Path

import requests
import yaml


ASANA_BASE = "https://app.asana.com/api/1.0"

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def _get_headers() -> dict:
    """Build auth headers using PAT."""
    pat = os.getenv("ASANA_PAT")
    if not pat:
        raise RuntimeError("ASANA_PAT environment variable not set")
    return {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json",
    }


# ---------------------------------------------------------------------------
# Tag config
# ---------------------------------------------------------------------------

def _load_tag_config() -> dict:
    """Load config/asana_tags.yaml."""
    candidates = [
        Path(__file__).parent.parent.parent / "config" / "asana_tags.yaml",
        Path(os.getenv("WORKSPACE_ROOT", "")) / "config" / "asana_tags.yaml",
    ]
    for p in candidates:
        if p.exists():
            with open(p) as f:
                return yaml.safe_load(f)
    raise FileNotFoundError("config/asana_tags.yaml not found")


# ---------------------------------------------------------------------------
# Task creation
# ---------------------------------------------------------------------------

def create_task(
    project_gid: str,
    name: str,
    notes: Optional[str] = None,
    due_date: Optional[str] = None,
    assignee_gid: Optional[str] = None,
    section_gid: Optional[str] = None,
    tag_gids: Optional[List[str]] = None,
) -> str:
    """
    Create a task in Asana. Returns the new task GID.

    Args:
        project_gid: Asana project to add the task to.
        name: Task title (action-verb-first per convention).
        notes: Task description (Priority line + context).
        due_date: ISO date string (YYYY-MM-DD) or None.
        assignee_gid: User GID to assign. Defaults to ASANA_USER_GID env var.
        section_gid: Optional section GID (defaults to first section).
        tag_gids: Optional list of tag GIDs to apply.
    """
    data: dict = {
        "name": name,
        "projects": [project_gid],
    }
    if assignee_gid:
        data["assignee"] = assignee_gid
    if notes:
        data["notes"] = notes
    if due_date:
        data["due_on"] = due_date

    resp = requests.post(
        f"{ASANA_BASE}/tasks",
        headers=_get_headers(),
        json={"data": data},
        timeout=15,
    )
    resp.raise_for_status()
    task_gid = resp.json()["data"]["gid"]

    # Move to specific section if provided
    if section_gid:
        requests.post(
            f"{ASANA_BASE}/sections/{section_gid}/addTask",
            headers=_get_headers(),
            json={"data": {"task": task_gid}},
            timeout=10,
        )

    # Apply tags
    if tag_gids:
        add_tags_to_task(task_gid, tag_gids)

    return task_gid


def create_project(workspace_gid: str, name: str, team_gid: str,
                    notes: str = "", color: str = "light-green") -> str:
    """Create a project in Asana. Returns the new project GID."""
    resp = requests.post(
        f"{ASANA_BASE}/projects",
        headers=_get_headers(),
        json={"data": {
            "name": name, "workspace": workspace_gid,
            "team": team_gid, "notes": notes, "color": color,
        }},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def get_task(task_gid: str, opt_fields: str = "name,notes") -> dict:
    """Fetch a single task by GID. Returns task data dict."""
    resp = requests.get(
        f"{ASANA_BASE}/tasks/{task_gid}",
        headers=_get_headers(),
        params={"opt_fields": opt_fields},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]


def list_project_tasks(project_gid: str, opt_fields: str = "name,completed") -> List[dict]:
    """Paginate through all tasks in a project. Returns list of task dicts."""
    tasks: List[dict] = []
    url = f"{ASANA_BASE}/projects/{project_gid}/tasks"
    params: dict = {"opt_fields": opt_fields, "limit": 100}

    while url:
        resp = requests.get(url, headers=_get_headers(), params=params, timeout=15)
        resp.raise_for_status()
        body = resp.json()
        tasks.extend(body.get("data", []))
        next_page = body.get("next_page")
        if next_page and next_page.get("uri"):
            url = next_page["uri"]
            params = {}
        else:
            url = None  # type: ignore[assignment]

    return tasks


def delete_task(task_gid: str) -> None:
    """Delete a task by GID. Retries on 429 rate limit."""
    for attempt in range(3):
        resp = requests.delete(
            f"{ASANA_BASE}/tasks/{task_gid}",
            headers=_get_headers(),
            timeout=10,
        )
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            continue
        resp.raise_for_status()
        return
    resp.raise_for_status()


def update_task(task_gid: str, updates: dict) -> dict:
    """Update an existing Asana task. Returns updated task data.

    Supported fields: name, notes, due_on, assignee, completed, etc.
    """
    resp = requests.put(
        f"{ASANA_BASE}/tasks/{task_gid}",
        headers=_get_headers(),
        json={"data": updates},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]


def move_task_to_section(task_gid: str, section_gid: str) -> None:
    """Move an existing task to a specific section."""
    requests.post(
        f"{ASANA_BASE}/sections/{section_gid}/addTask",
        headers=_get_headers(),
        json={"data": {"task": task_gid}},
        timeout=10,
    )


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def find_section(project_gid: str, section_name: str) -> Optional[str]:
    """Find a section GID by name (case-insensitive) in a project."""
    resp = requests.get(
        f"{ASANA_BASE}/projects/{project_gid}/sections",
        headers=_get_headers(),
        timeout=10,
    )
    resp.raise_for_status()
    for section in resp.json().get("data", []):
        if section["name"].lower().strip() == section_name.lower().strip():
            return section["gid"]
    return None


def find_backlog_section(project_gid: str) -> Optional[str]:
    """Legacy wrapper — use find_section() for new code."""
    return find_section(project_gid, "Backlog")


def list_sections(project_gid: str) -> Dict[str, str]:
    """Return {name: gid} for all sections in a project."""
    resp = requests.get(
        f"{ASANA_BASE}/projects/{project_gid}/sections",
        headers=_get_headers(),
        timeout=10,
    )
    resp.raise_for_status()
    return {s["name"]: s["gid"] for s in resp.json().get("data", [])}


def create_section(project_gid: str, name: str) -> str:
    """Create a section in a project. Returns section GID."""
    resp = requests.post(
        f"{ASANA_BASE}/projects/{project_gid}/sections",
        headers=_get_headers(),
        json={"data": {"name": name}},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def reorder_section(project_gid: str, section_gid: str,
                    insert_after: Optional[str] = None) -> None:
    """Move a section to a specific position in the project."""
    data: dict = {"section": section_gid}
    if insert_after:
        data["insert_after"] = insert_after
    else:
        data["insert_before"] = None  # move to top (before everything)
    resp = requests.post(
        f"{ASANA_BASE}/projects/{project_gid}/sections/insert",
        headers=_get_headers(),
        json={"data": data},
        timeout=10,
    )
    resp.raise_for_status()


def ensure_sections(project_gid: str, section_names: Optional[List[str]] = None,
                    reorder: bool = False) -> Dict[str, str]:
    """
    Ensure standard sections exist in a project. Creates any that are missing.
    If reorder=True, also reorders sections to match the canonical order.
    Returns {name: gid} for all requested sections.
    """
    if section_names is None:
        cfg = _load_tag_config()
        section_names = cfg.get("sections", ["Backlog", "Watch", "To Do", "Done", "Waiting on Someone Else"])

    existing = list_sections(project_gid)
    existing_lower = {k.lower().strip(): (k, v) for k, v in existing.items()}

    result = {}  # type: Dict[str, str]
    for name in section_names:
        match = existing_lower.get(name.lower().strip())
        if match:
            result[name] = match[1]
        else:
            gid = create_section(project_gid, name)
            result[name] = gid

    if reorder:
        prev_gid = None
        for name in section_names:
            gid = result[name]
            reorder_section(project_gid, gid, insert_after=prev_gid)
            prev_gid = gid

    return result


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

def list_workspace_tags(workspace_gid: str) -> Dict[str, dict]:
    """
    Return {tag_name_lower: {gid, name, color}} for all workspace tags.
    Paginates through all results.
    """
    tags = {}  # type: Dict[str, dict]
    url = f"{ASANA_BASE}/workspaces/{workspace_gid}/tags"
    params = {"opt_fields": "name,color", "limit": 100}  # type: dict

    while url:
        resp = requests.get(url, headers=_get_headers(), params=params, timeout=15)
        resp.raise_for_status()
        body = resp.json()
        for t in body.get("data", []):
            tags[t["name"].lower().strip()] = {
                "gid": t["gid"],
                "name": t["name"],
                "color": t.get("color", "none"),
            }
        next_page = body.get("next_page")
        if next_page and next_page.get("uri"):
            url = next_page["uri"]
            params = {}  # URI already contains params
        else:
            url = None  # type: ignore[assignment]

    return tags


def ensure_tag(workspace_gid: str, name: str, color: str = "none",
               _cache: Optional[Dict[str, dict]] = None) -> str:
    """
    Find or create a tag by name. Returns the tag GID.
    Pass _cache (from list_workspace_tags) to avoid repeated API calls.
    """
    cache = _cache if _cache is not None else list_workspace_tags(workspace_gid)
    existing = cache.get(name.lower().strip())
    if existing:
        return existing["gid"]

    # Create new tag
    resp = requests.post(
        f"{ASANA_BASE}/tags",
        headers=_get_headers(),
        json={"data": {"name": name, "color": color, "workspace": workspace_gid}},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def add_tags_to_task(task_gid: str, tag_gids: List[str]) -> None:
    """Add multiple tags to a task."""
    for gid in tag_gids:
        requests.post(
            f"{ASANA_BASE}/tasks/{task_gid}/addTag",
            headers=_get_headers(),
            json={"data": {"tag": gid}},
            timeout=10,
        )


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search_tasks(workspace_gid: str, text: str, project_gid: Optional[str] = None) -> List[dict]:
    """
    Search for tasks by text. Used for dedup checks at the Asana level.
    Returns list of matching task dicts with gid and name.
    """
    params: dict = {
        "text": text,
        "is_subtask": False,
        "completed": False,
        "opt_fields": "name,completed,due_on",
    }
    if project_gid:
        params["projects.any"] = project_gid

    resp = requests.get(
        f"{ASANA_BASE}/workspaces/{workspace_gid}/tasks/search",
        headers=_get_headers(),
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])
