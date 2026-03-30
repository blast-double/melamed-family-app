# `/add-task` Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the `/add-task` skill from the Itero workspace to Aaron's personal Asana workspace, creating tasks with structured tags, sections, descriptions, and semantic dedup.

**Architecture:** Direct port of the Itero task automation system with simplifications — no Supabase audit trail, no company signal routing, no confidence/triage logic. The skill parses natural language, confirms project/section, then creates/updates tasks via the Asana REST API. Semantic dedup via Gemini prevents duplicates.

**Tech Stack:** Python 3.10+, Asana REST API (PAT auth), Gemini 2.0 Flash (dedup), PyYAML, requests, python-dotenv

**Spec:** `docs/superpowers/specs/2026-03-27-add-task-skill-design.md`

**Itero source (reference):** `/Users/aaronmelamed/Dropbox/antigravity/workspaces/Itero/`

---

## File Structure

```
# New files:
config/asana_tags.yaml                              # Tag taxonomy (project, priority, source, person)
config/project_routing.yaml                         # 7 projects → Asana GIDs + workspace constants
config/prompts/task_dedup.md                        # Gemini dedup prompt

execution/taskops/__init__.py                       # Package init
execution/taskops/asana_client.py                   # Asana REST API wrapper (from Itero, one change)
execution/taskops/router.py                         # project key → GID lookup (simplified from Itero)
execution/taskops/task_classifier.py                # Build description + resolve tags (adapted from Itero)
execution/taskops/dedup.py                          # Keyword filter + Gemini semantic match (from Itero)
execution/taskops/date_resolver.py                  # "by Friday" → ISO date (from Itero)
execution/taskops/setup_workspace.py                # One-time: create projects/sections/tags in Asana

execution/utils/gemini_rest.py                      # Lightweight Gemini API client (from Itero)

.claude/skills/add-task/SKILL.md                    # Skill definition
.claude/skills/add-task/scripts/create_manual_task.py  # Entry point script

tests/taskops/__init__.py                           # Test package
tests/taskops/test_router.py                        # Router unit tests
tests/taskops/test_classifier.py                    # Classifier unit tests
tests/taskops/test_date_resolver.py                 # Date resolver unit tests

# Modified files:
requirements.txt                                    # Add requests, pyyaml
```

---

### Task 1: Dependencies + Package Structure

**Files:**
- Modify: `requirements.txt`
- Create: `execution/taskops/__init__.py`
- Create: `tests/taskops/__init__.py`

- [ ] **Step 1: Update requirements.txt**

Add `requests` and `pyyaml` to the existing `requirements.txt`:

```
requests>=2.31.0
PyYAML>=6.0
```

Append these two lines after the existing dependencies. Do NOT remove existing entries.

- [ ] **Step 2: Create taskops package**

Create the file `execution/taskops/__init__.py` with empty content (just the package marker).

- [ ] **Step 3: Create test package**

Create the file `tests/taskops/__init__.py` with empty content.

- [ ] **Step 4: Install dependencies**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && pip install -r requirements.txt`
Expected: Successfully installed (or already satisfied) for all packages.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt execution/taskops/__init__.py tests/taskops/__init__.py
git commit -m "chore: add taskops package structure and dependencies for add-task skill"
```

---

### Task 2: Config Files

**Files:**
- Create: `config/asana_tags.yaml`
- Create: `config/project_routing.yaml`
- Create: `config/prompts/task_dedup.md`

- [ ] **Step 1: Create asana_tags.yaml**

Create `config/asana_tags.yaml`:

```yaml
# Asana tag taxonomy and section definitions
# Used by: execution/taskops/asana_client.py, task_classifier.py
# Last Updated: 2026-03-27

categories:
  project:
    tags:
      Home: dark-blue
      Travel: dark-green
      Finance: dark-orange
      Social: dark-purple
      Health: dark-teal
      Baby: dark-pink
      Mateo: dark-brown

  priority:
    tags:
      "Priority: High": light-red
      "Priority: Medium": light-orange
      "Priority: Low": light-warm-gray

  source:
    tags:
      "Source: Manual": light-blue

  person:
    # Person tags are created on-demand for vendors, doctors, contacts
    default_color: light-teal

# Standard sections for every Asana project (canonical order)
sections:
  - "Backlog"
  - "Watch"
  - "To Do"
  - "Done"
  - "Waiting on Someone Else"

default_section: "To Do"
```

