# Last Edited: 2026-03-26 00:00
"""
Project routing: resolves project keys to Asana project GIDs.

Simplified from Itero's company router — no signal resolution needed.
Just project_key → GID lookup + workspace constants.
"""
import os
from pathlib import Path
from functools import lru_cache
from typing import Dict, List

import yaml


def _find_config_path() -> Path:
    """Locate project_routing.yaml relative to workspace root."""
    candidates = [
        Path(__file__).parent.parent.parent / "config" / "project_routing.yaml",
        Path(os.getenv("WORKSPACE_ROOT", "")) / "config" / "project_routing.yaml",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("config/project_routing.yaml not found")


@lru_cache(maxsize=1)
def _load_config() -> dict:
    """Load and cache the routing config."""
    with open(_find_config_path()) as f:
        return yaml.safe_load(f)


def get_project_gid(project_key: str) -> str:
    """Resolve a project key to its Asana project GID.

    Falls back to the configured fallback_project if key not found.
    """
    cfg = _load_config()
    projects = cfg.get("projects", {})
    key = project_key.lower().strip()

    if key in projects:
        return projects[key]["asana_gid"]

    fallback = cfg.get("fallback_project", "home")
    return projects.get(fallback, {}).get("asana_gid", "")


def get_asana_constants() -> dict:
    """Return workspace_gid, team_gid, aaron_gid, eugenia_gid."""
    return _load_config().get("asana", {})


def get_project_descriptions() -> Dict[str, str]:
    """Return {project_key: description} for use in LLM prompts."""
    cfg = _load_config()
    return {
        key: proj.get("description", proj.get("display_name", key))
        for key, proj in cfg.get("projects", {}).items()
    }


def list_project_keys() -> List[str]:
    """Return all configured project keys."""
    return list(_load_config().get("projects", {}).keys())
