# 0006 - Use Python + GitHub Actions for Web Scraping

## Status
Accepted

## Context
Need scheduled web scraping for camera listings from:
- Buyee (Japan)
- eBay (USA)

Requirements:
- Run every 4 hours (6 times per day)
- Store results in PostgreSQL (Supabase)
- Handle JavaScript-rendered pages (some sites need Playwright)
- No dedicated server budget (free tier only)

## Decision
Use Python 3.11+ with BeautifulSoup/Playwright for scraping, scheduled via GitHub Actions (free tier: 2,000 minutes/month).

## Alternatives considered
- **Node.js + Vercel Cron**: Pros - same language as backend. Cons - serverless functions have timeouts (10s), no persistent browser, more expensive
- **Dedicated server + cron**: Pros - full control. Cons - server costs money, need to maintain server
- **Cloud Functions (AWS Lambda/Google Cloud)**: Pros - serverless. Cons - more complex setup, billing complexity, timeouts
- **Python + GitHub Actions**: Pros - free tier (2,000 min/month), can run Playwright, persistent execution, easy scheduling, all code in one repo. Cons - tied to GitHub (but already using GitHub)

## Consequences
- No additional infrastructure cost (free GitHub Actions)
- Can run long-running scrapers (no 10s timeout)
- Playwright support for JavaScript-heavy sites
- All code in same repository (easier to maintain)
- Easy scheduling via GitHub Actions cron syntax
- Can test locally before committing
- Free tier more than sufficient (6 runs/day × 5 min = 30 min/day = 900 min/month)

## Links
- Tech Stack Final: `docs/specification/tech-stack-final.md`
- Scraper Behavior Spec: `docs/specification/implementation-scraper-behavior-specification.md`
- Validation: `validation/README.md`
