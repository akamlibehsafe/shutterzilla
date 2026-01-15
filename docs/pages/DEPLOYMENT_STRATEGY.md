# GitHub Pages Deployment Strategy

## Problem

When the app starts development, there will be conflicts:
- Frontend app will have `apps/frontend/index.html` or `apps/frontend/public/index.html`
- GitHub Pages needs `index.html` at root or in `docs/`
- Root directory should stay clean for app development

## Solution

Store GitHub Pages files in `docs/pages/` and deploy via GitHub Actions workflow.

## Structure

```
docs/
├── pages/              # GitHub Pages source files
│   ├── index.html      # Landing page
│   └── presentation.html # Presentation (if needed)
├── mockups/            # Design mockups
│   ├── current/        # Latest version (currently v2)
│   ├── v1/            # Version 1 (archived)
│   └── v2/            # Version 2 (when archived)
└── ...                 # Other documentation
```

## Workflow Strategy

The `.github/workflows/static.yml` workflow should:

1. **Create staging directory** for Pages deployment
2. **Copy Pages files** from `docs/pages/` to staging root
3. **Copy docs folder** to staging (for documentation access)
4. **Deploy** staging directory to GitHub Pages

This ensures:
- ✅ Root directory stays clean for app development
- ✅ Pages files are version-controlled in `docs/pages/`
- ✅ No conflicts with app `index.html`
- ✅ Documentation remains accessible via Pages

## Alternative: Use `/docs` as Pages Source

GitHub Pages can be configured to serve directly from `/docs` folder:
- Settings → Pages → Source: `/docs` folder
- Then `docs/index.html` becomes the Pages root
- But this still conflicts with app development

**Recommended:** Use workflow-based deployment from `docs/pages/` for maximum flexibility.
