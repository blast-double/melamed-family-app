---
name: review-pr
description: Reviews pull requests for correctness, security, performance, and adherence to project standards. Use when reviewing PRs, either by number or the current branch diff.
user-invocable: true
---

# PR Review Skill

Perform thorough, opinionated code reviews that catch real issues — not style nitpicks.

## Quick Start

```bash
# Review a specific PR by number
/review-pr 123

# Review the current branch against main
/review-pr
```

## Workflow

### Step 1: Gather Context

```bash
# If PR number provided:
gh pr view <number> --json title,body,files,additions,deletions,baseRefName,headRefName,commits
gh pr diff <number>

# If no PR number (review current branch):
git diff main...HEAD
git log main..HEAD --oneline
```

### Step 2: Understand the Change

Before reviewing line-by-line:
1. **Read the PR description** — What problem does this solve?
2. **Scan the file list** — Which layers are touched? (DB, API, UI, Inngest)
3. **Identify the blast radius** — What could this break?
4. **Check commit history** — Is this one logical change or several?

### Step 3: Review by Category

Run through each category below. Only flag real issues — skip anything that's purely stylistic preference.

### Step 4: Deliver the Review

Use the output format at the bottom. Be direct, cite specific lines, and suggest fixes.

## Review Categories

### 1. Correctness

The most important category. Does the code do what it claims?

- **Logic errors** — Off-by-one, wrong operator, inverted conditions
- **Missing edge cases** — Null/undefined, empty arrays, concurrent access
- **Race conditions** — Async operations that assume ordering
- **State management** — Stale closures, missing dependencies in useEffect
- **Data flow** — Does data actually reach where it needs to go?

### 2. Security

Non-negotiable. Flag and block on any of these:

- **SQL injection** — Raw string interpolation in queries
- **XSS** — Unescaped user input rendered as HTML
- **Auth bypass** — Missing RLS policies, unchecked permissions
- **Secret exposure** — API keys, tokens, or credentials in code
- **IDOR** — Direct object references without ownership checks
- **Server/client boundary** — Sensitive logic in client components, secrets accessible client-side

### 3. Error Handling

Silent failures are bugs waiting to happen:

- **Swallowed errors** — Empty catch blocks, `catch () {}`
- **Missing error propagation** — Errors caught but not re-thrown or logged
- **User-facing errors** — Does the UI show something useful, or does it just break?
- **Inngest failures** — Are step failures handled? Does `onFailure` exist for critical functions?
- **Database errors** — Are constraint violations caught meaningfully?

### 4. Performance

Flag only measurable concerns, not theoretical ones:

- **N+1 queries** — Loops that each make a database call
- **Missing indexes** — New queries on unindexed columns
- **Unbounded fetches** — Queries without LIMIT on user-facing pages
- **Large payloads** — Fetching entire rows when only a few columns are needed
- **Client bundle** — Heavy imports in client components (moment.js, lodash full)
- **Re-renders** — Missing memoization on expensive computations passed as props

### 5. Type Safety

TypeScript should prevent bugs, not just satisfy the compiler:

- **`any` usage** — Every `any` is a bug waiting to happen
- **Type assertions** — `as` casts that bypass actual validation
- **Missing null checks** — Optional chaining where explicit checks belong
- **Zod at boundaries** — External data (API responses, JSONB) must be validated with Zod, not trusted via `as`

### 6. Database & Migrations

Changes to the data layer need extra scrutiny:

- **RLS policies** — Every new table needs them. Every query path must be covered.
- **Migration safety** — Can this run on a live database without downtime?
- **Backwards compatibility** — Will the old code break before the new code deploys?
- **Index coverage** — New WHERE clauses or JOINs need appropriate indexes

### 7. Project Standards

Specific to this codebase:

- **Terminology** — "Enrichment Run" not "backfill run" in user-facing text
- **Provider isolation** — `findymail_verification_result` only set by Findymail provider
- **BYOK model** — LLM keys are per-org, never platform-funded (except Serper)
- **Error classes** — Custom errors extend `AppError` hierarchy from `lib/errors.ts`
- **File placement** — Agent tooling in `execution/` (Python only), app code in `apps/`
- **Enrichment interface** — `enrichBatch()` is the only public method; `enrichProspect()` is internal

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **BLOCK** | Must fix before merge. Security issues, data loss risks, correctness bugs. | Request changes |
| **WARN** | Should fix. Performance issues, missing error handling, type safety gaps. | Comment inline |
| **NOTE** | Consider fixing. Minor improvements, style suggestions with functional impact. | Suggest |

## Output Format

```markdown
## PR Review: [PR title]

**Verdict:** APPROVE / REQUEST CHANGES / NEEDS DISCUSSION

**Summary:** [1-2 sentences: what this PR does and overall assessment]

### Issues

#### BLOCK: [Issue title]
**File:** [file:line](path/to/file#L42)
**Problem:** [What's wrong]
**Fix:** [Concrete suggestion]

#### WARN: [Issue title]
**File:** [file:line](path/to/file#L42)
**Problem:** [What's wrong]
**Fix:** [Concrete suggestion]

#### NOTE: [Issue title]
**File:** [file:line](path/to/file#L42)
**Suggestion:** [What could be improved]

### What Looks Good
- [Positive callout — acknowledge good patterns and decisions]
```

## Anti-Patterns in Reviews

### Don't do this:

- **Style policing** — Don't flag formatting, naming preferences, or import order unless it causes a bug
- **Rewrite requests** — Don't ask to restructure working code just because you'd write it differently
- **Theoretical concerns** — "This could be a problem if..." is not a review comment unless it's plausible
- **Scope creep** — Review what's in the PR, not what you wish was also in the PR
- **Drive-by suggestions** — Every comment should be actionable with a clear severity

### Do this instead:

- **Be specific** — "Line 42: `data` can be null here after the fetch fails" not "check for nulls"
- **Provide fixes** — Don't just point out problems, show the solution
- **Prioritize** — Lead with blockers, end with notes
- **Acknowledge good work** — Call out smart decisions and clean implementations
- **Stay in scope** — Review the diff, not the entire file history

## Rules

1. **Read the full diff** before writing any comments
2. **Understand intent** from the PR description before judging implementation
3. **Flag security issues as BLOCK** — no exceptions
4. **Provide concrete fixes** — don't just say "this is wrong"
5. **One pass, all categories** — don't submit partial reviews
6. **Severity must be justified** — BLOCK requires a real risk, not a preference
7. **Respect the author** — review the code, not the person
