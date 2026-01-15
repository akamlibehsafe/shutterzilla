# Vercel Configuration File Location

## Question

Is `vercel.json` in the correct location (project root)?

## Answer: ✅ YES

**`vercel.json` must be in the project root directory** (or the root directory configured in Vercel project settings).

---

## Vercel's Requirements

### Standard Behavior

- ✅ Vercel looks for `vercel.json` at the **project root**
- ✅ It must be at the root of the directory that Vercel treats as the project root
- ✅ This is where Vercel applies build configuration, routing, and deployment settings

### Current Setup

```
shutterzilla/                    # Repository root
├── vercel.json                  # ✅ CORRECT - At repo root
├── .gitignore
├── package.json
├── apps/                        # Future app code
└── docs/                        # Documentation
```

**Status:** ✅ Correct location

---

## Monorepo Considerations

For monorepos (like this project), you have two options:

### Option 1: Repo Root (Current Approach) ✅

Keep `vercel.json` at the repository root:
- **Pros:**
  - Single configuration for the entire repo
  - Works for repo-level build control (like disabling builds)
  - Simple and clear
- **Cons:**
  - When deploying a specific app, you may need to configure build settings differently

**Best for:** Repo-level configuration (like build disabling), or when you want one Vercel project per repo.

### Option 2: App-Specific Root

Set Vercel's "Root Directory" to the app subdirectory (e.g., `apps/frontend/`):
- Move `vercel.json` to that subdirectory
- Configure Vercel project settings → Build & Deployment → Root Directory = `apps/frontend/`
- **Pros:**
  - App-specific configuration
  - Better for multiple apps in one repo (one Vercel project per app)
- **Cons:**
  - More complex setup
  - Need separate Vercel projects for each app

**Best for:** When deploying specific apps from a monorepo, or when you have multiple Vercel projects.

---

## Current Use Case

Right now, `vercel.json` is used to **disable builds** at the repo level:

```json
{
  "ignoreCommand": "echo '⚠️  Builds disabled - app not ready for deployment yet' && exit 0"
}
```

This is perfect for repo-root placement because:
- ✅ It applies to the entire repository
- ✅ Works regardless of which app might be deployed later
- ✅ Simple and clear

---

## Future Considerations

When you're ready to deploy the app (from `apps/frontend/` or similar):

1. **If keeping repo-root approach:**
   - Keep `vercel.json` at root
   - Configure build settings in Vercel dashboard for the specific app path
   - Or update `vercel.json` with app-specific build commands

2. **If switching to app-specific:**
   - Set Vercel project "Root Directory" to `apps/frontend/`
   - Move `vercel.json` to `apps/frontend/vercel.json`
   - Configure app-specific settings there

---

## Summary

✅ **Current location is correct:** `vercel.json` at repo root  
✅ **Vercel requires it at the project root** (or configured root directory)  
✅ **Current setup works perfectly** for repo-level build control  
✅ **Future flexibility:** Can move to app-specific location when needed

---

## See Also

- [Vercel Project Configuration](https://vercel.com/docs/projects/project-configuration)
- [Vercel Build Configuration](https://vercel.com/docs/builds/configure-a-build)
- `docs/guides/vercel-build-control.md` - How build control works