- [ ] **Step 2: Create project_routing.yaml (template with placeholder GIDs)**

Create `config/project_routing.yaml`:

```yaml
# Project Routing Table
# Maps project keys to Asana project GIDs.
# Used by: execution/taskops/router.py
# Last Updated: 2026-03-27
#
# GIDs are populated by running: python3 execution/taskops/setup_workspace.py

projects:
  home:
    display_name: "Home"
    description: "Household tasks, maintenance, purchases, contractors"
    asana_gid: "PLACEHOLDER"

  travel:
    display_name: "Travel"
    description: "Trips, bookings, itineraries"
    asana_gid: "PLACEHOLDER"

  finance:
    display_name: "Finance"
    description: "Bills, taxes, insurance, investments"
    asana_gid: "PLACEHOLDER"

  social:
    display_name: "Social"
    description: "Events, gifts, hosting"
    asana_gid: "PLACEHOLDER"

  health:
    display_name: "Health"
    description: "Medical, insurance, appointments, prescriptions"
    asana_gid: "PLACEHOLDER"

  baby:
    display_name: "Baby"
    description: "Baby prep, pediatrician, gear, registry, childcare"
    asana_gid: "PLACEHOLDER"

  mateo:
    display_name: "Mateo"
    description: "Vet visits, grooming, food, walks, training"
    asana_gid: "PLACEHOLDER"

fallback_project: home

asana:
  workspace_gid: "1213815286778073"
  team_gid: "1213815286778075"
  aaron_gid: "1213815286778061"
  eugenia_gid: "1213827192025062"
```

- [ ] **Step 3: Create task_dedup.md prompt**

Create directory `config/prompts/` then create `config/prompts/task_dedup.md`:

```markdown
# Task Deduplication Prompt

You are a task deduplication engine. Given a NEW task and a list of EXISTING tasks
from the same Asana project, determine if the new task is the same logical work item
as any existing one — i.e., the same task discussed again in a later meeting or entered
manually a second time.

## Input

NEW task:
- Title: "{new_title}"
- Context: "{new_context}"

EXISTING tasks in the project:
{existing_tasks}

## Rules

1. Match on **semantic equivalence**, not exact text overlap.
   - "Set up CI pipeline for auth service" and "Configure GitHub Actions for authentication module" → SAME task.
   - "Review PR #42" and "Review PR #58" → DIFFERENT tasks.
2. Two tasks that mention the same topic but describe different work are NOT a match.
   - "Write unit tests for billing" and "Fix billing calculation bug" → DIFFERENT tasks.
3. Ignore differences in phrasing, verb form, or level of detail.
4. Only return a match if you are confident (>= 0.8) they are the same logical work item.

## Output

Return exactly one JSON object (no markdown fencing):

{"match_gid": "<gid of matching existing task>" or null, "confidence": <0.0-1.0>, "reason": "<one sentence>"}
```

- [ ] **Step 4: Commit**

```bash
git add config/asana_tags.yaml config/project_routing.yaml config/prompts/task_dedup.md
git commit -m "feat: add config files for personal Asana task system"
```

---

### Task 3: Verbatim Modules (Asana Client, Gemini, Date Resolver, Dedup)

**Files:**
- Create: `execution/utils/gemini_rest.py`
- Create: `execution/taskops/asana_client.py`
- Create: `execution/taskops/date_resolver.py`
- Create: `execution/taskops/dedup.py`

These are copied from the Itero workspace. The Asana client gets one change: `create_task` should NOT auto-assign when no assignee is given (personal tasks default to unassigned).

- [ ] **Step 1: Copy gemini_rest.py verbatim**

Copy from Itero: `/Users/aaronmelamed/Dropbox/antigravity/workspaces/Itero/execution/utils/gemini_rest.py`
To: `execution/utils/gemini_rest.py`

The file is 67 lines. Copy it exactly as-is — no changes needed. The import paths and API patterns are workspace-agnostic.

- [ ] **Step 2: Copy asana_client.py with one modification**

