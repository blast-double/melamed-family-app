# `/add-task` Skill — Personal Asana Workspace

*Last Edited: 2026-03-27*

## Overview

Port the production `/add-task` skill from the Itero workspace to Aaron's personal Asana workspace. The skill lets Aaron or Eugenia add tasks to a shared family Asana workspace via natural language (e.g., `/add-task Pick up Mateo's heartworm meds by Friday`). Tasks are created with structured metadata via tags, sections, and formatted descriptions.

**Approach**: Direct port of the Itero system with simplifications — no Supabase audit trail, no company signal resolution, no confidence/disposition/triage logic. Semantic dedup via Gemini is retained.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Audit trail (Supabase) | Skipped | Unnecessary complexity for personal use; Asana is sole system of record |
| Semantic dedup | Kept | Prevents duplicate tasks; Gemini API key already configured |
| Assignee support | Built-in Asana field | No assignee tags — use Asana's native assignee (Aaron or Eugenia) |
| Custom fields | None | Free tier — all metadata encoded via tags, sections, and description |
| Fallback project | Home | Skill always asks which project; Home is the default if user says "just default it" |
| Tag taxonomy | Simplified | Project tags + priority + source + on-demand person tags. No type tags. |

## Asana Workspace

| Entity | GID |
|--------|-----|
| Workspace | `1213815286778073` |
| Team | `1213815286778075` |
| Aaron Melamed | `1213815286778061` |
| Eugenia Canul Celis | `1213827192025062` |

### Projects (7)

All projects to be created during setup. GIDs will be recorded in `config/project_routing.yaml` after creation.

| Project | Description |
|---------|-------------|
| Home | Household, maintenance, purchases, contractors |
| Travel | Trips, bookings, itineraries |
| Finance | Bills, taxes, insurance, investments |
| Social | Events, gifts, hosting |
| Health | Medical, insurance, appointments, prescriptions |
| Baby | Baby prep, pediatrician, gear, registry, childcare |
| Mateo | Vet visits, grooming, food, walks, training |

### Sections (same in every project, canonical order)

1. Backlog
2. Watch
3. To Do *(default)*
4. Done
5. Waiting on Someone Else

## Tag Taxonomy

### Project tags (auto-applied based on target project)

| Tag | Asana Color |
|-----|-------------|
| Home | dark-blue |
| Travel | dark-green |
| Finance | dark-orange |
| Social | dark-purple |
| Health | dark-teal |
| Baby | dark-pink |
| Mateo | dark-brown |

### Priority tags

| Tag | Asana Color |
|-----|-------------|
| Priority: High | light-red |
| Priority: Medium | light-orange |
| Priority: Low | light-warm-gray |

### Source tags

| Tag | Asana Color |
|-----|-------------|
| Source: Manual | light-blue |

### Person tags

- Created on-demand when a task references a specific vendor, doctor, contact, etc.
- Default color: `light-teal`

## Skill Workflow

### Step 1: Parse

Extract from natural language input:

| Field | Extraction Rule | Default |
|-------|----------------|---------|
| title | Action-verb-first task name | Required |
| project | Infer from keywords (e.g., "Mateo" → mateo, "flight" → travel, "doctor" → health) | Ask user |
| priority | "urgent"/"important" → high; "low"/"someday" → low | medium |
| due_date | Natural language → ISO date via `date_resolver.py` ("by Friday", "next week", "March 20") | None |
| section | "watch this" → Watch; "waiting on" → Waiting on Someone Else; "backlog" → Backlog | To Do |
| assignee | "Eugenia should..." → Eugenia GID; "I need to..." → Aaron GID | None (unassigned) |
| description | Any additional context provided by the user | None |

### Step 2: Confirm

Always ask which project, showing the inferred one as default:

```
Project: Mateo (change? Home / Travel / Finance / Social / Health / Baby)
Section: To Do (change? Backlog / Watch / Done / Waiting on Someone Else)
```

User can accept defaults or override. If project cannot be inferred, ask explicitly.

### Step 3: Execute

Run `create_manual_task.py`:

1. Resolve project → Asana GID via `project_routing.yaml`
2. Build structured description + resolve tag GIDs via `task_classifier.py`
3. Run dedup check via `dedup.py` (keyword filter + Gemini semantic match)
4. If duplicate found (confidence >= 0.8) → update existing task with new context
5. If no duplicate → create new Asana task with tags, section, due date, assignee

### Step 4: Report

```
Created: Pick up Mateo's heartworm meds
Project: Mateo | Section: To Do | Due: Mar 27
Tags: Mateo, Priority: Medium, Source: Manual
[View in Asana](https://app.asana.com/0/0/<task_gid>)
```

## Architecture

### File Structure

```
.claude/skills/add-task/
  SKILL.md                          # Skill definition (workflow + parsing rules)
  scripts/
    create_manual_task.py            # Entry point — orchestrates the flow

execution/taskops/
  asana_client.py                    # Asana REST API wrapper (copied from Itero)
  router.py                         # project key → Asana GID lookup (simplified)
  task_classifier.py                 # Builds description, resolves tags (adapted)
  dedup.py                          # Keyword filter + Gemini semantic match (copied from Itero)
  date_resolver.py                  # Natural language → ISO date (copied from Itero)

execution/utils/
  gemini_rest.py                    # Lightweight Gemini API client (copied from Itero)

config/
  project_routing.yaml              # 7 projects → Asana GIDs + workspace constants
  asana_tags.yaml                   # Tag taxonomy definition
  prompts/
    task_dedup.md                   # Gemini dedup prompt (copied from Itero)
```

### Modules: Copy vs. Adapt

**Copied verbatim from Itero** (no changes needed):

| Module | Lines | Why |
|--------|-------|-----|
| `asana_client.py` | 394 | Fully generic Asana REST wrapper |
| `dedup.py` | 120 | Project-agnostic dedup logic |
| `date_resolver.py` | 97 | Pure date math, no business logic |
| `gemini_rest.py` | 67 | Generic Gemini API client |
| `prompts/task_dedup.md` | 31 | Model-agnostic dedup prompt |

**Adapted for personal use**:

| Module | Changes |
|--------|---------|
| `router.py` | Strip signal resolution (email domains, Slack IDs, ADO orgs). Simple `project_key → GID` lookup + workspace constants. |
| `task_classifier.py` | Replace company references with project references. Add assignee support (Aaron/Eugenia GID). Remove Supabase fields. Simplify description template. |
| `create_manual_task.py` | Remove Supabase insert/update calls. Flow: route → classify → dedup → create/update → output JSON. |
| `SKILL.md` | Personal projects instead of companies. Assignee field added. Simplified confirmation. |

**Removed entirely**:

| Module | Reason |
|--------|--------|
| `supabase_rest.py` | No audit trail |
| Signal resolution in router | No email/Slack/ADO routing needed |
| Confidence/disposition/triage | Manual tasks always created |

### Task Description Template

```
Context: [user-provided or "Manual task — no additional context provided."]

---
Project: Mateo
Assignee: Aaron
Priority: Medium
Source: Manual
```

### Dedup Strategy

Same as Itero — designed for Asana free tier (no search API):

1. Extract up to 4 keywords from new task title (stop words excluded)
2. List all incomplete tasks in target project via `list_project_tasks`
3. Filter to tasks with keyword overlap in title
4. Fetch full task data (name, notes) for top 10 candidates
5. Send to Gemini 2.0 Flash with dedup prompt
6. If confidence >= 0.8 → return match (caller updates instead of creates)

## Environment Variables

Required in `.env`:

```
ASANA_PAT=2/...          # Already configured
GEMINI_API_KEY=AIza...   # Already configured
```

## Asana Setup Steps (Manual, Before Code)

These steps create the workspace structure that the code will reference:

1. Create 7 projects in the workspace (Home, Travel, Finance, Social, Health, Baby, Mateo)
2. Create standard sections in each project (Backlog, Watch, To Do, Done, Waiting on Someone Else)
3. Create tags per the taxonomy (7 project tags, 3 priority tags, 1 source tag)
4. Record all project GIDs into `config/project_routing.yaml`

The implementation scripts can automate steps 1-3 via the Asana API, then record the GIDs.

## Free Tier Constraints

- No custom fields — metadata lives in tags and structured description
- No Asana search API — dedup uses `list_project_tasks` + Gemini
- No rules/automations — all logic lives in the skill + Python scripts
- No portfolios/goals — not needed for this use case
- 10 user limit — only 2 users (Aaron + Eugenia)
