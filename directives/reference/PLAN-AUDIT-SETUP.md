# Plan-Audit Loop: Setup Guide

Step-by-step instructions to add the plan-audit convergence loop to any project. Two AI agents — a planner and an auditor — iterate on implementation plans adversarially until both sides genuinely agree.

---

## 1. Prerequisites

### Option A: Claude Code Native (no external dependencies)

```bash
# Claude Code (both planner and auditor)
npm i -g @anthropic-ai/claude-code
claude login
```

### Option B: Claude + Codex (cross-model diversity)

```bash
# Claude Code (planner)
npm i -g @anthropic-ai/claude-code
claude login

# OpenAI Codex CLI (auditor)
npm i -g @openai/codex
codex login --device-auth     # bills against ChatGPT subscription
```

Verify:

```bash
claude --version
codex login status          # should say "Logged in using ChatGPT"
```

Configure Codex model + reasoning in `~/.codex/config.toml`:

```toml
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
```

---

## 2. Three Available Commands

| Command | Auditor | Plans from | Rounds | Use case |
|---------|---------|------------|--------|----------|
| `/plan-audit-cc` | Claude subagent (Task tool) | Existing plan (auto-grabs latest) | 8 | Self-contained in Claude Code. No external deps. |
| `/plan-audit-loop` | Codex CLI (gpt-5.4) | Scratch (TASK.md or text) | 12 | Cross-model diversity. Different blind spots. |
| `/plan-audit` | One-shot skill | N/A | 1 | Quick single-pass review, no multi-round loop. |

---

## 3. Create File Structure

From your project root:

```bash
mkdir -p prompts .claude/commands .tmp/plan-audit
```

You'll create these files:

```
prompts/planner.md                    # Planner system prompt
prompts/auditor.md                    # Auditor system prompt
.claude/commands/plan-audit-cc.md     # Claude Code Native slash command
.claude/commands/plan-audit-loop.md   # Claude + Codex slash command (optional)
TASK.md                               # Task template (gitignored)
.tmp/plan-audit/                      # Work directory for round files + ledger
```

Optional extras:
```
scripts/plan-audit.sh                 # Standalone bash script (terminal)
.vscode/tasks.json                    # VS Code task runner
```

---

## 4. Create Each File

### 4a. `prompts/planner.md`

System prompt that tells the planner how to structure plans and defend decisions.

See the actual file for the full implementation. Key features:

- **8 required plan sections**: Summary, Architecture, Implementation Steps, Database Changes, API Changes, Testing Strategy, Rollout Plan, Error Handling
- **ID-based finding references**: Findings are referenced by ID and title (e.g., "F3: Migration has no rollback")
- **Defense Protocol**: ACCEPTED (with visible plan change) or DISPUTED (with concrete evidence)
- **Output Efficiency**: Round 1 outputs full plan; Round 2+ outputs only Audit Response + Delta Summary, writes full plan to file
- **Convergence Signal**: `<plan-ready/>` tag when the planner stands behind the plan

### 4b. `prompts/auditor.md`

System prompt for the auditor. Defines the finding schema, severity model, dispute handling, and convergence signal.

See the actual file for the full implementation. Key features:

- **Finding Eligibility Gate**: Only emit findings for production failure risk, delivery reliability impact, or meaningful complexity cost
- **Severity Model**: Critical (blocker), Significant (non-blocking), Minor (cumulative only)
- **Finding Ledger integration**: Receives ledger each round, references findings by stable ID, respects RESOLVED/DROPPED statuses
- **Scope Boundary (Round 3+)**: New findings must be directly caused by plan changes (prevents scope creep)
- **Convergence Ratchet**: Cannot re-raise RESOLVED or DROPPED findings unless planner's fix caused a demonstrable regression
- **Advisory Notes**: Scope-adjacent observations that don't affect verdict (no severity markers)
- **Dispute handling**: DROPPED / SUSTAINED / DOWNGRADED with specific rebuttals
- **Prompt trimming**: `<!-- BEGIN_TRIM_R3 -->` / `<!-- END_TRIM_R3 -->` markers allow stripping examples after Round 2 to save tokens
- **Convergence Signal**: `<plan-approved/>` tag on genuine Pass verdict

### 4c. `.claude/commands/plan-audit-cc.md` (Claude Code Native)

See the actual file for the full implementation. Key features:

- **Auditor**: Claude subagent via Task tool (`subagent_type: "Plan"`)
- **Input**: Defaults to latest plan in `~/.claude/plans/` (no arguments needed)
- **MAX_ROUNDS**: 8
- **File naming**: `{plan-name}_plan_round_N.md` (plan-name prefix, no collisions)
- **Scoring**: 4-point scale with advancement bonus
- **Finding Ledger**: Tracks findings with stable IDs across rounds
- **Regression**: Double regression guard (pauses after 2 consecutive regressions)
- **Prompt trimming**: Strips auditor examples after Round 2 to save tokens
- **Zero external dependencies** — runs entirely within Claude Code

### 4d. `.claude/commands/plan-audit-loop.md` (Claude + Codex)

See the actual file for the full implementation. Key features:

- **Auditor**: Codex CLI (`codex exec --full-auto --ephemeral -m gpt-5.4`)
- **Input**: Task description from `$ARGUMENTS`, file path, or `TASK.md` (plans from scratch)
- **MAX_ROUNDS**: 12
- **File naming**: `plan_round_N.md` (no prefix)
- **Scoring**: 3-point scale (simplified)
- **Finding Ledger**: Tracks findings with stable IDs across rounds
- **Requires**: Codex CLI installed + authenticated