Copy from Itero: `/Users/aaronmelamed/Dropbox/antigravity/workspaces/Itero/execution/taskops/asana_client.py`
To: `execution/taskops/asana_client.py`

**One change required** in the `create_task` function (lines 77-84 in Itero). Replace the auto-assign block:

```python
    if not assignee_gid:
        assignee_gid = os.getenv("ASANA_USER_GID", "1206320669440361")

    data: dict = {
        "name": name,
        "projects": [project_gid],
        "assignee": assignee_gid,
    }
```

With:

```python
    data: dict = {
        "name": name,
        "projects": [project_gid],
    }
    if assignee_gid:
        data["assignee"] = assignee_gid
```

This makes tasks unassigned by default (per spec). The caller (create_manual_task.py) passes the assignee GID explicitly when needed.

Everything else in the file (394 lines) stays exactly the same.

- [ ] **Step 3: Copy date_resolver.py verbatim**

Copy from Itero: `/Users/aaronmelamed/Dropbox/antigravity/workspaces/Itero/execution/taskops/date_resolver.py`
To: `execution/taskops/date_resolver.py`

97 lines. Copy exactly as-is — pure date math with no workspace-specific logic.

- [ ] **Step 4: Copy dedup.py verbatim**

Copy from Itero: `/Users/aaronmelamed/Dropbox/antigravity/workspaces/Itero/execution/taskops/dedup.py`
To: `execution/taskops/dedup.py`

120 lines. Copy exactly as-is. The import paths (`execution.taskops.asana_client`, `execution.utils.gemini_rest`) match the personal workspace package structure. The `WORKSPACE_ROOT` path resolution (`Path(__file__).parent.parent.parent`) resolves correctly to the personal workspace root.

- [ ] **Step 5: Verify imports resolve**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -c "from execution.taskops.date_resolver import resolve_deadline; print(resolve_deadline('tomorrow'))"`

Expected: Tomorrow's date in ISO format (e.g., `2026-03-28`).

- [ ] **Step 6: Commit**

```bash
git add execution/utils/gemini_rest.py execution/taskops/asana_client.py execution/taskops/date_resolver.py execution/taskops/dedup.py
git commit -m "feat: add core taskops modules (asana client, dedup, date resolver, gemini)"
```

---

### Task 4: Adapted Router + Tests

**Files:**
- Create: `execution/taskops/router.py`
- Create: `tests/taskops/test_router.py`

The Itero router (128 lines) has signal resolution for email domains, Slack workspaces, and ADO orgs. The personal version strips all of that — just project key → GID lookup.

- [ ] **Step 1: Write failing router tests**

Create `tests/taskops/test_router.py`:

```python
"""Tests for personal project router."""
import pytest
from unittest.mock import patch

