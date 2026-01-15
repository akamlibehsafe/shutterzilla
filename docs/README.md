# ShutterZilla Documentation

This folder contains comprehensive documentation for the ShutterZilla platform, organized for easy navigation and maintenance.

## 📁 Documentation Structure

```
docs/
├── README.md                    # This file - documentation index
│
├── guides/                      # Process & workflow documentation
│   ├── automation.md            # How to automate documentation
│   ├── quick-reference.md       # Quick command reference
│   ├── documentation-workflow.md # Complete workflow guide
│   ├── quick-start-automation.md # Quick start for automation
│   └── migration/               # Migration documentation (archive)
│
├── project/                     # Project-specific documentation
│   ├── ai-context.md            # AI/contributor briefing
│   ├── runbook.md               # Operations guide
│   ├── decisions/               # Architecture Decision Records (ADRs)
│   └── releases/                # Release notes
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
│   │   └── key-decisions-log.md
│   └── functional/             # Functional specs
│       └── functional-requirements.md
│
├── mockups/                     # Design mockups
│   ├── current/                 # v2 - Mobile-responsive (active)
│   └── archive/                 # v1 - Original desktop (preserved)
│
└── assets/                      # Branding & assets
    └── branding/                # Logo and branding files
```

## 🚀 Quick Start

### For New Contributors
1. **Start here**: [AI Context](./project/ai-context.md) - Quick project overview
2. **Setup**: [Runbook](./project/runbook.md) - Installation and troubleshooting
3. **Tech Stack**: [Tech Stack Guide](./specification/technical/tech-stack-guide.md)
4. **Design**: [Design System](./specification/design/design-system.md)

### For Developers
1. **Tech Stack**: [Tech Stack Guide](./specification/technical/tech-stack-guide.md)
2. **Design System**: [Design System](./specification/design/design-system.md)
3. **Pages**: [Page Inventory](./specification/design/page-inventory.md)
4. **Requirements**: [Functional Requirements](./specification/functional/functional-requirements.md)
5. **Components**: [Component Library](./specification/design/component-library.md)
6. **Data Models**: [Data Models](./specification/technical/data-models.md)
7. **Mockups**: [Current Mockups](./mockups/current/) - Browse HTML files

### For Documentation Maintainers
1. **Quick Reference**: [Quick Reference](./guides/quick-reference.md)
2. **Workflow**: [Documentation Workflow](./guides/documentation-workflow.md)
3. **Automation**: [Automation Guide](./guides/automation.md)

## 📚 Documentation by Category

### Project Documentation

| Document | Location | Description |
|---------|----------|-------------|
| **AI Context** | [`project/ai-context.md`](./project/ai-context.md) | Quick briefing for AI assistants and new contributors |
| **Runbook** | [`project/runbook.md`](./project/runbook.md) | Operations guide (installation, troubleshooting, recovery) |
| **ADRs** | [`project/decisions/`](./project/decisions/) | Architecture Decision Records - "why we did X instead of Y" |
| **Releases** | [`project/releases/`](./project/releases/) | Release notes and version history |

### Design Specifications

| Document | Location | Description |
|---------|----------|-------------|
| **Design System** | [`specification/design/design-system.md`](./specification/design/design-system.md) | Color palette, typography, spacing, visual guidelines |
| **Component Library** | [`specification/design/component-library.md`](./specification/design/component-library.md) | Reusable UI components reference |
| **Page Inventory** | [`specification/design/page-inventory.md`](./specification/design/page-inventory.md) | Complete list of all 26 pages with sitemap |

### Technical Specifications

| Document | Location | Description |
|---------|----------|-------------|
| **Tech Stack Guide** | [`specification/technical/tech-stack-guide.md`](./specification/technical/tech-stack-guide.md) | Comprehensive tech stack guide with decisions, Q&A, examples |
| **Tech Stack Final** | [`specification/technical/tech-stack-final.md`](./specification/technical/tech-stack-final.md) | Finalized tech stack reference |
| **Data Models** | [`specification/technical/data-models.md`](./specification/technical/data-models.md) | Database schema and data models |
| **Folder Structure** | [`specification/technical/folder-structure.md`](./specification/technical/folder-structure.md) | Project folder organization guide |

