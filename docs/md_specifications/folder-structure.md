# ShutterZilla Folder Structure

This document describes the folder structure adopted for the ShutterZilla project and explains the organization rationale.

## Overview

The project follows a **monorepo structure** with clear separation between application code, infrastructure, and documentation. This organization keeps the root directory clean and makes it easy to locate different types of files.

## Root Directory

The root directory contains only essential configuration files and the GitHub Pages landing page:

```
shutterzilla/
├── .env.local          # Local environment variables (gitignored)
├── .gitignore          # Git ignore rules
├── package.json        # Root package.json (monorepo workspace config)
└── ../README.md           # Project overview and quick start
```

**Rationale:** Keeping the root clean makes it easy to find configuration files and understand the project at a glance.

---

## Main Folders

### `apps/` - Application Code

All application code lives in the `apps/` folder. This includes frontend, backend, and scraping services.

```
apps/
├── frontend/           # Vue.js application
│   ├── src/
│   │   ├── components/ # Vue components (reusable UI)
│   │   ├── views/      # Page views (Scraper, Collection, Admin)
│   │   ├── router/     # Vue Router configuration
│   │   ├── stores/     # Pinia stores (state management)
│   │   ├── lib/        # Utilities (Supabase client, helpers)
│   │   └── main.ts     # Application entry point
│   ├── public/         # Static assets (images, fonts, etc.)
│   ├── package.json    # Frontend dependencies
│   └── vite.config.ts  # Vite build configuration
│
├── backend/            # API serverless functions
│   └── api/
│       ├── auth/       # Authentication endpoints
│       ├── cameras/     # Camera listing endpoints
│       ├── collections/ # Collection endpoints
│       └── admin/       # Admin endpoints
│
└── scraper/            # Python scraping service
    ├── main.py         # Scraper entry point
    ├── scrapers/       # Individual scraper modules
    │   ├── mercari.py
    │   ├── ebay.py
    │   ├── buyee.py
    │   └── jd_direct.py
    ├── utils/          # Utility functions
    │   ├── database.py # Supabase connection
    │   └── helpers.py
    └── requirements.txt # Python dependencies
```

**Rationale:**
- **Clear separation:** All application code in one place
- **Scalability:** Easy to add new apps (e.g., `apps/admin-panel/`, `apps/mobile-app/`)
- **Organization:** No mixing of code with documentation or infrastructure
- **Professional:** Common pattern in modern monorepos (Turborepo, Nx, etc.)

---

### `infrastructure/` - Infrastructure as Code

Infrastructure-related files including database migrations and CI/CD configurations.

```
infrastructure/
├── supabase/           # Database migrations
│   └── migrations/
│       ├── 20240101000000_initial_schema.sql
│       ├── 20240102000000_add_saved_searches.sql
│       └── ...
│
└── .github/            # GitHub Actions workflows
    └── workflows/
        └── scraper.yml # Scheduled scraper execution
```

**Rationale:**
- **Version control:** Database schema changes tracked in git
- **Reproducibility:** Infrastructure can be recreated from code
- **Separation:** Infrastructure code separate from application code

**Note:** The `.github/` folder is typically at the repository root, but we document it here as part of infrastructure. In practice, it may remain at root for GitHub to recognize it.

---

### `docs/` - Project Documentation

All documentation, design assets, and mockups are organized in the `docs/` folder.

```
docs/
├── tech-stack-guide.md      # Comprehensive tech stack guide
├── tech-stack-final.md      # Finalized tech stack reference
├── design-system.md         # Color palette, typography, spacing
├── functional-requirements.md # Feature requirements
├── data-models.md           # Database schema and models
├── component-library.md      # UI component reference
├── page-inventory.md        # Complete page list and sitemap
├── key-decisions-log.md     # Design and architecture decisions
├── folder-structure.md      # Folder structure guide
├── presentation-script.md    # Presentation script
├── session-summary-full.md   # Project summary
├── ../release-notes-v0.1.md    # Release notes
├── ../release-notes-v0.2.md    # Release notes
├── ../README.md                 # Documentation index
│
├── mockupsv1/          # Original desktop-focused HTML/CSS mockups
│   ├── css/
│   │   └── styles.css  # Original stylesheet
│   ├── assets/         # Logo files and placeholder images
│   ├── screenshots/     # Page screenshots for reference
│   └── *.html          # 26 HTML mockup pages
│
├── mockupsv2/          # Mobile-responsive HTML/CSS mockups
│   ├── css/
│   │   └── styles.css  # Mobile-first responsive stylesheet
│   ├── js/
│   │   └── mobile-menu.js # Mobile navigation JavaScript
│   ├── assets/         # Logo files and placeholder images
│   └── *.html          # 26 HTML mockup pages (mobile-optimized)
│
├── branding/           # Logo and brand assets
│   └── Logo/
│       ├── 01 Inspiration Initial Designs/
│       └── 02 Manus Generated Logos/
│           ├── v1_all_gray/
│           └── v2_accent_blade/
│
├── presentation.html   # Interactive presentation
├── index.html          # GitHub Pages landing page
├── README.md           # Documentation index
├── release-notes-v0.1.md    # Release notes
└── release-notes-v0.2.md    # Release notes
```