# Mock config that mirrors the real project_routing.yaml structure
MOCK_CONFIG = {
    "projects": {
        "home": {
            "display_name": "Home",
            "description": "Household tasks",
            "asana_gid": "111111",
        },
        "travel": {
            "display_name": "Travel",
            "description": "Trips and bookings",
            "asana_gid": "222222",
        },
        "health": {
            "display_name": "Health",
            "description": "Medical stuff",
            "asana_gid": "333333",
        },
    },
    "fallback_project": "home",
    "asana": {
        "workspace_gid": "ws_111",
        "team_gid": "team_111",
        "aaron_gid": "aaron_111",
        "eugenia_gid": "eugenia_111",
    },
}


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear lru_cache between tests."""
    from execution.taskops import router
    router._load_config.cache_clear()
    yield
    router._load_config.cache_clear()


@patch("execution.taskops.router._load_config", return_value=MOCK_CONFIG)
class TestRouter:
    def test_get_project_gid_valid(self, mock_cfg):
        from execution.taskops.router import get_project_gid
        assert get_project_gid("travel") == "222222"

    def test_get_project_gid_fallback(self, mock_cfg):
        from execution.taskops.router import get_project_gid
        assert get_project_gid("nonexistent") == "111111"

    def test_get_project_gid_case_insensitive(self, mock_cfg):
        from execution.taskops.router import get_project_gid
        assert get_project_gid("Health") == "333333"

    def test_get_asana_constants(self, mock_cfg):
        from execution.taskops.router import get_asana_constants
        constants = get_asana_constants()
        assert constants["workspace_gid"] == "ws_111"
        assert constants["aaron_gid"] == "aaron_111"
        assert constants["eugenia_gid"] == "eugenia_111"

    def test_get_project_descriptions(self, mock_cfg):
        from execution.taskops.router import get_project_descriptions
        descs = get_project_descriptions()
        assert descs["home"] == "Household tasks"
        assert descs["travel"] == "Trips and bookings"

    def test_list_project_keys(self, mock_cfg):
        from execution.taskops.router import list_project_keys
        keys = list_project_keys()
        assert "home" in keys
        assert "travel" in keys
        assert "health" in keys
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m pytest tests/taskops/test_router.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'execution.taskops.router'` or `ImportError: cannot import name 'get_project_gid'`

- [ ] **Step 3: Write router.py**

Create `execution/taskops/router.py`:

```python
# Last Edited: 2026-03-27 00:00
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

    # Fallback
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m pytest tests/taskops/test_router.py -v`

Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add execution/taskops/router.py tests/taskops/test_router.py
git commit -m "feat: add project router with tests"
```

---

### Task 5: Asana Workspace Setup Script

**Files:**
- Create: `execution/taskops/setup_workspace.py`

One-time script that creates 7 projects with standard sections and all tags, then outputs GIDs for `project_routing.yaml`.

- [ ] **Step 1: Write setup_workspace.py**

Create `execution/taskops/setup_workspace.py`:

```python
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

# Workspace constants (from earlier API calls)
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
    # Project tags
    "Home": "dark-blue",
    "Travel": "dark-green",
    "Finance": "dark-orange",
    "Social": "dark-purple",
    "Health": "dark-teal",
    "Baby": "dark-pink",
    "Mateo": "dark-brown",
    # Priority tags
    "Priority: High": "light-red",
    "Priority: Medium": "light-orange",
    "Priority: Low": "light-warm-gray",
    # Source tags
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

    # Add YAML header comment
    print("# Project Routing Table")
    print("# Last Updated: 2026-03-27")
    print(yaml.dump(routing, default_flow_style=False, sort_keys=False))

    print("=== Setup complete! ===")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the setup script**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 execution/taskops/setup_workspace.py`

Expected: Creates 7 projects, sections, and tags in Asana. Outputs YAML with real GIDs.

**IMPORTANT**: Copy the YAML output and save it — you need it for the next task.

- [ ] **Step 3: Verify in Asana**

Open [app.asana.com](https://app.asana.com/) and confirm:
- 7 projects visible (Home, Travel, Finance, Social, Health, Baby, Mateo)
- Each project has 5 sections (Backlog, Watch, To Do, Done, Waiting on Someone Else)
- Tags visible in workspace

- [ ] **Step 4: Commit**

```bash
git add execution/taskops/setup_workspace.py
git commit -m "feat: add one-time Asana workspace setup script"
```

---

### Task 6: Record Real GIDs in Config

**Files:**
- Modify: `config/project_routing.yaml`

- [ ] **Step 1: Update project_routing.yaml with real GIDs**

Replace every `"PLACEHOLDER"` in `config/project_routing.yaml` with the actual GIDs from the setup script output.

The file structure stays the same — just replace the `asana_gid` values for each project.

- [ ] **Step 2: Verify config loads**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -c "from execution.taskops.router import get_project_gid, list_project_keys; print('Projects:', list_project_keys()); print('Home GID:', get_project_gid('home'))"`

Expected: Lists all 7 project keys and prints a real GID (not "PLACEHOLDER") for home.

- [ ] **Step 3: Commit**

```bash
git add config/project_routing.yaml
git commit -m "feat: record Asana project GIDs from workspace setup"
```

---

### Task 7: Adapted Task Classifier + Tests

**Files:**
- Create: `execution/taskops/task_classifier.py`
- Create: `tests/taskops/test_classifier.py`

Adapted from Itero's 309-line classifier. Strips company/meeting logic, adds assignee support, uses project tags instead of company tags.

- [ ] **Step 1: Write failing classifier tests**

Create `tests/taskops/test_classifier.py`:

```python
"""Tests for personal task classifier."""
import pytest
from unittest.mock import patch, MagicMock

MOCK_TAG_CONFIG = {
    "categories": {
        "project": {
            "tags": {
                "Home": "dark-blue",
                "Travel": "dark-green",
                "Health": "dark-teal",
                "Mateo": "dark-brown",
            },
        },
        "priority": {
            "tags": {
                "Priority: High": "light-red",
                "Priority: Medium": "light-orange",
                "Priority: Low": "light-warm-gray",
            },
        },
        "source": {
            "tags": {
                "Source: Manual": "light-blue",
            },
        },
        "person": {
            "default_color": "light-teal",
        },
    },
}

MOCK_CONSTANTS = {
    "workspace_gid": "ws_test",
    "aaron_gid": "aaron_test",
    "eugenia_gid": "eugenia_test",
}


@patch("execution.taskops.task_classifier.list_workspace_tags", return_value={})
@patch("execution.taskops.task_classifier.ensure_tag", return_value="tag_gid_123")
@patch("execution.taskops.task_classifier.get_asana_constants", return_value=MOCK_CONSTANTS)
@patch("execution.taskops.task_classifier._load_tag_config", return_value=MOCK_TAG_CONFIG)
class TestClassifier:
    def test_basic_classify(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Buy groceries",
            "project": "home",
            "source": "manual",
        })
        assert result["title"] == "Buy groceries"
        assert result["section"] == "To Do"
        assert result["priority"] == "medium"
        assert "Context:" in result["description"]
        assert "Project: Home" in result["description"]

    def test_description_with_context(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Call vet",
            "project": "mateo",
            "context": "Annual checkup is overdue",
            "source": "manual",
        })
        assert "Annual checkup is overdue" in result["description"]
        assert "Project: Mateo" in result["description"]

    def test_description_no_context(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Something",
            "project": "home",
            "source": "manual",
        })
        assert "Manual task" in result["description"]

    def test_priority_high(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Urgent fix",
            "project": "home",
            "priority": "high",
            "source": "manual",
        })
        assert result["priority"] == "high"

    def test_assignee_aaron(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Do taxes",
            "project": "finance",
            "assignee": "aaron",
            "source": "manual",
        })
        assert result["assignee_gid"] == "aaron_test"
        assert "Assignee: Aaron" in result["description"]

    def test_assignee_eugenia(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Call doctor",
            "project": "health",
            "assignee": "eugenia",
            "source": "manual",
        })
        assert result["assignee_gid"] == "eugenia_test"
        assert "Assignee: Eugenia" in result["description"]

    def test_assignee_none(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Shared task",
            "project": "home",
            "source": "manual",
        })
        assert result["assignee_gid"] is None

    def test_tags_include_project_priority_source(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Walk Mateo",
            "project": "mateo",
            "priority": "low",
            "source": "manual",
        })
        tag_names = [t["name"] for t in result["tags"]]
        assert "Mateo" in tag_names
        assert "Priority: Low" in tag_names
        assert "Source: Manual" in tag_names

    def test_person_tag_hints(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Schedule cleaning",
            "project": "home",
            "source": "manual",
            "tag_hints": ["Maria (Cleaner)"],
        })
        tag_names = [t["name"] for t in result["tags"]]
        assert "Maria (Cleaner)" in tag_names
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m pytest tests/taskops/test_classifier.py -v`

Expected: FAIL — `ImportError: cannot import name 'classify' from 'execution.taskops.task_classifier'`

- [ ] **Step 3: Write task_classifier.py**

Create `execution/taskops/task_classifier.py`:

```python
# Last Edited: 2026-03-27 00:00
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


# ── Constants ────────────────────────────────────────────────────────────

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


# ── Helpers ───────────────────────────────────────────────────────────────

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


# ── Core ─────────────────────────────────────────────────────────────────

def classify(task: dict) -> dict:
    """Classify and enrich a raw task into Asana-ready structured output.

    Args:
        task: dict with keys:
            title (str, required)
            context (str, optional) — why this task exists
            project (str, required) — project key (home, travel, etc.)
            priority (str, optional, default medium) — high/medium/low
            due_date (str, optional) — ISO date
            source (str, required) — manual (only source for now)
            assignee (str, optional) — "aaron" or "eugenia"
            tag_hints (list[str], optional) — extra tag names (person tags, etc.)
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

    # ── Description ──────────────────────────────────────────────────
    description = _build_description(
        context=context,
        project=project,
        priority=priority,
        assignee_name=assignee_name,
        source=source,
    )

    # ── Tags ─────────────────────────────────────────────────────────
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


