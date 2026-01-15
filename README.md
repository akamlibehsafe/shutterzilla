# ShutterZilla

Modern apps for your vintage cameras. Discover, collect, and manage your film camera collection with powerful tools designed for enthusiasts.

## Overview

ShutterZilla is a comprehensive platform for vintage camera enthusiasts, featuring:

- **Scraper App**: Aggregates camera listings from Buyee and eBay with saved search functionality
- **Collection App**: Personal camera collection management with statistics and detailed tracking
- **Admin Dashboard**: System administration, user management, and scraper configuration

## Tech Stack

**Frontend:** Vue 3 + Vite + TypeScript + Tailwind CSS  
**Backend:** Node.js + Express + TypeScript  
**Database:** PostgreSQL on Supabase  
**Authentication:** Supabase Auth (Email/Password + OAuth)  
**Hosting:** Vercel (Frontend + API)  
**Scraping:** Python + GitHub Actions  
**Email:** Resend (sending) + Zoho Mail (receiving)  
**Monitoring:** Sentry + Vercel Analytics  

**Total Monthly Cost:** $0 (free tiers for up to 10 users)

For detailed tech stack information, see [Tech Stack Guide](./docs/specification/technical/tech-stack-guide.md).

## Project Status

- ✅ Design & Mockups Complete (26 pages)
- ✅ Mobile-Responsive Mockups (mockupsv2)
- ✅ Tech Stack Defined
- 🚧 Implementation In Progress

## Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) folder:

- **[CHANGELOG](./CHANGELOG.md)** - User-facing "what changed" per release
- **[AI Context](./docs/project/ai-context.md)** - Quick briefing for AI assistants and new contributors
- **[Runbook](./docs/project/runbook.md)** - Operations guide (installation, troubleshooting, recovery)
- **[Architecture Decision Records](./docs/project/decisions/)** - Technical and product decisions ("why we did X instead of Y")
- **[Documentation Index](./docs/README.md)** - Complete list of all documentation files
- **[Tech Stack Guide](./docs/specification/technical/tech-stack-guide.md)** - Complete tech stack guide with all decisions, Q&A, and examples
- **[Design System](./docs/specification/design/design-system.md)** - Color palette, typography, spacing, and visual guidelines
- **[Automation Guide](./docs/guides/automation.md)** - How to automate documentation maintenance

See [docs/README.md](./docs/README.md) for the complete documentation index.

## Live Mockups

- **[Live Mockups v2](https://akamlibehsafe.github.io/shutterzilla/docs/mockups/current/landing-page.html)** - Mobile-responsive versions of all pages
- **[Original Mockups v1](https://akamlibehsafe.github.io/shutterzilla/docs/mockups/archive/landing-page.html)** - Original desktop-focused mockups

## Project Structure

```
shutterzilla/
├── apps/                   # Application code
│   ├── frontend/          # Vue.js application (to be implemented)
│   ├── backend/           # API serverless functions (to be implemented)
│   └── scraper/           # Python scraping service (to be implemented)
├── infrastructure/         # Infrastructure as code
│   ├── supabase/          # Database migrations (to be implemented)
│   └── .github/            # GitHub Actions workflows
├── docs/                   # Project documentation
│   ├── guides/            # Process & workflow documentation
│   ├── project/           # Project-specific docs (ai-context, runbook, decisions, releases)
│   ├── specification/     # Technical specifications (design, technical, implementation, functional)
│   ├── mockups/           # Design mockups (current/active, archive/old)
│   └── assets/            # Branding and other assets
├── scripts/                # Helper scripts for documentation
├── validation/             # Scraper validation tests
└── README.md
```

## Quick Start

1. **Read this README** - Understand what ShutterZilla is
2. **Quick Start** - Read [AI Context](./docs/project/ai-context.md) for project overview
3. **Setup** - Follow [Runbook](./docs/project/runbook.md) for installation and troubleshooting
4. **Check Documentation** - See [docs/README.md](./docs/README.md) for all available docs
5. **View Mockups** - Browse [Live Mockups v2](https://akamlibehsafe.github.io/shutterzilla/docs/mockups/current/landing-page.html)

## Development

This project uses:
- **Vue 3** for the frontend
- **Node.js + TypeScript** for the backend API
- **Supabase** for database, auth, and storage
- **Vercel** for hosting
- **GitHub Actions** for scheduled scraping tasks

See [tech-stack-guide.md](./docs/specification/technical/tech-stack-guide.md) for detailed setup instructions.

## License

[Add license information here]

## Links

- **GitHub Pages**: https://akamlibehsafe.github.io/shutterzilla/
- **Documentation**: [docs/README.md](./docs/README.md)
- **Changelog**: [CHANGELOG.md](./CHANGELOG.md)
- **ADRs**: [docs/project/decisions/](./docs/project/decisions/)
