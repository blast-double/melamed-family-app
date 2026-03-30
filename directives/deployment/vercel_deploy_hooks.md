# Vercel Deploy Hooks — Generalized Guide

> **Purpose**: How to set up deploy-hook-based deployments for any Vercel project, bypassing the broken GitHub auto-deploy author attribution.

## Why Deploy Hooks Instead of Auto-Deploy

Vercel's GitHub integration has a **known bug with git author attribution** in multi-repo / multi-project setups. When a Vercel account is connected to many GitHub repos, Vercel sometimes misattributes the git author on pushes. This causes deployments to fail with:

```
Git author {username} must have access to the project on Vercel to create deployments.
```

This happens even when the author DOES have access — Vercel's integration gets confused across projects. The error is on Vercel's side, not a permissions misconfiguration.

**Deploy hooks bypass this entirely** because they're triggered via HTTP POST, not the GitHub integration's push event. The hook doesn't care who pushed — it just builds the latest commit on the configured branch.

---

## Setup (Any Vercel + GitHub Project)

### Step 1: Create the Deploy Hook in Vercel

1. Go to **Project Settings → Git → Deploy Hooks**
2. Create a hook:
   - **Name**: `production` (or `github-action-deploy`)
   - **Branch**: `main` (or your production branch)
3. Copy the generated URL — it looks like:
   ```
   https://api.vercel.com/v1/integrations/deploy/prj_{projectId}/{secret}
   ```

### Step 2: Disable Auto-Deploy

Add to your project's `vercel.json` (in the app root, wherever Vercel's Root Directory points):

```json
{
  "git": {
    "deploymentEnabled": false
  }
}
```

**This does three things:**
- Stops Vercel from auto-building on every push
- Keeps the GitHub integration connected (PR comments, status checks, etc.)
- Deploy hooks still work (they are NOT affected by this setting)

**WARNING — Do NOT use `github.enabled: false`**. That setting is deprecated and **breaks deploy hooks entirely**. Only use `git.deploymentEnabled: false`.

### Step 3: Store the Hook URL as a GitHub Actions Secret

```bash
gh secret set VERCEL_DEPLOY_HOOK --body "https://api.vercel.com/v1/integrations/deploy/prj_{projectId}/{secret}"
```

Also store in your local `.env` for manual deploys:

```
VERCEL_DEPLOY_HOOK=https://api.vercel.com/v1/integrations/deploy/prj_{projectId}/{secret}
```

### Step 4: Add Deploy Job to CI Workflow

In `.github/workflows/ci.yml` (or your CI file), add a deploy job that runs after your tests/build:

```yaml
  deploy:
    name: Deploy to Vercel
    needs: lint-and-build  # or whatever your CI job is called
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Vercel Deploy Hook
        run: curl -fsS -X POST "${{ secrets.VERCEL_DEPLOY_HOOK }}"
```

Key points:
- `needs:` ensures deploy only runs after CI passes
- `if:` ensures it only deploys on pushes to main (not on PR branches)
- The hook URL is read from the GitHub Actions secret

---

## Result

```
PR merged to main
  → GitHub Actions CI runs (tests, lint, build)
    → CI passes → deploy job triggers VERCEL_DEPLOY_HOOK
      → Vercel builds and deploys to production
```

- **One deployment per merge** — no duplicates
- **Gated behind CI** — broken code doesn't deploy
- **No author attribution issues** — hook doesn't check git author
- **GitHub integration still works** — PR comments, deployment status events

---

## Manual Deploy

For deploying without a push (e.g., after changing Vercel env vars):

```bash
source .env && curl -fsS -X POST "$VERCEL_DEPLOY_HOOK"
```

---

## Troubleshooting

### Duplicate deployments appearing
**Cause**: `git.deploymentEnabled: false` is not set in `vercel.json`, so both the auto-deploy and the hook fire.
**Fix**: Add the setting to `vercel.json` and push.

### Deploy hook returns 200 but no build appears
**Cause**: `github.enabled: false` is in `vercel.json`. This breaks hooks.
**Fix**: Remove that setting. Use `git.deploymentEnabled: false` instead.

### "Git author must have access" errors
**Cause**: Known Vercel bug with multi-project GitHub accounts. Auto-deploy misattributes the git committer.
**Fix**: This is the whole reason for deploy hooks. Set up the hook + disable auto-deploy as described above.

### CI passes but deploy job is skipped
**Cause**: The `if:` condition doesn't match. Common issues:
- Event is `pull_request` not `push` (deploy only runs on push to main)
- Branch name doesn't match `refs/heads/main`
**Fix**: Check that CI triggers on `push: branches: [main]` and the deploy job's `if:` condition matches.

### Hook URL exposed in logs
**Cause**: Using `echo` or logging the curl command.
**Fix**: GitHub Actions masks secrets automatically in `${{ secrets.* }}`. Never hardcode the URL in workflow files.

---

## Checklist for New Projects

- [ ] Deploy hook created in Vercel (Settings → Git → Deploy Hooks)
- [ ] `git.deploymentEnabled: false` added to `vercel.json`
- [ ] Hook URL stored as `VERCEL_DEPLOY_HOOK` GitHub Actions secret
- [ ] Hook URL stored in local `.env` for manual deploys
- [ ] Deploy job added to CI workflow with `needs:` and `if:` guards
- [ ] First merge to main produces exactly ONE Vercel deployment
- [ ] GitHub PR comments still appear (integration still connected)