# ── Description Builder ──────────────────────────────────────────────────

def _build_description(
    context: str,
    project: str,
    priority: str,
    assignee_name: Optional[str],
    source: str,
) -> str:
    """Build a structured Asana task description."""
    parts = []

    # Context field — always present
    if context and context.strip():
        parts.append(f"Context: {context.strip()}")
    else:
        parts.append("Context: Manual task — no additional context provided.")
    parts.append("")

    # Separator before metadata
    parts.append("---")

    # Structured metadata
    project_display = PROJECT_DISPLAY.get(project.lower(), project.title())
    parts.append(f"Project: {project_display}")

    if assignee_name:
        parts.append(f"Assignee: {assignee_name}")

    priority_display = PRIORITY_TAGS.get(priority, "Medium").replace("Priority: ", "")
    parts.append(f"Priority: {priority_display}")

    source_label = SOURCE_TAG_MAP.get(source, f"Source: {source.title()}")
    parts.append(source_label)

    return "\n".join(parts)


# ── Tag Resolution ───────────────────────────────────────────────────────

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

    # Project tag
    project_name = PROJECT_DISPLAY.get(project.lower(), project.title())
    project_colors = categories.get("project", {}).get("tags", {})
    specs.append((project_name, project_colors.get(project_name, "none")))

    # Priority tag
    if priority and priority in PRIORITY_TAGS:
        priority_name = PRIORITY_TAGS[priority]
        priority_colors = categories.get("priority", {}).get("tags", {})
        specs.append((priority_name, priority_colors.get(priority_name, "light-orange")))

    # Source tag
    source_name = SOURCE_TAG_MAP.get(source, f"Source: {source.title()}")
    source_colors = categories.get("source", {}).get("tags", {})
    specs.append((source_name, source_colors.get(source_name, "light-warm-gray")))

    # Person / hint tags (on-demand)
    person_default = categories.get("person", {}).get("default_color", "light-teal")
    for hint in tag_hints:
        hint = hint.strip()
        if hint:
            specs.append((hint, person_default))

    return specs
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m pytest tests/taskops/test_classifier.py -v`

Expected: All 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add execution/taskops/task_classifier.py tests/taskops/test_classifier.py
git commit -m "feat: add personal task classifier with tests"
```

