*Last Edited: 2026-03-30*

# Vercel Deploy Hooks

> **Purpose**: How to use deploy hooks for manual or CI-triggered deployments.

## Current Setup

| Setting | Value |
|---------|-------|
| **GitHub Repo** | `blast-double/melamed-family-app` |
| **Vercel Root Directory** | `tax-portal/` |
| **Deploy Trigger** | Push to `main` (auto) or deploy hook (manual) |
| **Deploy Hook** | Stored in `.env` as `VERCEL_DEPLOY_HOOK` |
| **Project ID** | Stored in `.env` as `VERCEL_PROJECT_ID` |

## Why Deploy Hooks

Vercel's GitHub integration has a known bug with git author attribution in multi-repo setups. Deploy hooks bypass this by triggering builds via HTTP POST instead of the push event.

## Manual Deploy

For deploying after env var changes or when auto-deploy isn't triggering:

```bash
source .env && curl -fsS -X POST "$VERCEL_DEPLOY_HOOK"
```

## Future: GitHub Actions CI

When the project needs CI gating (tests must pass before deploy):

1. Add `vercel.json` to `tax-portal/`:
   ```json
   { "git": { "deploymentEnabled": false } }
   ```
2. Create `.github/workflows/ci.yml` with build + test + deploy hook trigger
3. Store `VERCEL_DEPLOY_HOOK` as a GitHub Actions secret

This is not set up yet — Vercel currently auto-deploys on every push to main.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Duplicate deployments | Add `git.deploymentEnabled: false` to `vercel.json` |
| Hook returns 200, no build | Don't use deprecated `github.enabled: false` |
| Build passes locally, fails on Vercel | Missing env var in Vercel dashboard |
| "Git author must have access" | Use deploy hooks instead of auto-deploy |
