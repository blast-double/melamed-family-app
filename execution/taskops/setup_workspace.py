#!/usr/bin/env python3
# Last Edited: 2026-03-27 00:00
"""
One-time Asana workspace setup script.

Creates projects, sections, and tags for the personal task system.
Outputs GIDs in YAML format to paste into config/project_routing.yaml.

Usage:
    python3 execution/taskops/setup_workspace.py
"""
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from dotenv import load_dotenv
load_dotenv(WORKSPACE_ROOT / ".env")

import yaml
from execution.taskops.asana_client import (
    create_project,
    ensure_sections,
    ensure_tag,
    list_workspace_tags,
)

# Workspace constants
WORKSPACE_GID = "1213815286778073"
TEAM_GID = "1213815286778075"

PROJECTS = {
    "home": {"name": "Home", "notes": "Household tasks, maintenance, purchases, contractors", "color": "dark-blue"},
    "travel": {"name": "Travel", "notes": "Trips, bookings, itineraries", "color": "dark-green"},
    "finance": {"name": "Finance", "notes": "Bills, taxes, insurance, investments", "color": "dark-orange"},
    "social": {"name": "Social", "notes": "Events, gifts, hosting", "color": "dark-purple"},
    "health": {"name": "Health", "notes": "Medical, insurance, appointments, prescriptions", "color": "dark-teal"},
    "baby": {"name": "Baby", "notes": "Baby prep, pediatrician, gear, registry, childcare", "color": "dark-pink"},
    "mateo": {"name": "Mateo", "notes": "Vet visits, grooming, food, walks, training", "color": "dark-brown"},
}

SECTIONS = ["Backlog", "Watch", "To Do", "Done", "Waiting on Someone Else"]

TAGS = {
    "Home": "dark-blue",
    "Travel": "dark-green",
    "Finance": "dark-orange",
    "Social": "dark-purple",
    "Health": "dark-teal",
    "Baby": "dark-pink",
    "Mateo": "dark-brown",
    "Priority: High": "light-red",
    "Priority: Medium": "light-orange",
    "Priority: Low": "light-warm-gray",
    "Source: Manual": "light-blue",
}


def main():
    print("=== Personal Asana Workspace Setup ===\n")

    # 1. Create projects
    print("Creating projects...")
    project_gids = {}
    for key, spec in PROJECTS.items():
        print(f"  Creating: {spec['name']}...", end=" ")
        gid = create_project(
            workspace_gid=WORKSPACE_GID,
            name=spec["name"],
            team_gid=TEAM_GID,
            notes=spec["notes"],
            color=spec["color"],
        )
        project_gids[key] = gid
        print(f"GID: {gid}")

    # 2. Create sections in each project
    print("\nCreating sections...")
    for key, gid in project_gids.items():
        print(f"  {PROJECTS[key]['name']}: ", end="")
        ensure_sections(gid, SECTIONS, reorder=True)
        print("OK")

    # 3. Create tags
    print("\nCreating tags...")
    tag_cache = list_workspace_tags(WORKSPACE_GID)
    for name, color in TAGS.items():
        print(f"  {name}: ", end="")
        tag_gid = ensure_tag(WORKSPACE_GID, name, color, _cache=tag_cache)
        tag_cache[name.lower().strip()] = {"gid": tag_gid, "name": name, "color": color}
        print(f"GID: {tag_gid}")

    # 4. Output YAML for project_routing.yaml
    print("\n=== Copy this into config/project_routing.yaml ===\n")
    routing = {"projects": {}}
    for key, gid in project_gids.items():
        routing["projects"][key] = {
            "display_name": PROJECTS[key]["name"],
            "description": PROJECTS[key]["notes"],
            "asana_gid": gid,
        }
    routing["fallback_project"] = "home"
    routing["asana"] = {
        "workspace_gid": WORKSPACE_GID,
        "team_gid": TEAM_GID,
        "aaron_gid": "1213815286778061",
        "eugenia_gid": "1213827192025062",
    }

    print("# Project Routing Table")
    print("# Last Updated: 2026-03-27")
    print(yaml.dump(routing, default_flow_style=False, sort_keys=False))

    print("=== Setup complete! ===")


if __name__ == "__main__":
    main()