---

### Task 8: Date Resolver Tests

**Files:**
- Create: `tests/taskops/test_date_resolver.py`

Quick tests for the verbatim-copied date resolver to confirm it works in this workspace.

- [ ] **Step 1: Write date resolver tests**

Create `tests/taskops/test_date_resolver.py`:

```python
"""Tests for date resolver (copied from Itero — smoke tests)."""
from datetime import date
from execution.taskops.date_resolver import resolve_deadline


class TestDateResolver:
    def test_tomorrow(self):
        ref = date(2026, 3, 27)
        assert resolve_deadline("tomorrow", ref) == "2026-03-28"

    def test_today(self):
        ref = date(2026, 3, 27)
        assert resolve_deadline("today", ref) == "2026-03-27"

    def test_next_week(self):
        ref = date(2026, 3, 27)  # Friday
        assert resolve_deadline("next week", ref) == "2026-03-30"  # Monday

    def test_by_friday(self):
        ref = date(2026, 3, 23)  # Monday
        assert resolve_deadline("by Friday", ref) == "2026-03-27"

    def test_relative_days(self):
        ref = date(2026, 3, 27)
        assert resolve_deadline("3 days", ref) == "2026-03-30"

    def test_none_input(self):
        assert resolve_deadline(None) is None

    def test_empty_string(self):
        assert resolve_deadline("") is None

    def test_unrecognized(self):
        assert resolve_deadline("whenever") is None
```

