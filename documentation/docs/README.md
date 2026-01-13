# ShutterZilla Documentation

This folder contains comprehensive documentation for the ShutterZilla platform, intended for handoff to Cursor AI (or any development team) for implementation.

## Contents

| Document | Description |
|---|---|
| **[tech-stack-guide.md](./tech-stack-guide.md)** | Comprehensive tech stack guide with all decisions, Q&A, examples, and implementation details. |
| **[tech-stack-final.md](./tech-stack-final.md)** | Finalized tech stack reference document with complete summary. |
| **[design-system.md](./design-system.md)** | Color palette, typography, spacing, border radius, shadows, and logo usage guidelines. |
| **[page-inventory.md](./page-inventory.md)** | Complete list of all 26 pages with their file names, purposes, and a sitemap. |
| **[functional-requirements.md](./functional-requirements.md)** | Detailed functional requirements for each section of the platform (Auth, Scraper, Collection, Admin). |
| **[component-library.md](./component-library.md)** | Reference for reusable UI components (top bar, footer, cards, badges, buttons, etc.). |
| **[data-models.md](./data-models.md)** | Suggested data models for the backend (User, CameraListing, SavedSearch, CollectionCamera). |
| **[key-decisions-log.md](./key-decisions-log.md)** | Log of key design and architectural decisions made during prototyping and tech stack selection. |
| **[folder-structure.md](./folder-structure.md)** | Complete guide to the project's folder structure, organization rationale, and navigation. |

## How to Use with Cursor AI

1.  Open the `shutterzilla` project folder in Cursor AI.
2.  Point Cursor to the `documentation` folder (which includes all mockups and branding assets).
3.  Use the documentation as context for generating implementation code.
4.  The HTML/CSS mockups in `../mockupsv2/` provide a visual reference and can be used as a starting point for component development.
5.  Reference the [tech-stack-guide.md](./tech-stack-guide.md) for all technology decisions and implementation details.

## Mockups

The project includes **26 HTML/CSS pages** that serve as the visual specification for the platform. These are fully styled and interactive prototypes.

**Mockup Versions:**

| Folder | Description |
|---|---|
| `../mockupsv2/` | **Mobile-responsive versions** - Optimized for mobile, tablet, and desktop. Recommended for implementation reference. |
| `../mockupsv1/` | Original desktop-focused mockups - Preserved for reference. |

**Key Files:**

| Folder/File | Description |
|---|---|
| `../mockupsv2/css/styles.css` | Mobile-first stylesheet with responsive design system CSS variables and component styles. |
| `../mockupsv2/js/mobile-menu.js` | JavaScript for mobile navigation menu. |
| `../mockupsv2/assets/` | Logo files and placeholder camera images. |
| `../mockupsv1/css/styles.css` | Original stylesheet (desktop-focused). |
| `../mockupsv1/assets/` | Original logo files and placeholder camera images. |
| `../mockupsv1/screenshots/` | Screenshots of each page for quick reference. |

**Live Mockups:**
- [Live Mockups v2](https://akamlibehsafe.github.io/shutterzilla/documentation/mockupsv2/landing-page.html) - Mobile-responsive versions
- [Original Mockups v1](https://akamlibehsafe.github.io/shutterzilla/documentation/mockupsv1/landing-page.html) - Original desktop versions

## Quick Start for Developers

1.  **Review the Tech Stack:** Start with [tech-stack-guide.md](./tech-stack-guide.md) to understand all technology decisions, setup, and architecture.
2.  **Review the Design System:** Read [design-system.md](./design-system.md) to understand the color palette, typography, and spacing.
3.  **Understand the Page Structure:** Use [page-inventory.md](./page-inventory.md) to see the full list of pages and their relationships.
4.  **Check Functional Requirements:** Refer to [functional-requirements.md](./functional-requirements.md) for what each page should do.
5.  **Build Components:** Use [component-library.md](./component-library.md) and `../mockupsv2/css/styles.css` to build reusable UI components.
6.  **Model the Data:** Use [data-models.md](./data-models.md) as a starting point for your database schema.
7.  **View Mockups:** Browse the [live mockups](https://akamlibehsafe.github.io/shutterzilla/documentation/mockupsv2/landing-page.html) to see the visual design.
