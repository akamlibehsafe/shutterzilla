# AI / Contributor Context (ShutterZilla)

**Last Updated**: 2026-01-15

Quick briefing for AI assistants, new contributors, and team members joining the project.

---

## Goal

ShutterZilla is a platform for vintage camera enthusiasts to:
- **Discover cameras**: Scrape and browse listings from Buyee (Japan) and eBay (USA)
- **Manage collections**: Track personal camera inventory with statistics and wishlist
- **Save searches**: Get notified when new listings match saved search criteria

**Scale**: Friends/family project, max 10 users  
**Cost**: $0/month (all free tiers)  
**Status**: Mockups complete, implementation in progress

---

## Key Workflows

### Install
1. Clone repo: `git clone https://github.com/akamlibehsafe/shutterzilla.git`
2. Set up Supabase projects (dev + prod)
3. Connect to Vercel (auto-deploy from GitHub)
4. Install dependencies: `npm install` (frontend/backend), `pip install -r requirements.txt` (scraper)
5. Configure environment variables (see `docs/project/runbook.md`)

### Uninstall
- Local: Stop servers, optionally remove `node_modules`
- Cloud: Delete Supabase projects, delete Vercel project (⚠️ deletes data)

### Create from Local/Remote
- **Local dev**: `npm run dev` (frontend), `vercel dev` (backend), `python main.py` (scraper)
- **Remote deploy**: Push to `main` → Vercel auto-deploys production
- **Preview deploy**: Push to feature branch → Vercel creates preview URL

### Push Flow
1. Create feature branch: `git checkout -b feature-name`
2. Make changes (with AI assistance)
3. Test locally or on preview URL
4. Push: `git push origin feature-name` (creates preview URL)
5. Merge to `main`: Auto-deploys to production

---

## Repo Layout

```
shutterzilla/
├── apps/                    # Application code
│   ├── frontend/           # Vue 3 + Vite + TypeScript (to be implemented)
│   ├── backend/            # Node.js + Express + TypeScript (to be implemented)
│   └── scraper/            # Python + Playwright (to be implemented)
├── infrastructure/          # Infrastructure as code
│   ├── supabase/           # Database migrations (to be implemented)
│   └── .github/            # GitHub Actions workflows
├── docs/                    # All documentation
│   ├── mockups/            # Design mockups
│   │   ├── current/       # Mobile-responsive mockups (26 pages)
│   │   └── archive/       # Original desktop mockups (26 pages)
│   ├── specification/     # Design specs, tech stack, implementation plans
│   ├── project/           # Project-specific docs
│   │   ├── decisions/     # ADRs (Architecture Decision Records)
│   │   ├── runbook.md     # Operations guide (this file's companion)
│   │   └── ai-context.md  # This file
│   └── branding/          # Logo and brand assets
├── validation/             # Scraper validation tests
└── README.md              # Project overview
```

**Key directories**:
- `apps/`: Application code (frontend, backend, scraper)
- `docs/specification/`: Design specs, tech stack, implementation plans
- `docs/project/decisions/`: ADRs documenting why we made key decisions
- `docs/mockups/current/` and `docs/mockups/v1/`: HTML/CSS mockups (reference for implementation)
- `validation/`: Scraper feasibility tests

---

## Invariants / Rules

### Compatibility
- **macOS/Linux**: Development tested on macOS, should work on Linux
- **Windows**: Not tested, may need adjustments (path separators, etc.)

### Shell Assumptions
- **zsh/bash**: Scripts assume Unix shell (zsh on macOS, bash on Linux)
- **Git**: Required for version control

### Safety Rules
- **No destructive ops without confirmation**: Always prompt before deleting data
- **Backup before major changes**: Especially database migrations
- **Test on preview URLs before merging**: Feature branches → preview URLs → test → merge to main
- **Database migrations**: Apply to dev first, test, then prod

### Code Organization
- **All `.md` files in `docs/specification/`**: Except README, release notes, and special files
- **ADRs in `docs/project/decisions/`**: Format: `NNNN-title.md` (e.g., `0001-teal-color.md`)
- **Changelog in root**: `CHANGELOG.md` (user-facing changes per release)

---

## Known Sharp Edges

### Common Failure Modes + Fixes

1. **Supabase free tier pauses**
   - **Symptom**: Database connection fails, project shows as paused
   - **Fix**: Reactivate project in Supabase dashboard, keep dev project active

2. **GitHub Actions scraper fails**
   - **Symptom**: Actions logs show errors
   - **Fix**: Check secrets (`SUPABASE_URL`, `SUPABASE_KEY`), verify Python version (3.11+), check Playwright installation

3. **Vercel build fails**
   - **Symptom**: Deployment shows build error
   - **Fix**: Check Vercel logs, verify Node.js version, check all dependencies in `package.json`

4. **Environment variables missing**
   - **Symptom**: API calls fail, auth doesn't work
   - **Fix**: Set required variables in Vercel dashboard (see `docs/project/runbook.md`)