- [ ] **Step 2: Run tests**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m pytest tests/taskops/test_date_resolver.py -v`

Expected: All 8 tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/taskops/test_date_resolver.py
git commit -m "test: add date resolver smoke tests"
```

---

### Task 9: Create Manual Task Script (Adapted)

**Files:**
- Create: `.claude/skills/add-task/scripts/create_manual_task.py`

Adapted from Itero's 167-line script. Removes all Supabase logic. Adds `--project` and `--assignee` flags.

- [ ] **Step 1: Create directory structure**

Run: `mkdir -p /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal/.claude/skills/add-task/scripts`

- [ ] **Step 2: Write create_manual_task.py**

Create `.claude/skills/add-task/scripts/create_manual_task.py`:

```python
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
```

- [ ] **Step 3: Verify script loads without errors**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 .claude/skills/add-task/scripts/create_manual_task.py --help`

Expected: Shows argparse help text with all flags (--title, --project, --priority, --section, --due, --assignee, --description, --tags).

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/add-task/scripts/create_manual_task.py
git commit -m "feat: add create_manual_task.py entry point (no Supabase, personal projects)"
```

---

### Task 10: SKILL.md

**Files:**
- Create: `.claude/skills/add-task/SKILL.md`

The skill definition that Claude reads when the user invokes `/add-task`.

- [ ] **Step 1: Write SKILL.md**

Create `.claude/skills/add-task/SKILL.md`:

````markdown
---
name: add-task
description: Add a task to the family Asana workspace from natural language. Parses title, project, priority, due date, assignee, and section, then creates in Asana with structured tags and description. Checks for duplicates before creating.
user-invocable: true
---

# Task — Manual Entry

Add a task to the personal/family Asana workspace from natural language. Fast: parse, confirm, create.

## Step 1: Parse the User's Request

Extract these fields from what the user said after `/add-task`:

| Field | Required | Default | Notes |
|---|---|---|---|
| title | yes | — | Action-verb-first (e.g., "Buy groceries", "Call pediatrician") |
| project | no | ask user | One of: home, travel, finance, social, health, baby, mateo |
| priority | no | medium | low/medium/high — look for "urgent"/"important" (→high), "low"/"someday" (→low) |
| due_date | no | null | Natural language ("by Friday", "next week", "March 20") → resolve to ISO date using today as reference |
| section | no | To Do | One of: Backlog, Watch, To Do, Done, Waiting on Someone Else |
| assignee | no | null | "aaron" or "eugenia" — infer from context (see below) |
| description | no | null | Any additional context the user provides |
| tags | no | null | Person tags — vendors, doctors, contacts mentioned by name |

**Project detection**: Infer from keywords in the user's text:
- **home** — "house", "apartment", "clean", "fix", "maintenance", "contractor", "furniture", "groceries", "cook"
- **travel** — "flight", "hotel", "trip", "vacation", "booking", "airbnb", "passport", "visa", "airport"
- **finance** — "tax", "bill", "insurance", "bank", "invest", "budget", "payment", "CPA", "accountant"
- **social** — "party", "dinner", "gift", "invite", "event", "friends", "host"
- **health** — "doctor", "appointment", "prescription", "dentist", "hospital", "insurance claim", "therapy"
- **baby** — "baby", "pediatrician", "nursery", "registry", "diaper", "stroller", "prenatal"
- **mateo** — "Mateo", "vet", "dog", "grooming", "heartworm", "kibble", "walk"

If project cannot be inferred, **always ask the user**.

**Section inference**:
- "watch this", "keep an eye on", "monitor" → **Watch**
- "waiting on", "blocked by", "need response from" → **Waiting on Someone Else**
- "backlog", "someday", "when I get to it" → **Backlog**
- Otherwise → **To Do** (default)

**Assignee inference**:
- "Eugenia should...", "Can Eugenia...", "for Eugenia" → **eugenia**
- "I need to...", "I should...", "remind me to..." → **aaron**
- If unclear → leave unassigned (null)

## Step 2: Confirm

Present a compact summary and ask the user to confirm:

