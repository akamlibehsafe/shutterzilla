# ShutterZilla Runbook

Operations guide for installation, troubleshooting, recovery, and common issues.

## Table of Contents

- [Installation](#installation)
- [Uninstallation](#uninstallation)
- [Local Development Setup](#local-development-setup)
- [Troubleshooting](#troubleshooting)
- [Recovery Procedures](#recovery-procedures)
- [Known Gotchas](#known-gotchas)
- [Environment Variables](#environment-variables)

---

## Installation

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+ (for scraping)
- **Git**
- **Supabase account** (free tier)
- **Vercel account** (free tier)
- **GitHub account**

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/akamlibehsafe/shutterzilla.git
   cd shutterzilla
   ```

2. **Set up Supabase projects**
   - Create two Supabase projects: `shutterzilla-dev` and `shutterzilla-prod`
   - Note the project URLs and API keys
   - Set up authentication providers (Google, Facebook OAuth) if needed

3. **Set up Vercel project**
   - Connect repository to Vercel
   - Configure environment variables (see [Environment Variables](#environment-variables))
   - Vercel will auto-deploy from `main` branch

4. **Install frontend dependencies** (when frontend exists)
   ```bash
   cd apps/frontend
   npm install
   ```

5. **Install backend dependencies** (when backend exists)
   ```bash
   cd apps/backend
   npm install
   ```

6. **Install scraper dependencies**
   ```bash
   cd apps/scraper
   pip install -r requirements.txt
   ```

7. **Set up GitHub Actions**
   - Scraper workflow is in `.github/workflows/`
   - Configure secrets: `SUPABASE_URL`, `SUPABASE_KEY`
   - Workflow runs automatically on schedule (every 4 hours)

### Database Setup

1. **Apply migrations**
   ```bash
   # Connect to dev Supabase project
   # Apply migrations from infrastructure/supabase/migrations/
   ```

2. **Set up RLS (Row Level Security) policies**
   - Configure in Supabase dashboard or via migrations

---

## Uninstallation

### Removing Local Development

1. **Stop local servers** (Ctrl+C)
2. **Remove node_modules** (optional)
   ```bash
   rm -rf apps/frontend/node_modules
   rm -rf apps/backend/node_modules
   ```

3. **Remove Python virtual environment** (if used)
   ```bash
   deactivate  # if activated
   rm -rf venv
   ```

### Removing Cloud Resources

⚠️ **Warning**: This will delete all data. Only do this if you're sure.

1. **Supabase**
   - Delete projects in Supabase dashboard
   - Data will be permanently deleted

2. **Vercel**
   - Delete project in Vercel dashboard
   - Or disconnect repository (project remains but no auto-deploy)

3. **GitHub Actions**
   - Delete workflow files from `.github/workflows/`
   - Secrets can remain (no active workflows using them)

---

## Local Development Setup

### Frontend Development

```bash
cd apps/frontend
npm run dev  # Starts Vite dev server (usually http://localhost:5173)
```

### Backend Development

```bash
cd apps/backend
vercel dev  # Starts local serverless functions
# or
npm run dev
```

### Database Development

- Use `shutterzilla-dev` Supabase project
- Apply migrations to dev project first
- Use Supabase dashboard for schema inspection

### Scraper Development

```bash
cd apps/scraper
# Test locally
python scrapers/test_buyee_playwright.py

# Run full scraper (if implemented)
python main.py
```

### Environment Variables

Create `.env.local` files as needed:
- `apps/frontend/.env.local`
- `apps/backend/.env.local`
- `apps/scraper/.env.local`

See [Environment Variables](#environment-variables) section for required variables.

---

## Troubleshooting

### Frontend Issues

**Problem**: `npm run dev` fails
- **Solution**: Check Node.js version (need 18+), try `rm -rf node_modules package-lock.json && npm install`

**Problem**: Vite dev server not starting
- **Solution**: Check if port 5173 is in use: `lsof -i :5173`, kill process or change port in `vite.config.js`

**Problem**: Build fails on Vercel
- **Solution**: Check Vercel logs, ensure all dependencies in `package.json`, check Node.js version in Vercel settings

### Backend Issues

**Problem**: API requests failing
- **Solution**: Check environment variables in Vercel dashboard, verify Supabase URL/key, check CORS settings

**Problem**: Authentication not working
- **Solution**: Verify Supabase Auth configuration, check OAuth redirect URLs in Supabase dashboard

### Database Issues

**Problem**: Connection refused
- **Solution**: Check Supabase project URL and API key, verify project is active (not paused), check network connection

**Problem**: Migration fails
- **Solution**: Check migration SQL syntax, verify permissions, check if tables already exist, rollback previous migration if needed

### Scraper Issues

**Problem**: GitHub Actions scraper fails
- **Solution**: Check Actions logs, verify secrets (`SUPABASE_URL`, `SUPABASE_KEY`), check Python version (need 3.11+), verify Playwright browsers installed

**Problem**: Scraper can't access website
- **Solution**: Check if website structure changed (selector updates needed), verify no rate limiting/blocking, check Playwright wait times

**Problem**: Playwright browsers missing in GitHub Actions
- **Solution**: Add `playwright install` step in workflow, or use `playwright install --with-deps` in setup

### Email Issues

**Problem**: Emails not sending
- **Solution**: Check Resend API key in environment variables, verify domain verification in Resend dashboard, check SPF/DKIM records

**Problem**: Emails going to spam
- **Solution**: Verify SPF/DKIM records in DNS, check Resend domain status, review email content (avoid spam trigger words)

---

## Recovery Procedures

### Database Recovery

**Backup database**:
```bash
# Use Supabase dashboard to export data
# Or use pg_dump if direct database access available
```

**Restore from backup**:
```bash
# Use Supabase dashboard to import
# Or use psql if direct database access available
```

**Rollback migration**:
1. Create new migration that reverses changes
2. Apply to Supabase project
3. Or manually edit via Supabase dashboard (not recommended)

### Deployment Recovery

**Revert to previous Vercel deployment**:
1. Go to Vercel dashboard
2. Find previous successful deployment
3. Click "Promote to Production"

**Rollback Git commit**:
```bash
git revert <commit-hash>
git push origin main
# Vercel will auto-deploy rollback
```

### Scraper Recovery

**Clear scraper errors**:
- Check GitHub Actions logs for specific errors
- Update scraper code if website structure changed
- Verify database connection still works

**Re-run failed scraper**:
- Manually trigger GitHub Actions workflow
- Or wait for next scheduled run (every 4 hours)

---

## Known Gotchas

### General

1. **Supabase free tier pauses after inactivity**
   - Solution: Keep dev project active by using it regularly, or upgrade to Pro ($25/month)

2. **GitHub Actions has monthly minute limits**
   - Free tier: 2,000 minutes/month
   - Current usage: ~900 minutes/month (6 runs/day × 5 min × 30 days)
   - If exceeded: Wait for next month or upgrade

3. **Vercel preview URLs expire**
   - Feature branch previews are temporary
   - Use production URL (`main` branch) for permanent links

4. **Environment variables must be set in Vercel**
   - Local `.env.local` files don't work in production
   - Set all required vars in Vercel dashboard

### Development

1. **Supabase migrations are cloud-only**
   - No local Docker setup (decision: see ADR)
   - Requires internet connection for development
   - Dev project is separate from prod

2. **Python dependencies must be in `requirements.txt`**
   - GitHub Actions installs from `requirements.txt`
   - Don't forget to add new packages

3. **Playwright browsers are large**
   - First GitHub Actions run may be slow (installing browsers)
   - Consider caching Playwright browsers in workflow

### Deployment

1. **`main` branch = production**
   - No separate staging environment
   - Test on preview URLs before merging to main
   - See ADR 0005 for rationale

2. **Database migrations are manual**
   - Apply to dev project first
   - Test thoroughly
   - Then apply to prod project
   - Consider migration rollback plan

---

## Environment Variables

### Frontend (`.env.local`)

```bash
VITE_SUPABASE_URL=your-supabase-project-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_SENTRY_DSN=your-sentry-dsn  # Optional
```

### Backend (Vercel environment variables)

```bash
SUPABASE_URL=your-supabase-project-url
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
RESEND_API_KEY=your-resend-api-key
SENTRY_DSN=your-sentry-dsn  # Optional
```

### Scraper (GitHub Actions secrets)

```bash
SUPABASE_URL=your-supabase-project-url
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
```

### Supabase Environment Variables

Set in Supabase dashboard under Project Settings → API:
- Project URL
- `anon` key (public)
- `service_role` key (secret, backend only)

---

## Getting Help

- **Documentation**: Check `docs/specification/` for detailed docs
- **Tech Stack**: See `docs/specification/tech-stack-guide.md`
- **Decisions**: See `docs/decisions/` for ADRs
- **Issues**: Create GitHub issue or check existing issues

---

**Last Updated**: 2026-01-15
