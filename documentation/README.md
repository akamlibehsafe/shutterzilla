# ShutterZilla Documentation

This folder contains comprehensive documentation for the ShutterZilla platform, intended for handoff to Cursor AI (or any development team) for implementation.

## Contents

| Document | Description |
|---|---|
| **[design-system.md](./design-system.md)** | Color palette, typography, spacing, border radius, shadows, and logo usage guidelines. |
| **[page-inventory.md](./page-inventory.md)** | Complete list of all 26 pages with their file names, purposes, and a sitemap. |
| **[functional-requirements.md](./functional-requirements.md)** | Detailed functional requirements for each section of the platform (Auth, Scraper, Collection, Admin). |
| **[component-library.md](./component-library.md)** | Reference for reusable UI components (top bar, footer, cards, badges, buttons, etc.). |
| **[data-models.md](./data-models.md)** | Suggested data models for the backend (User, CameraListing, SavedSearch, CollectionCamera). |
| **[key-decisions-log.md](./key-decisions-log.md)** | Log of key design and architectural decisions made during prototyping. |

## How to Use with Cursor AI

1.  Open the `shutterzilla` project folder in Cursor AI.
2.  Point Cursor to this `documentation` folder and the `mockups` folder.
3.  Use the documentation as context for generating implementation code.
4.  The HTML/CSS mockups in `mockups/` provide a visual reference and can be used as a starting point for component development.

## Mockups

The `mockups/` folder contains **26 HTML/CSS pages** that serve as the visual specification for the platform. These are fully styled and interactive prototypes.

**Key Folders:**

| Folder/File | Description |
|---|---|
| `mockups/css/styles.css` | The main stylesheet containing the design system CSS variables and component styles. |
| `mockups/assets/` | Logo files and placeholder camera images. |
| `mockups/screenshots/` | Screenshots of each page for quick reference. |

## Quick Start for Developers

1.  **Review the Design System:** Start with `design-system.md` to understand the color palette, typography, and spacing.
2.  **Understand the Page Structure:** Use `page-inventory.md` to see the full list of pages and their relationships.
3.  **Check Functional Requirements:** Refer to `functional-requirements.md` for what each page should do.
4.  **Build Components:** Use `component-library.md` and `styles.css` to build reusable UI components.
5.  **Model the Data:** Use `data-models.md` as a starting point for your database schema.