```
Task: <title>
Project: <project> (change? home / travel / finance / social / health / baby / mateo)
Section: <section> (change? Backlog / Watch / To Do / Done / Waiting on Someone Else)
Priority: <priority>
Assignee: <assignee or "unassigned">
Due: <resolved ISO date or "none">
Notes: <description or "none">
```

**Always ask which project** — show the inferred one as the default. If project couldn't be inferred, ask explicitly with no default.

If the user confirms, proceed. If they want changes, adjust and re-confirm.

## Step 3: Execute

Resolve the due date to ISO format (YYYY-MM-DD) before calling the script. Use today as the reference date for relative phrases like "by Friday" or "next week".

```bash
python3 .claude/skills/add-task/scripts/create_manual_task.py \
  --title "<title>" \
  --project "<project_key>" \
  --priority "<low|medium|high>" \
  --section "<section>" \
  [--due "<YYYY-MM-DD>"] \
  [--assignee "<aaron|eugenia>"] \
  [--description "<description>"] \
  [--tags "<person tag 1>,<person tag 2>"]
```

Run from workspace root: `/Users/aaronmelamed/Dropbox/antigravity/workspaces/personal`

**Tags are auto-applied** by the script — project, priority, and source tags are added automatically. Only pass `--tags` for person tags (vendors, doctors, contacts).

The script automatically checks for duplicate tasks. If a semantically equivalent task exists, it updates the existing task instead of creating a new one.

## Step 4: Report

Show the result:
- Asana task link: `https://app.asana.com/0/0/<task_gid>`
- If `status` is `"created"`: show project, section, tags applied
- If `status` is `"updated"`: note which existing task was updated and its name

Format:
```
Created: <title>
Project: <project> | Section: <section> | Due: <date or "none">
Tags: <comma-separated tag names>
[View in Asana](<url>)
```

## Error Handling

| Error | Fix |
|---|---|
| ASANA_PAT not set | Check `.env` file has ASANA_PAT |
| "No Asana GID found" | Run `python3 execution/taskops/setup_workspace.py` to create projects |
| Asana 403 | Verify ASANA_PAT has write access to the workspace |
| GEMINI_API_KEY not set | Check `.env` file — needed for duplicate detection |

Never ask the user to create the task manually. Diagnose, fix, and retry.
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/add-task/SKILL.md
git commit -m "feat: add /add-task skill definition for personal Asana workspace"
```

---

### Task 11: End-to-End Test

**Files:** None created — this is a live integration test.

- [ ] **Step 1: Run all unit tests**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m pytest tests/taskops/ -v`

Expected: All tests pass (router: 6, classifier: 9, date_resolver: 8 = 23 total).

- [ ] **Step 2: Create a real task via the script**

Run:
```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 .claude/skills/add-task/scripts/create_manual_task.py \
  --title "Test task — delete me" \
  --project home \
  --priority low \
  --section "To Do" \
  --description "End-to-end test of the add-task skill"
```

Expected: JSON output with `"status": "created"`, a valid `asana_task_gid`, and `asana_url`.

- [ ] **Step 3: Verify in Asana**

Open the Asana URL from the output and confirm:
- Task appears in the **Home** project
- Task is in the **To Do** section
- Tags applied: **Home**, **Priority: Low**, **Source: Manual**
- Description has the structured format with Context and metadata

- [ ] **Step 4: Test dedup — create the same task again**

Run the same command again:
```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 .claude/skills/add-task/scripts/create_manual_task.py \
  --title "Test task — delete me" \
  --project home \
  --priority low \
  --section "To Do" \
  --description "Second attempt — should detect duplicate"
```

Expected: JSON output with `"status": "updated"` and the same `asana_task_gid` as step 2.

- [ ] **Step 5: Test assignee**

Run:
```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 .claude/skills/add-task/scripts/create_manual_task.py \
  --title "Test assignee task — delete me" \
  --project mateo \
  --priority medium \
  --assignee eugenia \
  --description "Testing assignee support"
```

Expected: Task created in Mateo project, assigned to Eugenia.

- [ ] **Step 6: Clean up test tasks**

Delete the test tasks from Asana (via UI or API). They served their purpose.

- [ ] **Step 7: Final commit**

```bash
git add -A
git commit -m "feat: complete /add-task skill for personal Asana workspace"
```
