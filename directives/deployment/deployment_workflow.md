# Deployment Workflow

> **Directive**: How to safely deploy changes to production via GitHub Actions + Vercel.

---

## Overview

Auto Prospector uses **GitHub Actions** for automatic deployments:

```
Local Changes → Git Commit → Push to GitHub → GitHub Actions CI → Deploy Hook → Vercel → Production
```

**GitHub Repository**: `blast-double/auto-prospector` (https://github.com/blast-double/auto-prospector)

Every push to `main` triggers the workflow in `.github/workflows/ci.yml`, which first runs type-check (`tsc --noEmit`) and build (`npm run build`), then triggers the Vercel deploy hook. PRs to `main` run the CI job only (no deploy). This bypasses the Vercel GitHub App integration (which has a known bug with org-authored squash merges). See `directives/vercel_deploy_hooks.md` for the full deploy hook setup guide.

A broken commit that passes CI still goes directly to production — there's no staging environment. This directive ensures you minimize errors.

### Deploying to Production

**Just push to main:**

```bash
git push origin main
```

GitHub Actions handles the rest automatically. Monitor the deploy at: https://github.com/blast-double/auto-prospector/actions

### Required GitHub Secrets

The following secret must be set on the GitHub repo (Settings → Secrets and variables → Actions):

| Secret | Description |
|--------|-------------|
| `VERCEL_DEPLOY_HOOK` | Vercel deploy hook URL (created in Project Settings → Git → Deploy Hooks) |

### Manual Deploy (Emergency Only)

If GitHub Actions is down, trigger the deploy hook directly:

```bash
# Push to GitHub first
git push origin main

# Then trigger deploy hook manually (requires VERCEL_DEPLOY_HOOK in .env)
source .env && curl -fsS -X POST "$VERCEL_DEPLOY_HOOK"
```

---

## Pre-Deployment Checklist

### 1. Verify TypeScript Compiles

**Always run before committing:**

```bash
cd apps/prospector-v2 && npx tsc --noEmit
```

This catches:
- Type errors
- Missing imports
- Interface mismatches

**If it fails**: Fix all errors before proceeding. Never push code that doesn't compile.

### 2. Verify Build Succeeds

**For significant changes:**

```bash
cd apps/prospector-v2 && npm run build
```

This catches:
- ESLint errors (if configured as build errors)
- Next.js build-time issues
- Missing environment variables in server components
- Dynamic import problems

**If it fails**: Fix all errors. Vercel will reject the deploy anyway.

### 3. Test Locally (When Applicable)

For UI changes:
```bash
cd apps/prospector-v2 && npm run dev
```

Then manually verify the change works as expected.

### 4. Check for Unintended Changes

```bash
git diff
```

Review every line. Look for:
- Debug console.log statements
- Hardcoded values
- Accidentally modified files
- Credentials or secrets

---

## Commit Standards

### Commit Message Format

Use conventional commits:

```
<type>: <description>

<optional body>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Types:**
| Type | Use For |
|------|---------|
| `fix` | Bug fixes |
| `feat` | New features |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace |
| `test` | Adding/fixing tests |
| `chore` | Build config, dependencies |

**Examples:**
```bash
# Bug fix
git commit -m "fix: HubSpot integration showing configured when token missing"

# Feature
git commit -m "feat: Add property mapping clear option for HubSpot sync"

# Refactor
git commit -m "refactor: Extract credential validation into separate module"
```

### Atomic Commits

- One logical change per commit
- If you need "and" in the description, it's probably two commits
- Makes rollbacks easier if something breaks

---

## Git Workflow

### Git Author Configuration

**Required author email**: `aaron@palisadeslabs.ai`

Ensure your git config is set correctly before committing:

```bash
# Set for this repo only
git config user.email "aaron@palisadeslabs.ai"

# Verify
git config user.email
```

If a commit was made with the wrong author, it will need to be amended or the history corrected.

### Standard Deploy

```bash
# 1. Check what you're committing
git status
git diff

# 2. Stage specific files (preferred over git add -A)
git add path/to/file1.ts path/to/file2.tsx

# 3. Commit with descriptive message
git commit -m "fix: Description of what this fixes

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# 4. Push to trigger deploy (GitHub Actions handles the rest)
git push origin main
```

### When Pre-Commit Hooks Fail

If hooks fail due to unrelated issues (e.g., test config problems):

```bash
# Only skip if the failure is NOT related to your changes
git commit --no-verify -m "fix: Your message

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Warning**: Never skip hooks to bypass legitimate errors in your code.

---

## Post-Deploy Verification

### 1. Check Deployment Status

After pushing, check deployment status:
- **GitHub Actions**: https://github.com/blast-double/auto-prospector/actions (build + deploy)
- **Vercel Dashboard**: Check for successful deployment and production URL
- Review build logs if failed

### 2. Verify in Production

After successful deploy (~1-2 minutes):
1. Open production URL
2. Test the specific feature you changed
3. Check browser console for errors
4. Verify no regressions in related features

### 3. Monitor for Issues

For the next hour, watch for:
- Error reports in Vercel logs
- User complaints
- Inngest function failures (if backend changes)

---

## Rollback Procedure

If a deploy breaks production:

### Quick Rollback (Vercel UI)
1. Go to Vercel Dashboard → Deployments
2. Find the last working deployment
3. Click "..." → "Promote to Production"

### Git Rollback
```bash
# Revert the problematic commit
git revert HEAD

# Push the revert
git push origin main
```

**Never use `git reset --hard` on main** - this rewrites history and causes problems for others.

---

## Environment Variables

### Vercel Environment Variables

Production environment variables are set in Vercel:
- Go to Project Settings → Environment Variables
- Never commit secrets to git
- Update Vercel env vars before deploying code that uses new ones

### Local Development

Use `.claude/settings.local.json` for local env vars (never committed).

### New Env Var Checklist

When adding a new environment variable:
1. Add to `.claude/settings.local.json.example` (template)
2. Add to Vercel production environment
3. Update `directives/credentials_policy.md` if it's a credential
4. Add validation in code for missing var

---

## Common Errors and Fixes

### Build Error: Module Not Found

**Cause**: Import path wrong or dependency missing

**Fix**:
```bash
# Check import paths are correct
# Ensure package is in package.json
npm install missing-package
```

### Build Error: Type 'X' is not assignable to type 'Y'

**Cause**: TypeScript type mismatch

**Fix**: Run `npx tsc --noEmit` locally, fix all type errors

### Runtime Error: Missing Environment Variable

**Cause**: Code uses env var not set in Vercel

**Fix**: Add the variable in Vercel Dashboard → Environment Variables

### Deploy Stuck / Queued

**Cause**: Previous deploy still running or GitHub Actions issue

**Fix**:
1. Check https://github.com/blast-double/auto-prospector/actions for stuck runs
2. Cancel the stuck run if needed
3. If GitHub Actions is down, use the manual Vercel CLI deploy (see above)

---

## Files Modified Checklist

Before pushing, verify you haven't accidentally modified:

| File Pattern | Should Be Modified? |
|--------------|---------------------|
| `*.ts`, `*.tsx` | ✅ If intentional |
| `package.json` | ⚠️ Only if adding deps |
| `package-lock.json` | ⚠️ Only if deps changed |
| `.env*` | ❌ Never commit |
| `*.local.*` | ❌ Never commit |
| `node_modules/` | ❌ Never commit |

---

## Summary: The Safe Deploy Flow

```
1. Make changes
2. npx tsc --noEmit          # Verify types
3. npm run build             # Verify build (optional but recommended)
4. npm run dev + test        # Verify functionality
5. git diff                  # Review changes
6. git add <specific files>  # Stage intentionally
7. git commit -m "..."       # Descriptive message
8. git push origin main      # GitHub Actions auto-deploys
9. Check Actions + Vercel    # Confirm success
10. Test in production       # Verify it works
```

---

## References

- [Vercel Deployments Documentation](https://vercel.com/docs/deployments)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Revert vs Reset](https://www.atlassian.com/git/tutorials/undoing-changes)
