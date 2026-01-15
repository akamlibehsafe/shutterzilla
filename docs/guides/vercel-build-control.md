# Controlling Vercel Builds

## Problem

Vercel automatically tries to build your app on every push, but since the app is incomplete, builds fail.

## ✅ Adopted Solution: Code-Based Control via `vercel.json`

**This project uses `vercel.json` to control builds.** This approach is version-controlled, clear, and easy to toggle.

### Current Configuration

The `vercel.json` file in the project root contains:
```json
{
  "ignoreCommand": "echo '⚠️  Builds disabled - app not ready for deployment yet' && exit 0"
}
```

### How It Works

- Vercel runs the `ignoreCommand` before each build
- **Exit code `0`** = Skip/Cancel the deployment (build is skipped)
- **Exit code `1` (or non-zero)** = Proceed with the deployment (build continues)

**Note:** This is counterintuitive! Exit 0 usually means "success", but in Vercel's `ignoreCommand`, exit 0 means "skip this build".

### Enabling Builds

When the app is ready for deployment:

**Option 1:** Change `exit 0` to `exit 1` in `vercel.json` (to allow builds)
```json
{
  "ignoreCommand": "exit 1"
}
```

Or simply remove the `ignoreCommand` entirely.

**Option 2:** Delete `vercel.json` entirely

**Option 3:** Use conditional logic (see Advanced section below)

### Benefits

- ✅ Version controlled - decision is documented in code
- ✅ Easy to toggle - just edit one file
- ✅ Clear intent - anyone can see builds are disabled
- ✅ No dashboard access needed

### Dashboard Setting vs `vercel.json`

**Important:** `ignoreCommand` in `vercel.json` **overrides** the Dashboard's "Ignore Build Step" setting.

- If you have `ignoreCommand` in `vercel.json`, Vercel uses that (Dashboard setting is ignored)
- If you don't have `ignoreCommand` in `vercel.json`, Vercel uses the Dashboard setting

**Recommendation:** Since we're using `vercel.json`:
- Leave Dashboard "Ignore Build Step" as **"Automatic"** (default) or **empty**
- The `vercel.json` file will control everything
- This keeps configuration in code, not in dashboard settings

---

## Alternative Solutions (Not Currently Used)

### Option 1: Pause Project in Vercel Dashboard (Recommended - Easiest)

**Steps:**
1. Go to [vercel.com](https://vercel.com) and log in
2. Navigate to your project
3. Go to **Settings** → **General**
4. Scroll down to find **"Pause Project"** or **"Deployment Protection"**
5. Click **"Pause"** or enable **"Ignore Build Step"**
6. The project will stop building automatically

**To resume later:**
- Return to Settings → General
- Click **"Resume"** or disable **"Ignore Build Step"**

**Pros:**
- ✅ No code changes needed
- ✅ Easy to toggle on/off
- ✅ Preserves all Vercel settings

**Cons:**
- ❌ Requires manual action in dashboard

---

### Option 2: Ignore Builds via `vercel.json` (Code-Based) ✅ **CURRENTLY USED**

This is the approach adopted for this project. See the "Adopted Solution" section above for details.

---

### Option 3: Disable Automatic Deployments (Branch-Based)

**Steps:**
1. Go to Vercel Dashboard → Your Project → **Settings** → **Git**
2. Under **"Production Branch"** or **"Deployment Protection"**
3. Enable **"Only deploy when a commit is pushed to the Production Branch"**
4. Or disable automatic deployments for specific branches

**Pros:**
- ✅ More granular control
- ✅ Can still deploy manually when ready

**Cons:**
- ❌ Still builds on production branch pushes

---

### Option 4: Remove Vercel Integration Temporarily

**Steps:**
1. Go to Vercel Dashboard → Your Project → **Settings** → **Git**
2. Click **"Disconnect"** or **"Remove Integration"**
3. Reconnect when ready to deploy

**Pros:**
- ✅ Completely stops all builds
- ✅ No failed builds cluttering dashboard

**Cons:**
- ❌ Need to reconnect later
- ❌ May lose some deployment history

---

### Option 5: Use `.vercelignore` Pattern

Create a `vercel.json` that ignores all files:

```json
{
  "buildCommand": "echo 'Builds disabled' && exit 1",
  "outputDirectory": "."
}
```

Or use Vercel's "Ignore Build Step" feature via environment variable check.

---

## Advanced: Conditional Builds

You can make builds conditional based on branch, environment variables, or other factors:

### Example: Only Build on `main` Branch

```json
{
  "ignoreCommand": "if [ \"$VERCEL_GIT_COMMIT_REF\" != \"main\" ]; then exit 1; fi; exit 0"
}
```

### Example: Build Only When `ENABLE_BUILD` Env Var is Set

```json
{
  "ignoreCommand": "if [ -z \"$ENABLE_BUILD\" ]; then echo 'Builds disabled' && exit 1; fi; exit 0"
}
```

### Example: Check for Build Marker File

```json
{
  "ignoreCommand": "if [ ! -f \".vercel-build-enabled\" ]; then echo 'Builds disabled - create .vercel-build-enabled to enable' && exit 1; fi; exit 0"
}
```

Then create `.vercel-build-enabled` when ready (and add it to `.gitignore` if you want local control).

---

## Checking Current Status

To see if Vercel is connected:
- Check `.vercel/` folder (if exists, contains project ID)
- Check Vercel dashboard for your GitHub repo
- Look for Vercel badges/links in README (if any)

---

## Future: Selective Builds

When your app is ready, you can configure Vercel to:
- Only build on specific branches (e.g., `main`, `production`)
- Use build commands that check if app is ready
- Deploy only when certain conditions are met

---

## Notes

- Vercel builds are triggered by GitHub webhooks
- Even paused projects may show in dashboard (but won't build)
- You can always deploy manually via Vercel CLI: `vercel --prod`
