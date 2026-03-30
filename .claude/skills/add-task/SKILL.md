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
