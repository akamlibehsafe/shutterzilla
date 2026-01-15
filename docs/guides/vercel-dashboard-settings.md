# Vercel Dashboard Settings

## Ignore Build Step Setting

### Question: Should I configure "Ignore Build Step" in Vercel Dashboard?

**Answer: No, leave it as "Automatic" (default) or empty.**

### Why?

Since this project uses `vercel.json` with `ignoreCommand`, the Dashboard setting is **overridden** by the file-based configuration.

### How It Works

1. **`vercel.json` takes precedence** - If `ignoreCommand` exists in `vercel.json`, Vercel uses that
2. **Dashboard setting is ignored** - Any command in Dashboard's "Ignore Build Step" won't be used
3. **Best practice** - Keep configuration in code (`vercel.json`) rather than dashboard settings

### Current Setup

- ✅ `vercel.json` contains `ignoreCommand` → Controls build skipping
- ✅ Dashboard "Ignore Build Step" → Leave as "Automatic" or empty (doesn't matter)

### If You Remove `vercel.json` Later

If you delete `vercel.json` and want to control builds via Dashboard:
1. Go to Project Settings → Git → Ignore Build Step
2. Enter your command there
3. But remember: code-based config (`vercel.json`) is preferred for version control

### Summary

**Leave Dashboard setting as "Automatic"** - `vercel.json` handles everything.
