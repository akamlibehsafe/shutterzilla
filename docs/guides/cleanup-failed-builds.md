# Cleaning Up Failed Build Notices on GitHub

## What Can and Can't Be Done

### ❌ Cannot Delete
- **Status checks on commits/PRs** - These are part of commit history and cannot be manually removed
- **Failed checks in PR checks list** - Historical checks remain visible

### ✅ Can Delete/Clean Up
- **Workflow runs in Actions tab** - Can be deleted (if > 2 weeks old or completed)
- **Old Vercel deployment runs** - Can be cleaned up via Vercel dashboard

---

## Options for Cleaning Up

### Option 1: Delete Old Workflow Runs (GitHub Actions)

If you have failed GitHub Actions workflow runs:

**Via GitHub UI:**
1. Go to your repository → **Actions** tab
2. Find failed workflow runs
3. Click on a run → Click **"..."** menu → **"Delete workflow run"**
4. Confirm deletion

**Via GitHub CLI (bulk delete):**
```bash
# List failed runs
gh run list --status failure --limit 100

# Delete specific run by ID
gh run delete <run-id>

# Or use a script to delete all failed runs older than X days
```

**Note:** Only completed runs older than 2 weeks can be deleted via UI. Newer runs need API/CLI.

---

### Option 2: Clean Up Vercel Builds

Vercel builds show up as status checks on GitHub commits. You can:

**Via Vercel Dashboard:**
1. Go to Vercel Dashboard → Your Project → **Deployments**
2. Find failed deployments
3. Click **"..."** → **"Delete"** (if available)
4. Or filter by status and bulk delete

**Note:** Deleting Vercel deployments removes them from Vercel dashboard, but the **status check on GitHub commits remains** (it's part of commit history).

---

### Option 3: Rerun Failed Checks (Changes Status)

If you want to change a failed check to success:

1. **For GitHub Actions:** Go to Actions → Click failed run → **"Re-run jobs"**
2. **For Vercel:** Push a new commit (with `vercel.json` now, it will skip instead of fail)

**Important:** With `vercel.json` configured, new commits will show as **"skipped"** (not failed), which is cleaner.

---

### Option 4: Override Status Checks (Advanced)

You can use GitHub API to add a new "success" status, but this doesn't remove the old failed one:

```bash
# Using GitHub CLI
gh api repos/:owner/:repo/statuses/<commit-sha> \
  -f state=success \
  -f context="vercel" \
  -f description="Build skipped - app not ready"
```

**Note:** This adds a new status but doesn't remove the old failed one. Both will show.

---

## Recommended Approach

### For Future Commits
✅ **Already handled** - With `vercel.json` configured:
- New commits will show as **"skipped"** (not failed)
- No more failed build notices going forward
- Clean status checks

### For Past Failed Builds

**Option A: Leave them** (simplest)
- They're historical and don't affect new work
- New commits will show skipped status
- No action needed

**Option B: Clean up Vercel dashboard**
- Delete old failed deployments in Vercel
- Keeps dashboard clean
- Status checks on GitHub commits remain (historical)

**Option C: Delete old workflow runs** (if using GitHub Actions)
- Clean up Actions tab
- Use GitHub CLI for bulk operations
- Only affects workflow runs, not commit status checks

---

## Script: Bulk Delete Old Failed Workflow Runs

If you want to clean up old GitHub Actions runs:

```bash
#!/bin/bash
# Delete all failed workflow runs older than 30 days

gh run list --status failure --limit 100 --json databaseId,createdAt \
  | jq -r '.[] | select(.createdAt < (now - 2592000 | strftime("%Y-%m-%dT%H:%M:%SZ"))) | .databaseId' \
  | while read run_id; do
      echo "Deleting run $run_id..."
      gh run delete $run_id --confirm
    done
```

**Note:** Requires `gh` CLI and `jq` installed.

---

## Summary

**Short answer:** You can't delete status checks from commits (they're historical), but:

1. ✅ **Future builds** - Will show as "skipped" (not failed) thanks to `vercel.json`
2. ✅ **Old workflow runs** - Can be deleted from Actions tab
3. ✅ **Vercel deployments** - Can be deleted from Vercel dashboard
4. ❌ **Commit status checks** - Cannot be deleted (part of history)

**Best approach:** Leave old failures as historical record. New commits will show clean "skipped" status.

---

## See Also

- [GitHub: Delete workflow runs](https://docs.github.com/en/actions/managing-workflow-runs/deleting-a-workflow-run)
- [GitHub CLI: Managing runs](https://cli.github.com/manual/gh_run)
- [Vercel: Managing deployments](https://vercel.com/docs/concepts/deployments)