### 4e. `TASK.md` (template for `/plan-audit-loop`)

```markdown
# Task: [Title]

## Objective
[What needs to be built or changed, and why]

## Context
[Background: related systems, current behavior, what prompted this task]

## Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Constraints
- [Technical constraints: languages, frameworks, compatibility]
- [Timeline constraints]
- [Budget or resource constraints]

## Out of Scope
- [What this task explicitly does NOT include]

## Acceptance Criteria
- [ ] [Criterion 1: specific, testable condition]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## References
- [Links to PRDs, design docs, existing code, related issues]
```

### 4f. `.gitignore` additions

```
# Plan-audit transient outputs
TASK.md
PLAN_FINAL*.md
PLAN_AUDIT_LOG*.md
FINDING_LEDGER*.md
*_plan_round_*.md
*_audit_round_*.md
.tmp/
```

---

## 5. How It Works

```
┌─────────────────────────────────────────────────┐
│                  ROUND N                        │
│                                                 │
│  ┌──────────┐         ┌──────────┐              │
│  │  Planner  │──plan──▶│  Auditor │              │
│  │ (Claude)  │◀─audit──│(subagent │              │
│  │           │         │ or Codex)│              │
│  └──────────┘         └──────────┘              │
│       │                    │                    │
│  <plan-ready/>?    <plan-approved/>?             │
│       │                    │                    │
│       └───── BOTH? ────────┘                    │
│              │                                  │
│         CONVERGED                               │
└─────────────────────────────────────────────────┘
```

### Bilateral Convergence
The loop only stops when **both** signals appear in the same round:
- Planner emits `<plan-ready/>` — "I stand behind this plan"
- Auditor emits `<plan-approved/>` — "No material findings remain"

### Inline Defense
The planner doesn't blindly accept every finding:
- **ACCEPTED** — incorporates the fix, shows the plan change
- **DISPUTED** — defends the original decision with evidence

The auditor must respond to each dispute:
- **DROPPED** — planner was right, finding removed
- **SUSTAINED** — risk is real, rebuttal provided
- **DOWNGRADED** — partially valid, severity lowered

### Quality Trajectory
Each round logs finding counts. Warnings are printed for regressions (more findings than the previous round).

---

## 6. Typical Workflows

### Workflow A: Plan in Claude Code, audit in same window

1. Plan interactively with Claude in VS Code
2. Claude saves plan to `~/.claude/plans/`
3. Run `/plan-audit-cc` — auto-grabs latest plan, audits via subagent
4. Converged plan is at `.tmp/plan-audit/PLAN_FINAL_{plan-name}.md`
5. Implement from the plan

### Workflow B: Plan + audit from scratch with Codex

1. Write a task description in `TASK.md`
2. Run `/plan-audit-loop` — Claude generates plan, Codex audits
3. Multi-round convergence loop runs autonomously
4. Converged plan is at `PLAN_FINAL.md`

### Workflow C: Quick one-shot audit

1. Have a plan already written
2. Run `/plan-audit` — single-pass review, no multi-round loop
3. Get findings immediately

---

## 7. Output Files

### `/plan-audit-cc` outputs (plan-name prefixed)

| File | Description |
|------|-------------|
| `PLAN_FINAL_{plan-name}.md` | The approved or best-effort final plan |
| `PLAN_AUDIT_LOG_{plan-name}.md` | Every round's plan + audit + quality trajectory |
| `FINDING_LEDGER_{plan-name}.md` | Finding tracker with stable IDs and statuses across rounds |
| `{plan-name}_plan_round_N.md` | Individual round plans |
| `{plan-name}_audit_round_N.md` | Individual round audits |

### `/plan-audit-loop` outputs (no prefix)

| File | Description |
|------|-------------|
| `PLAN_FINAL.md` | The approved or best-effort final plan |
| `PLAN_AUDIT_LOG.md` | Every round's plan + audit + quality trajectory |
| `FINDING_LEDGER.md` | Finding tracker with stable IDs and statuses across rounds |
| `plan_round_N.md` | Individual round plans |
| `audit_round_N.md` | Individual round audits |

All output files go to `.tmp/plan-audit/`.

---

## 8. Scoring

### `/plan-audit-cc` (4-point scale)

**Base score** (when did it converge?):

| Rounds to converge | Points |
|---------------------|--------|
| 1-3                 | 3      |
| 4-6                 | 2      |
| 7-8 or max rounds   | 1      |
| Max rounds + Fail   | 0      |

**Advancement bonus** (+0.5 each, cumulative):
- +0.5 if the plan moved from Fail → Pass with Significant Risks
- +0.5 if the plan moved from Pass with Significant Risks → Pass

### `/plan-audit-loop` (3-point scale)

| Rounds to converge | Points |
|---------------------|--------|
| 1-3                 | 3      |
| 4-6                 | 2      |
| 7-9                 | 1      |
| 10-12 or no convergence | 0  |

---

## 9. Customization

| What | Where | Notes |
|------|-------|-------|
| Max rounds (CC) | `MAX_ROUNDS` in `plan-audit-cc.md` | Default 8 |
| Max rounds (Codex) | `MAX_ROUNDS` in `plan-audit-loop.md` | Default 12 |
| Auditor model (Codex) | `CODEX_CMD` in command | Default `gpt-5.4` |
| Plan sections | `prompts/planner.md` | Add/remove sections to match your project |
| Audit strictness | `prompts/auditor.md` | Tighten the eligibility gate or severity model |
| Reasoning effort | `~/.codex/config.toml` | `model_reasoning_effort = "xhigh"` |

Prompts are loaded fresh each round, so edits take effect immediately without restarting.