### Implementation Documentation

| Document | Location | Description |
|---------|----------|-------------|
| **Implementation Plan** | [`specification/implementation/implementation-plan.md`](./specification/implementation/implementation-plan.md) | Step-by-step implementation plan |
| **Implementation Notes** | [`specification/implementation/implementation-notes.md`](./specification/implementation/implementation-notes.md) | Notes and learnings from implementation |
| **Key Decisions Log** | [`specification/implementation/key-decisions-log.md`](./specification/implementation/key-decisions-log.md) | Log of key design and architectural decisions |

### Functional Specifications

| Document | Location | Description |
|---------|----------|-------------|
| **Functional Requirements** | [`specification/functional/functional-requirements.md`](./specification/functional/functional-requirements.md) | Detailed functional requirements for each section |

### Process & Workflow Documentation

| Document | Location | Description |
|---------|----------|-------------|
| **Quick Reference** | [`guides/quick-reference.md`](./guides/quick-reference.md) | Quick command reference for documentation scripts |
| **Documentation Workflow** | [`guides/documentation-workflow.md`](./guides/documentation-workflow.md) | Complete workflow guide |
| **Automation Guide** | [`guides/automation.md`](./guides/automation.md) | How to automate documentation maintenance |

## 🎨 Mockups

The project includes **26 HTML/CSS pages** that serve as the visual specification.

| Folder | Description |
|--------|-------------|
| [`mockups/current/`](./mockups/current/) | **Latest version (v2)** - Mobile-responsive versions - Optimized for mobile, tablet, and desktop. **Recommended for implementation reference.** |
| [`mockups/v1/`](./mockups/v1/) | **Version 1** - Original desktop-focused mockups - Preserved for reference |

**Key Files:**
- `mockups/current/css/styles.css` - Mobile-first stylesheet with responsive design (v2)
- `mockups/current/js/mobile-menu.js` - JavaScript for mobile navigation (v2)
- `mockups/current/assets/` - Logo files and placeholder camera images (v2)
- `mockups/v1/` - Version 1 mockups (archived)

**Live Mockups:**
- [Live Mockups v2](https://akamlibehsafe.github.io/shutterzilmockupsv2/landing-page.html) - Mobile-responsive versions
- [Original Mockups v1](https://akamlibehsafe.github.io/shutterzilmockupsv1/landing-page.html) - Original desktop versions

## 🔗 External Links

- **GitHub Pages**: https://akamlibehsafe.github.io/shutterzilla/
- **Root README**: [../README.md](../README.md)
- **Changelog**: [../CHANGELOG.md](../CHANGELOG.md)

## 📝 How to Use with Cursor AI

1. Open the `shutterzilla` project folder in Cursor AI
2. Point Cursor to the `docs` folder (includes all mockups and branding assets)
3. Use the documentation as context for generating implementation code
4. The HTML/CSS mockups in `mockups/current/` provide visual reference
5. Reference the [tech-stack-guide.md](./specification/technical/tech-stack-guide.md) for all technology decisions

## 🎯 Development Workflow

1. **Review Tech Stack**: Start with [tech-stack-guide.md](./specification/technical/tech-stack-guide.md)
2. **Review Design System**: Read [design-system.md](./specification/design/design-system.md)
3. **Understand Pages**: Use [page-inventory.md](./specification/design/page-inventory.md)
4. **Check Requirements**: Refer to [functional-requirements.md](./specification/functional/functional-requirements.md)
5. **Build Components**: Use [component-library.md](./specification/design/component-library.md) and `mockups/current/css/styles.css`
6. **Model Data**: Use [data-models.md](./specification/technical/data-models.md) for database schema
7. **View Mockups**: Browse the [live mockups](https://akamlibehsafe.github.io/shutterzilmockupsv2/landing-page.html)
