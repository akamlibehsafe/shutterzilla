# Migration Notes: GitHub Pages Files

## What Changed

GitHub Pages files (`index.html`, `presentation.html`) have been moved from root to `docs/pages/` to avoid conflicts with app development.

## Why?

1. **Avoid conflicts**: When the app starts, frontend will have its own `index.html`
2. **Clean root**: Root directory stays clean for app code
3. **Better organization**: Pages files are clearly separated from app code

## Files Moved

- `index.html` → `docs/pages/index.html`
- `presentation.html` → `docs/pages/presentation.html` (if existed)

## Workflow Updated

The `.github/workflows/static.yml` workflow has been updated to:
1. Copy files from `docs/pages/` to staging root
2. Copy `docs/` folder for documentation access
3. Deploy everything to GitHub Pages

## Next Steps

1. ✅ Files moved to `docs/pages/`
2. ✅ Workflow updated
3. ⚠️ **Update any links** in `index.html` that reference root paths
4. ⚠️ **Test deployment** on next push to main

## Link Updates Needed

If `index.html` or `presentation.html` reference files with relative paths, they may need updating:
- Links to `docs/mockups/` should work (docs folder is copied)
- Links to root files may need adjustment