5. **Scraper can't access website**
   - **Symptom**: Scraper returns empty results or errors
   - **Fix**: Website structure may have changed, update selectors, check rate limiting

### Gotchas

- **`main` branch = production**: No staging environment (see ADR 0005)
- **Supabase is cloud-only**: No local Docker (see ADR 0004), requires internet
- **Preview URLs expire**: Feature branch deployments are temporary
- **Database migrations are manual**: Apply to dev first, then prod

---

## Current Priorities

### What's Next
1. **Phase 0.2**: Scraping feasibility validation (test Buyee, eBay)
2. **Phase 1**: Complete tech stack setup (Supabase, Vercel, Vue.js)
3. **Phase 2**: Implement frontend (Vue.js app based on mockups)
4. **Phase 3**: Implement backend API (Express serverless functions)
5. **Phase 4**: Implement scraper (Python + GitHub Actions)

### What Not to Change
- **Tech stack decisions**: See ADRs in `docs/project/decisions/` for rationale
- **Deployment strategy**: `main` = production, branches = previews (see ADR 0005)
- **Cost model**: Stick to free tiers (max 10 users)
- **Documentation structure**: Keep ADRs in `docs/project/decisions/`, specs in `docs/specification/`

---

## Tech Stack Quick Reference

**Frontend**: Vue 3 + Vite + TypeScript + Tailwind CSS  
**Backend**: Node.js + Express + TypeScript  
**Database**: PostgreSQL on Supabase  
**Auth**: Supabase Auth (Email/Password + OAuth)  
**Hosting**: Vercel (Frontend + API)  
**Scraping**: Python + GitHub Actions  
**Email**: Resend (sending) + Zoho Mail (receiving)  
**Monitoring**: Sentry + Vercel Analytics

**Total Cost**: $0/month (free tiers)

---

## Decision Log

Key architectural decisions are documented in ADRs (`docs/project/decisions/`):
- 0001: Teal primary color scheme
- 0002: Split scraper/collection into two apps
- 0003: Vue.js for frontend
- 0004: Supabase for database/auth/storage
- 0005: Simplified deployment (main = prod)
- 0006: Python + GitHub Actions for scraping
- 0007: Limit scraping sources to Buyee and eBay
- 0008: Use Node.js + TypeScript for backend
- 0009: Use Prisma ORM
- 0010: Use Vercel for hosting
- 0011: Use Resend for email sending
- 0012: Use Zoho Mail + Gmail forwarding for email receiving
- 0013: Use Sentry for error tracking
- 0014: Use cloud Supabase (no local Docker)
- 0015: Include OAuth from start
- 0016: Use Tailwind CSS
- 0017: Prioritize free tier services
- 0018: Use Zod for runtime validation
- 0019: Use monorepo structure
- 0020: Use React Native for mobile apps
- 0021: DevOps environment strategy and project management

**Always check ADRs before making major architectural decisions.**

---

## Documentation Index

- **This file**: `docs/project/ai-context.md` (briefing for AI/contributors)
- **Runbook**: `docs/project/runbook.md` (operations, troubleshooting)
- **Changelog**: `CHANGELOG.md` (user-facing changes)
- **ADRs**: `docs/project/decisions/` (architectural decisions)
- **Tech Stack**: `docs/specification/technical/tech-stack-guide.md` (complete guide)
- **Implementation Plan**: `docs/specification/implementation/implementation-plan.md`
- **Design System**: `docs/specification/design/design-system.md`
- **Mockups**: `docs/mockups/current/` (v2), `docs/mockups/v1/` (v1) (26 pages each)

---

## Documentation Scripts

Helper scripts for maintaining documentation (in `scripts/`):
- `doc_new_adr` - Create new ADR
- `doc_update_changelog` - Add changelog entries
- `doc_check` - Check documentation status (runs in pre-commit hook)
- `doc_release` - Create new release from unreleased entries

**Quick reference**: See `docs/guides/quick-reference.md`  
**Complete workflow**: See `docs/guides/documentation-workflow.md`

## AI Assistant Guidelines

When helping with this project:

1. **Check ADRs first**: Before suggesting major changes, review `docs/project/decisions/`
2. **Follow existing patterns**: Match code style in mockups, follow folder structure
3. **Update docs as you go**: If making decisions, create ADRs; if adding features, update CHANGELOG
4. **Test on preview URLs**: Never merge directly to main without testing
5. **Respect free tier constraints**: Don't suggest paid services unless explicitly needed
6. **Keep it simple**: Solo dev + AI workflow favors simplicity over complexity

---

**For detailed setup instructions, see `docs/project/runbook.md`.**  
**For technical specifications, see `docs/specification/`.**  
**For architectural decisions, see `docs/project/decisions/`.**  
**For documentation workflow, see `docs/guides/documentation-workflow.md`.**
