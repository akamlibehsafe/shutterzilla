# GitHub Pages Source Files

This folder contains the source files for the GitHub Pages site.

## Files

- `index.html` - Landing page for the GitHub Pages site
- `presentation.html` - Interactive presentation (if applicable)

## Deployment

These files are automatically deployed to GitHub Pages via the `.github/workflows/static.yml` workflow.

The workflow:
1. Copies files from `docs/pages/` to a staging directory
2. Copies `docs/` folder contents (for documentation)
3. Deploys everything to GitHub Pages

## Why Separate?

- **Avoids conflicts**: Keeps root directory clean for app development
- **Clear separation**: Pages files are separate from app code
- **Easy maintenance**: All Pages-related files in one place

## Note

When the app starts development, the frontend will have its own `index.html` (e.g., `apps/frontend/index.html` or `apps/frontend/public/index.html`). This folder ensures the GitHub Pages site doesn't conflict with the app.