**Rationale:**
- **Centralized:** All documentation in one place
- **Complete:** Design assets (mockups, branding) alongside written docs
- **Easy to find:** Developers know where to look for documentation
- **Versioned:** Mockups organized by version (v1 = desktop, v2 = mobile-responsive)

---

## File Naming Conventions

### Applications
- Use kebab-case for folder names: `frontend/`, `backend/`, `scraper/`
- Each app has its own `package.json` or `requirements.txt`

### Database Migrations
- Format: `YYYYMMDDHHMMSS_description.sql`
- Example: `20240101000000_initial_schema.sql`
- Timestamp ensures chronological order

### Documentation
- Use kebab-case for markdown files: `tech-stack-guide.md`
- Descriptive names that indicate content: `functional-requirements.md`

---

## Navigation Guide

### For Developers

**Starting development:**
1. Read `../README.md` at root for project overview
2. Check `docs/../README.md` for documentation index
3. Review `docs/md_specifications/tech-stack-guide.md` for setup instructions
4. View `mockupsv2/` for design reference

**Finding code:**
- Frontend code: `apps/frontend/`
- Backend API: `apps/backend/api/`
- Scrapers: `apps/scraper/scrapers/`

**Finding documentation:**
- All docs: `docs/`
- Design system: `docs/design-system.md`
- Mockups: `mockupsv2/` (use v2 for mobile-responsive)

**Finding infrastructure:**
- Database migrations: `infrastructure/supabase/migrations/`
- CI/CD workflows: `infrastructure/.github/workflows/`

### For Designers

**Design assets:**
- Branding: `docs/branding/`
- Mockups: `mockupsv2/` (latest version)
- Design system: `docs/design-system.md`

---

## Benefits of This Structure

### 1. Clear Separation of Concerns
- **Code** (`apps/`) is separate from **documentation** (`docs/`)
- **Infrastructure** (`infrastructure/`) is separate from application code
- Easy to understand what goes where

### 2. Scalability
- Easy to add new applications: just create `apps/new-app/`
- Easy to add new infrastructure: add to `infrastructure/`
- Structure supports growth without reorganization

### 3. Professional Organization
- Follows modern monorepo best practices
- Similar to structures used by Turborepo, Nx, and other monorepo tools
- Clear mental model: "code in apps/, docs in docs/"

### 4. Clean Root Directory
- Root contains only essential files
- Easy to see project structure at a glance
- No clutter from mixing code, docs, and configs

### 5. Easy Navigation
- Developers know where to find code: `apps/`
- Designers know where to find mockups: `mockupsv2/`
- Everyone knows where docs are: `docs/`

---

## Migration Notes

This structure was adopted after the initial design phase. The following changes were made:

1. **Mockups reorganized:**
   - `mockups/` → `mockupsv1/` (renamed for clarity)
   - `mockupsv2/` → `mockupsv2/` (moved to documentation)

2. **Branding moved:**
   - `branding/` → `docs/branding/` (design assets belong with docs)

3. **Documentation organized:**
   - All `.md` files → `docs/` (centralized documentation)

4. **Code structure planned:**
   - Future code will go in `apps/` folder
   - Infrastructure will go in `infrastructure/` folder

All references in documentation and GitHub Pages have been updated to reflect the new structure.

---

## Future Considerations

As the project grows, consider:

1. **Adding shared packages:**
   - `packages/shared-types/` for TypeScript types shared between frontend/backend
   - `packages/ui-components/` for shared UI components

2. **Adding more apps:**
   - `apps/admin-panel/` for separate admin interface
   - `apps/mobile-app/` for mobile application

3. **Infrastructure expansion:**
   - `infrastructure/terraform/` for infrastructure as code
   - `infrastructure/docker/` for container configurations

The current structure supports these additions without major reorganization.

---

## Quick Reference

| What | Where |
|------|-------|
| Frontend code | `apps/frontend/` |
| Backend API | `apps/backend/api/` |
| Scrapers | `apps/scraper/scrapers/` |
| Database migrations | `infrastructure/supabase/migrations/` |
| CI/CD workflows | `infrastructure/.github/workflows/` |
| Documentation | `docs/*.md` |
| Mockups (latest) | `mockupsv2/` |
| Branding assets | `docs/branding/` |
| Project config | Root directory |

---

**Last Updated:** 2026-01-13  
**Structure Version:** 1.0
