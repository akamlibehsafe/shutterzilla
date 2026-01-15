# ShutterZilla Tech Stack - Finalized

**Project Scale:** Friends/family project, max 10 users  
**Priority:** Free tiers and cost-effective solutions  
**Total Monthly Cost:** $0

---

## Complete Tech Stack

### Frontend
- **Vue 3** with Composition API
- **Vite** - Build tool and dev server
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Hosting:** Vercel (free tier: unlimited personal projects)

### Backend
- **Node.js** with **TypeScript**
- **Express.js** - Web framework
- **Prisma** - ORM and database toolkit
- **Zod** - Runtime type validation
- **Hosting:** Vercel serverless functions (free tier: 100GB-hours/month)

### Database
- **PostgreSQL** on **Supabase**
- **Two projects:** 
  - `shutterzilla-dev` (development)
  - `shutterzilla-prod` (production)
- **Migrations:** Stored in GitHub (`supabase/migrations/`)
- **Free tier:** 500MB database, 1GB file storage per project

### Authentication
- **Supabase Auth** - Handles all authentication
- **Sign-up options:**
  - Email/Password (default)
  - Google OAuth (included from start)
  - Facebook OAuth (included from start)
- **JWT tokens** - Stateless authentication
- **Email verification** - Via Resend (configured in Supabase)
- **Password reset** - Built-in

### Web Scraping
- **Python 3.11+** - Scraping language
- **BeautifulSoup/Playwright** - Scraping libraries
- **GitHub Actions** - Scheduled execution
- **Schedule:** Every 4 hours (configurable)
- **Free tier:** 2,000 minutes/month (more than enough)

### Email Service

#### Sending (Automated Emails)
- **Resend** - Email API
- **Free tier:** 3,000 emails/month, 100 emails/day
- **Use for:** Verification emails, password resets, search notifications
- **Domain:** Configured to send from `noreply@shutterzilla.com` and `hello@shutterzilla.com`

#### Receiving (Support Emails)
- **Zoho Mail Free** - Email hosting
- **Setup:** `hello@shutterzilla.com` on Zoho Mail
- **Forwarding:** Auto-forwards to personal Gmail
- **Sending:** Gmail "Send mail as" configured with Zoho SMTP
- **Result:** All emails in Gmail, no Zoho app needed
- **DNS:** MX records added to Vercel DNS

### File Storage
- **Supabase Storage** - Included with Supabase
- **Free tier:** 1GB storage, 2GB bandwidth/month
- **Use for:** User-uploaded camera photos in Collection app

### Monitoring & Observability

#### Error Tracking
- **Sentry** - Error tracking and monitoring
- **Free tier:** 5,000 events/month, 1 project
- **Tracks:** Frontend errors (Vue.js), backend errors (API), crashes

#### Analytics
- **Vercel Analytics** - Page views and performance
- **Free tier:** Built-in, automatic
- **Tracks:** Page views, load times, user locations

#### Logs
- **Vercel Logs** - Function execution logs
- **Free tier:** Built-in, automatic
- **Tracks:** API requests, function execution, errors

#### Uptime Monitoring
- **UptimeRobot** - Site uptime checks
- **Free tier:** 50 monitors, 5-minute intervals
- **Tracks:** Site availability, response times

### Hosting Architecture

```
GitHub Repository (single source of truth)
    │
    ├─→ Vercel (auto-deploys on git push)
    │   ├─→ Frontend (Vue.js SPA)
    │   └─→ Backend API (serverless functions)
    │
    └─→ GitHub Actions (runs on schedule)
        └─→ Python Scraper → Supabase Database
```

**Deployment Strategy:**
- **Production:** `main` branch → Auto-deploys to production
- **Preview:** Feature branches → Preview deployments (test URLs)
- **Database:** Migrations in GitHub, applied to dev/prod Supabase projects

---

## Project Structure

```
shutterzilla/
├── apps/                   # Application code
│   ├── frontend/          # Vue.js application
│   │   ├── src/
│   │   │   ├── components/   # Vue components
│   │   │   ├── views/        # Page views
│   │   │   ├── router/       # Vue Router config
│   │   │   ├── stores/       # Pinia stores
│   │   │   └── main.js       # App entry point
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   ├── backend/           # API serverless functions
│   │   └── api/
│   │       ├── login.js
│   │       ├── cameras.js
│   │       └── collections.js
│   │
│   └── scraper/           # Python scraping service
│       ├── main.py
│       ├── scrapers/
│       │   ├── ebay.py
│       │   └── buyee.py
│       ├── utils/
│       │   └── database.py
│       └── requirements.txt
│
├── infrastructure/         # Infrastructure as code
│   ├── supabase/          # Database migrations
│   │   └── migrations/
│   │       ├── 20240101000000_initial_schema.sql
│   │       └── ...
│   │
│   └── .github/           # GitHub Actions workflows
│       └── workflows/
│           └── scraper.yml   # GitHub Actions scraper
│
├── documentation/         # Project documentation
│   ├── mockupsv1/        # Original desktop mockups
│   ├── mockupsv2/        # Mobile-responsive mockups
│   └── branding/         # Logo and brand assets
│
└── ../README.md
```

