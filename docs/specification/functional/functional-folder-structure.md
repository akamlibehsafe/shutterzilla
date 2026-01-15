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
├── vercel.json         # Vercel build control configuration
├── validation/         # Scraping validation tests (kept as documentation)
│   ├── README.md       # Validation overview and purpose
│   └── scrapers/       # Test scripts for scraping feasibility
└── README.md            # Project overview and quick start
```

**Rationale:** Keeping the root clean makes it easy to find configuration files and understand the project at a glance. The `validation/` folder is kept as historical documentation of scraping feasibility testing.

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
    │   ├── ebay.py
    │   └── buyee.py
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

**Note:** For detailed documentation folder structure and organization rationale, see [`docs/specification/technical/folder-structure.md`](../technical/folder-structure.md).

```
docs/
├── README.md                    # Main documentation index
│
├── guides/                      # Process & workflow documentation
│   ├── automation.md            # How to automate documentation
│   ├── quick-reference.md       # Quick command reference
│   ├── documentation-workflow.md # Complete workflow guide
│   ├── quick-start-automation.md # Quick start for automation
│   └── migration/               # Migration docs (archived)
│
├── project/                     # Project-specific documentation
│   ├── ai-context.md            # AI/contributor briefing
│   ├── runbook.md               # Operations guide
│   ├── decisions/               # Architecture Decision Records (ADRs)
│   │   └── 0001-*.md, 0002-*.md, etc.
│   └── releases/                # Release notes
│       └── release-notes-v*.md
│
├── specification/               # Technical specifications
│   ├── design/                  # Design-related specs
│   │   ├── design-system.md
│   │   ├── component-library.md
│   │   └── page-inventory.md
│   ├── technical/               # Technical specs
│   │   ├── tech-stack-guide.md
│   │   ├── tech-stack-final.md
│   │   ├── data-models.md
│   │   └── folder-structure.md
│   ├── implementation/          # Implementation docs
│   │   ├── implementation-plan.md
│   │   ├── implementation-notes.md
│   │   ├── key-decisions-log.md
│   │   └── ... (other implementation docs)
│   └── functional/             # Functional specs
│       ├── functional-requirements.md
│       ├── functional-folder-structure.md
│       ├── presentation-script.md
│       └── session-summary-full.md
│
├── mockups/                     # Design mockups
│   ├── current/                 # Latest version (currently v2) - Mobile-responsive (active)
│   │   ├── css/
│   │   │   └── styles.css      # Mobile-first responsive stylesheet
│   │   ├── js/
│   │   │   └── mobile-menu.js  # Mobile navigation JavaScript
│   │   ├── assets/             # Logo files and placeholder images
│   │   └── *.html              # 26 HTML mockup pages (mobile-optimized)
│   ├── v1/                     # Version 1 - Original desktop (archived)
│   │   ├── css/
│   │   │   └── styles.css      # Original stylesheet
│   │   ├── assets/             # Logo files and placeholder images
│   │   ├── screenshots/         # Page screenshots for reference
│   │   └── *.html              # 26 HTML mockup pages
│   └── v2/                     # Version 2 - Will be created when v3 is added
│   └── ...                     # Future versions (v3, v4, etc.)
│
└── assets/                      # Branding & assets
    └── branding/                # Logo and brand assets
        └── Logo/
            ├── 01 Inspiration Initial Designs/
            └── 02 Manus Generated Logos/
                ├── v1_all_gray/
                └── v2_accent_blade/
```

**Rationale:**
- **Centralized:** All documentation in one place
- **Complete:** Design assets (mockups, branding) alongside written docs
- **Organized:** Clear separation between guides, project docs, and specifications
- **Structured:** Specifications organized by type (design, technical, implementation, functional)
- **Versioned:** Mockups organized by version (current = v2 active, archive = v1 preserved)
- **Easy to find:** Developers know where to look for documentation

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
3. Review `docs/specification/technical/tech-stack-guide.md` for setup instructions
4. View `docs/mockups/current/` for design reference

**Finding code:**
- Frontend code: `apps/frontend/`
- Backend API: `apps/backend/api/`
- Scrapers: `apps/scraper/scrapers/`

**Finding documentation:**
- All docs: `docs/`
- Project docs: `docs/project/` (ai-context, runbook, ADRs, releases)
- Guides: `docs/guides/` (automation, workflow)
- Design system: `docs/specification/design/design-system.md`
- Tech stack: `docs/specification/technical/tech-stack-guide.md`
- Mockups: `docs/mockups/current/` (use current for mobile-responsive)

**Finding infrastructure:**
- Database migrations: `infrastructure/supabase/migrations/`
- CI/CD workflows: `infrastructure/.github/workflows/`

**Finding validation:**
- Validation scripts: `validation/scrapers/`
- Validation plan: `docs/specification/implementation/implementation-validation-plan.md`
- Validation results: `docs/specification/implementation/implementation-validation-notes.md`

### For Designers

**Design assets:**
- Branding: `docs/assets/branding/`
- Mockups: `docs/mockups/current/` (latest version)
- Design system: `docs/specification/design/design-system.md`
- Component library: `docs/specification/design/component-library.md`

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
- Designers know where to find mockups: `docs/mockups/current/`
- Everyone knows where docs are: `docs/`
- Clear organization: guides, project docs, and specifications are separated

---

## Migration Notes

This structure was adopted after the initial design phase. The following changes were made:

1. **Mockups reorganized:**
   - `mockups/` → `docs/mockups/v1/` (v1 archived)
   - `mockupsv2/` → `docs/mockups/current/` (v2 active, latest)
   - Future versions: When v3 is created, `current/` → `v2/`, new version → `current/`

2. **Branding moved:**
   - `branding/` → `docs/assets/branding/` (design assets belong with docs)

3. **Documentation reorganized:**
   - Project docs → `docs/project/` (ai-context, runbook, ADRs, releases)
   - Guides → `docs/guides/` (automation, workflow)
   - Specifications → `docs/specification/` organized by type (design, technical, implementation, functional)

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
| Documentation | `docs/` |
| Project docs | `docs/project/` |
| Guides | `docs/guides/` |
| Specifications | `docs/specification/` |
| Mockups (latest) | `docs/mockups/current/` |
| Mockups v1 | `docs/mockups/v1/` |
| Mockups v2 | `docs/mockups/v2/` (when v3 is created) |
| Branding assets | `docs/assets/branding/` |
| Project config | Root directory |

---

**Last Updated:** 2026-01-15  
**Structure Version:** 2.0 (reorganized documentation structure)
