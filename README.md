# ShutterZilla

Modern apps for your vintage cameras. Discover, collect, and manage your film camera collection with powerful tools designed for enthusiasts.

## Overview

ShutterZilla is a comprehensive platform for vintage camera enthusiasts, featuring:

- **Scraper App**: Aggregates camera listings from multiple sources (Mercari, Buyee, eBay, JD Direct) with saved search functionality
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

For detailed tech stack information, see [Tech Stack Guide](./documentation/docs/tech-stack-guide.md).

## Project Status

- ✅ Design & Mockups Complete (26 pages)
- ✅ Mobile-Responsive Mockups (mockupsv2)
- ✅ Tech Stack Defined
- 🚧 Implementation In Progress

## Documentation

Comprehensive documentation is available in the [`documentation/`](./documentation/) folder:

- **[Documentation Index](./documentation/docs/README.md)** - Complete list of all documentation files
- **[Tech Stack Guide](./documentation/docs/tech-stack-guide.md)** - Complete tech stack guide with all decisions, Q&A, and examples
- **[Design System](./documentation/docs/design-system.md)** - Color palette, typography, spacing, and visual guidelines
- **[Folder Structure](./documentation/docs/folder-structure.md)** - Project organization and navigation guide

See [documentation/docs/README.md](./documentation/docs/README.md) for the complete documentation index.

## Live Mockups

- **[Live Mockups v2](https://akamlibehsafe.github.io/shutterzilla/documentation/mockupsv2/landing-page.html)** - Mobile-responsive versions of all pages
- **[Original Mockups v1](https://akamlibehsafe.github.io/shutterzilla/documentation/mockupsv1/landing-page.html)** - Original desktop-focused mockups

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
├── documentation/          # Project documentation
│   ├── mockupsv1/         # Original desktop HTML/CSS mockups
│   ├── mockupsv2/         # Mobile-responsive HTML/CSS mockups
│   └── branding/          # Logo and branding assets
└── README.md
```

## Quick Start

1. **Read this README** - Understand what ShutterZilla is
2. **Check Documentation** - See [documentation/docs/README.md](./documentation/docs/README.md) for all available docs
3. **Review Tech Stack** - Read [tech-stack-guide.md](./documentation/docs/tech-stack-guide.md) for setup instructions
4. **View Mockups** - Browse [Live Mockups v2](https://akamlibehsafe.github.io/shutterzilla/documentation/mockupsv2/landing-page.html)

## Development

This project uses:
- **Vue 3** for the frontend
- **Node.js + TypeScript** for the backend API
- **Supabase** for database, auth, and storage
- **Vercel** for hosting
- **GitHub Actions** for scheduled scraping tasks

See [tech-stack-guide.md](./documentation/docs/tech-stack-guide.md) for detailed setup instructions.

## License

[Add license information here]

## Links

- **GitHub Pages**: https://akamlibehsafe.github.io/shutterzilla/
- **Documentation**: [documentation/docs/README.md](./documentation/docs/README.md)