---

## Environment Setup

### Development Environment
- **Frontend:** `npm run dev` (Vite dev server)
- **Backend:** Vercel dev (local serverless functions)
- **Database:** Supabase dev project (cloud)
- **Environment variables:** `.env.local`

### Production Environment
- **Frontend:** Vercel (auto-deployed from `main` branch)
- **Backend:** Vercel serverless functions
- **Database:** Supabase prod project (cloud)
- **Environment variables:** Set in Vercel dashboard

---

## Key Technologies Summary

| Component | Technology | Free Tier | Notes |
|-----------|-----------|-----------|-------|
| **Frontend Framework** | Vue 3 + Vite | ✅ Free | You specified Vue |
| **State Management** | Pinia | ✅ Free | Vue's official state management |
| **Backend Runtime** | Node.js + Express | ✅ Free | Same language as frontend |
| **Database** | PostgreSQL (Supabase) | ✅ 500MB free | Includes auth + storage |
| **File Storage** | Supabase Storage | ✅ 1GB free | Included with Supabase |
| **Authentication** | Supabase Auth | ✅ Free | Email/password + OAuth |
| **Email Sending** | Resend | ✅ 3,000/month | Automated emails |
| **Email Receiving** | Zoho Mail | ✅ Free | Forwards to Gmail |
| **Scraping** | Python + GitHub Actions | ✅ 2,000 min/month | Scheduled tasks |
| **Hosting** | Vercel | ✅ Free | Unlimited personal projects |
| **Error Tracking** | Sentry | ✅ 5,000 events/month | Error monitoring |
| **Analytics** | Vercel Analytics | ✅ Free | Built-in |
| **Logs** | Vercel Logs | ✅ Free | Built-in |
| **Uptime** | UptimeRobot | ✅ 50 monitors | Optional |

**Total Monthly Cost: $0** ✅

---

## Development Workflow

### Daily Development
1. Create feature branch: `git checkout -b feature-name`
2. Make changes (with AI assistance)
3. Test locally
4. Push to branch → Vercel creates preview URL
5. Test preview URL
6. Merge to `main` → Production deploys automatically

### Database Changes
1. Create migration file: `supabase/migrations/YYYYMMDDHHMMSS_description.sql`
2. Test on dev Supabase project
3. Commit migration to GitHub
4. Apply to prod Supabase when ready

### Scraping Updates
1. Update Python scraper code
2. Commit to GitHub
3. GitHub Actions runs automatically on schedule
4. Check GitHub Actions logs for status

---

## DNS Configuration

**Current Setup:**
- **Domain Registrar:** Namecheap
- **DNS Management:** Vercel
- **Email Records:** Added to Vercel DNS

**DNS Records Needed:**
- **A/CNAME records:** For Vercel deployments (automatic)
- **MX records:** For Zoho Mail (hello@shutterzilla.com)
- **TXT records:** 
  - SPF/DKIM for Resend (sending emails)
  - Domain verification for Zoho Mail

---

## Security Considerations

- **HTTPS:** Automatic (Vercel provides SSL)
- **Password Hashing:** Handled by Supabase (bcrypt)
- **JWT Tokens:** Short-lived access tokens + refresh tokens
- **API Security:** Token verification on all protected routes
- **Rate Limiting:** Can be added with Express middleware
- **CORS:** Configured in Vercel/Vue.js

---

## Scaling Considerations

**Current setup supports:**
- 10 users comfortably
- All free tiers sufficient
- Room to grow within free tiers

**When to upgrade:**
- User base grows beyond free tier limits
- Need more database storage (>500MB)
- Need more email sending (>3,000/month)
- Need more error tracking (>5,000 events/month)

**Upgrade path:**
- Supabase Pro: $25/month (8GB database, 100GB storage)
- Resend Pro: $20/month (50,000 emails/month)
- Sentry Pro: $26/month (50,000 events/month)
- Vercel Pro: $20/month (more features)

**For now:** All free tiers are more than sufficient.

---

## Learning Resources

### Vue.js
- Official docs: vuejs.org
- Vue Router: router.vuejs.org
- Pinia: pinia.vuejs.org

### Supabase
- Official docs: supabase.com/docs
- Auth guide: supabase.com/docs/guides/auth
- Database guide: supabase.com/docs/guides/database

### Vercel
- Official docs: vercel.com/docs
- Serverless functions: vercel.com/docs/functions

### OAuth/Social Login
- OAuth 2.0 explained: oauth.net/2/
- Google OAuth: developers.google.com/identity/protocols/oauth2
- Facebook OAuth: developers.facebook.com/docs/facebook-login

---

## Next Steps

1. **Set up development environment**
2. **Create Supabase projects** (dev + prod)
3. **Set up Vercel project**
4. **Configure OAuth providers** (Google, Facebook)
5. **Set up email** (Resend + Zoho Mail)
6. **Initialize Vue.js project**
7. **Set up database migrations**
8. **Create GitHub Actions workflow** for scraper

---

**This tech stack is finalized and ready for implementation.**
