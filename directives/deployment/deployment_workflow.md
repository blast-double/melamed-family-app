*Last Edited: 2026-03-30*

# Deployment Workflow

> **Directive**: How to safely deploy changes to production via GitHub + Vercel.

---

## Overview

The personal workspace is a **monorepo** with the tax portal as a subdirectory:

```
Local Changes → Git Commit → Push to GitHub → Vercel → Production
```

**GitHub Repository**: `blast-double/melamed-family-app`
**Vercel Project**: Tax Portal (root directory: `tax-portal/`)
**Production URL**: Check Vercel dashboard

Every push to `main` triggers a Vercel build. There is no CI pipeline yet — Vercel builds directly from the GitHub push. A broken commit goes straight to production.

---

## Project Structure

```
melamed-family-app/          ← git root (blast-double/melamed-family-app)
├── execution/               ← Python tools (not deployed)
├── config/                  ← YAML configs (not deployed)
├── .claude/skills/          ← Claude skills (not deployed)
├── directives/              ← SOPs and reference docs (not deployed)
├── tests/                   ← Python tests (not deployed)
├── tax-portal/              ← Next.js app (Vercel deploys THIS)
│   ├── src/
│   ├── package.json
│   └── ...
├── dashboard/               ← Next.js app (not yet deployed)
├── CLAUDE.md
└── .gitignore
```

Only `tax-portal/` is deployed to Vercel. Everything else is backend tooling that runs locally via Claude Code.

---

## Deploying to Production

**Just push to main:**

```bash
git push origin main
```

Vercel detects the push and builds `tax-portal/` automatically.

### Manual Deploy (Emergency / Env Var Changes)

After changing Vercel environment variables (which don't trigger a rebuild):

```bash
source .env && curl -fsS -X POST "$VERCEL_DEPLOY_HOOK"
```

---

## Pre-Deployment Checklist

### 1. Verify TypeScript Compiles

```bash
cd tax-portal && npx tsc --noEmit
```

### 2. Verify Build Succeeds

```bash
cd tax-portal && npm run build
```

This catches build-time issues, missing env vars in server components, and Next.js errors.

### 3. Run Python Tests (If Backend Changed)

```bash
python3 -m pytest tests/ -v
```

### 4. Check for Unintended Changes

```bash
git diff
git status
```

Review every line. Look for:
- Debug `console.log` statements
- Hardcoded values
- Accidentally modified files
- Credentials or secrets

---

## Commit Standards

### Commit Message Format

```
<type>: <description>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**Types:** `fix`, `feat`, `refactor`, `docs`, `style`, `test`, `chore`

### Selective Staging

**Never run `git add .` or `git add -A`.** Stage specific files:

```bash
git add execution/tax/rename_docs.py config/tax_config.yaml
```

Unrelated local changes frequently exist from parallel work sessions.

---

## Environment Variables

### Vercel (Production)

Set in Vercel Dashboard → Project Settings → Environment Variables:

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL (client-side) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key (client-side, RLS-protected) |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service key (server-side API routes) |

### Local Development (`.env` — gitignored)

Contains all Vercel vars plus:

| Variable | Purpose |
|----------|---------|
| `VERCEL_DEPLOY_HOOK` | Deploy hook URL for manual triggers |
| `VERCEL_PROJECT_ID` | Vercel project identifier |
| `GOOGLE_OCR` | Google Document AI endpoint |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to GCP service account JSON |
| `MONARCH_EMAIL` / `MONARCH_PASSWORD` / `MONARCH_MFA_SECRET_KEY` | Monarch Money API |
| `SUPABASE_PROJECT_URL` / `SUPABASE_SERVICE_ROLE_KEY` | Supabase (Python backend) |
| `ASANA_PAT` | Asana API token |

### Adding a New Env Var

1. Add to `.env` locally
2. If needed by the portal at runtime: add to Vercel Environment Variables
3. If needed at build time: prefix with `NEXT_PUBLIC_`
4. Trigger a rebuild: `source .env && curl -fsS -X POST "$VERCEL_DEPLOY_HOOK"`

---

## Rollback Procedure

### Quick Rollback (Vercel UI)
1. Vercel Dashboard → Deployments
2. Find last working deployment
3. Click "..." → "Promote to Production"

### Git Rollback
```bash
git revert HEAD
git push origin main
```

**Never use `git reset --hard` on main.**

---

## Common Errors

| Error | Fix |
|-------|-----|
| Build fails: Module not found | Check import paths, run `npm install` in `tax-portal/` |
| Build fails: Type error | Run `npx tsc --noEmit` locally, fix errors |
| Runtime: Missing env var | Add to Vercel Dashboard → Environment Variables |
| Deploy hook returns 200, no build | Check `vercel.json` — don't use deprecated `github.enabled: false` |
| Build passes locally, fails on Vercel | Missing env var in Vercel (works locally because `.env.local` exists) |

---

## Summary: The Safe Deploy Flow

```
1. Make changes
2. cd tax-portal && npx tsc --noEmit     # Verify types
3. cd tax-portal && npm run build        # Verify build
4. python3 -m pytest tests/ -v           # If backend changed
5. git diff                              # Review changes
6. git add <specific files>              # Stage intentionally
7. git commit -m "type: description"     # Descriptive message
8. git push origin main                  # Vercel auto-deploys
9. Check Vercel dashboard                # Confirm success
10. Test in production                   # Verify it works
```
