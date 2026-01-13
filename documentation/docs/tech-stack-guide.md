# ShutterZilla Tech Stack Guide - Comprehensive

**Goal:** Build ShutterZilla with Vue.js frontend, keeping costs at **$0/month** for up to 10 users.

**Project Scale:** Friends/family project, max 10 users  
**Priority:** Free tiers and cost-effective solutions  
**Total Monthly Cost:** $0

**Context:** This guide assumes familiarity with LAMP stack (Linux, Apache, MySQL, PHP) and explains modern equivalents. It includes all options considered, questions asked, and decisions made.

---

## Table of Contents

1. [Frontend: Vue.js](#1-frontend-vuejs)
2. [Backend: Node.js + TypeScript](#2-backend-nodejs--typescript)
3. [Database: PostgreSQL on Supabase](#3-database-postgresql-on-supabase)
4. [Web Scraping: Python Scripts](#4-web-scraping-python-scripts)
5. [File Storage: Supabase Storage](#5-file-storage-supabase-storage)
6. [Email Service](#6-email-service)
7. [Hosting: Vercel](#7-hosting-vercel)
8. [Authentication: Supabase Auth](#8-authentication-supabase-auth)
9. [Monitoring & Observability](#9-monitoring--observability)
10. [Project Structure](#project-structure)
11. [Development Workflow](#development-workflow)
12. [Deployment Strategy](#deployment-strategy)
13. [Database Migrations](#database-migrations)
14. [DNS Configuration](#dns-configuration)
15. [Architecture Comparison](#architecture-comparison)
16. [Scaling Considerations](#scaling-considerations)
17. [Next Steps](#next-steps)

---

---

## 1. Frontend: Vue.js

### What is Vue.js?
Vue.js is a JavaScript framework for building user interfaces - similar to how jQuery made DOM manipulation easier in the 2000s, but Vue handles entire component-based applications. It's like PHP templates but client-side, with reactive data binding.

**What you'll use:**
- **Vue 3** - The latest version with Composition API
- **Vite** - Build tool and dev server (like a turbo-charged development server)
- **Vue Router** - Handles navigation between pages (like going from "Scraper" to "Collection")
- **Pinia** - Manages shared data across your app (like user login status)
- **TypeScript** - Type safety (catches errors at compile time)
- **Tailwind CSS** - Utility-first CSS framework for styling

**Cost:** FREE (all open-source)

**Why these?**
- Vue is beginner-friendly but powerful
- Vite makes development much faster (hot module replacement)
- All are industry-standard and well-documented
- TypeScript adds safety without complexity
- Tailwind CSS speeds up styling

**Example:**

```
&lt;template&gt;
  &lt;div&gt;
    &lt;h1&gt;{{ camera.name }}&lt;/h1&gt;
    &lt;button @click="saveCamera"&gt;Save&lt;/button&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref } from 'vue'

const camera = ref({ name: 'Nikon FM2' })

function saveCamera() {
  // Save logic here
}
&lt;/script&gt;
```

---


## 2. Backend: Node.js + TypeScript

### What is Node.js?
Node.js is like PHP but using JavaScript. Instead of Apache + PHP, you have Node.js running JavaScript on the server. It's event-driven and non-blocking (like how you'd handle async operations in C).

**Key differences from PHP:**
- No separate web server needed (Node.js IS the server, like Apache + PHP combined)
- Single-threaded event loop (very efficient for I/O operations)
- npm package manager (like PEAR/PECL but much better)
- Async/await syntax (cleaner than callbacks)

### What is TypeScript?
TypeScript adds static typing to JavaScript (like C's type system). Catches errors at compile time instead of runtime. Optional but highly recommended.

**What you'll use:**
- **Node.js** - Runs your server code
- **Express.js** - A simple framework for building APIs (like building roads for data to travel)
- **TypeScript** - Safer JavaScript
- **Prisma** - ORM (Object-Relational Mapper) that makes working with databases easier
- **Zod** - Runtime type validation for API requests

**Cost:** FREE (all open-source)

**Alternative considered:** Python + FastAPI (if you prefer Python, but Node.js is easier since you're already using JavaScript for Vue)

**Example:**
```typescript
// api/cameras.ts
import { Request, Response } from 'express'
import { prisma } from '../lib/prisma'

export async function getCameras(req: Request, res: Response) {
  const cameras = await prisma.cameraListing.findMany()
  res.json(cameras)
}
```

---

## 3. Database: PostgreSQL on Supabase

### PostgreSQL vs MySQL
PostgreSQL is similar to MySQL but:
- Better JSON support (important for flexible data like saved search params)
- More advanced features (better for complex queries)
- Open source, free, and very reliable
- Similar SQL syntax (you'll feel at home)

**For your use case:** Either would work, but PostgreSQL + Supabase gives you more free features.

### What is Supabase?
Supabase is like cPanel hosting but modern:
- **PostgreSQL database** (like MySQL but hosted/managed)
- **Built-in authentication** (like writing your own PHP auth, but done for you)
- **File storage** (like uploading to `/uploads/` but cloud-based)
- **REST API auto-generated** (like writing PHP endpoints, but automatic)
- **Real-time subscriptions** (like polling but with WebSockets)

**Think of it as:** MySQL + PHP auth + file uploads, but all managed and modern.

**Why Supabase?**
- **FREE tier:** 500MB database, 1GB file storage, 50,000 monthly users
- Perfect for 10 users (you'll use maybe 1% of the free tier)
- Easy to set up
- Great documentation
- Includes authentication and storage (no extra services needed)

**Cost:** FREE (for your use case)

**Alternative free options considered:**
- **Neon** (0.5GB free) - Good alternative, but Supabase includes more features
- **Vercel Postgres** (256MB free) - Too small, and doesn't include auth/storage

**Setup:**
- **Two projects:** `shutterzilla-dev` (development) and `shutterzilla-prod` (production)
- **Migrations:** Stored in GitHub (`supabase/migrations/`)
- **Connection:** Via connection string in environment variables

**Example SQL:**
```sql
-- Similar to MySQL syntax
CREATE TABLE camera_listings (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2),
  url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 4. Web Scraping: Python Scripts

### What is Web Scraping?
Web scraping is automatically collecting data from websites (like getting camera listings from Mercari, eBay, etc.).

### Why Python?
Python has the best tools for scraping websites. It's also what you'll use for the scraper, separate from your main app.

**What you'll use:**
- **Python 3.11+** - The programming language
- **BeautifulSoup** - For parsing HTML (simpler sites)
- **Playwright** - For JavaScript-heavy sites (runs a real browser)
- **GitHub Actions** - Runs your scraper on a schedule (every 4 hours)

**Cost:** FREE
- Python: FREE (open-source)
- GitHub Actions: FREE (2,000 minutes/month - more than enough for 4-hour intervals)

**How it works:**
1. You write a Python script that visits websites and collects camera listings
2. GitHub Actions runs this script every 4 hours automatically
3. The script saves new listings to your Supabase database
4. Your Vue.js app displays the listings

**Example:**
```python
# scraper/scrapers/mercari.py
import requests
from bs4 import BeautifulSoup

def scrape_mercari():
    url = "https://mercari.com/search?keyword=nikon+fm2"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    listings = []
    for item in soup.find_all('div', class_='item'):
        listings.append({
            'title': item.find('h3').text,
            'price': item.find('span', class_='price').text,
            'url': item.find('a')['href']
        })
    
    return listings
```

**Schedule:** Every 4 hours (configurable in GitHub Actions)

---

## 5. File Storage: Supabase Storage

### What is File Storage?
Where you store user-uploaded photos (like camera pictures from the Collection app).

**Why Supabase Storage?**
- Included with Supabase (no extra service needed)
- **FREE tier:** 1GB storage, 2GB bandwidth/month
- Easy to use (simple API)
- For 10 users, this is plenty (each user would need 100MB+ to exceed)

**Cost:** FREE (included with Supabase)

**Alternative considered:** 
- **Cloudflare R2** (10GB free) - More storage, but Supabase is simpler since you're already using it
- **AWS S3** - Paid, overkill for this project

**Use case:** User-uploaded camera photos in the Collection app

**Example:**
```typescript
// Upload a file
const { data, error } = await supabase.storage
  .from('camera-photos')
  .upload(`${userId}/${cameraId}.jpg`, file)

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from('camera-photos')
  .getPublicUrl(`${userId}/${cameraId}.jpg`)
```

---

## 6. Email Service

### Sending Emails (Automated)

**Resend** - Email API for automated emails

**Why Resend?**
- **FREE tier:** 3,000 emails/month, 100 emails/day
- Modern API (easy to use)
- Great deliverability
- Domain verification (send from `@shutterzilla.com`)

**Use for:**
- Email verification (when users sign up)
- Password reset emails
- Search notifications (when new cameras match saved searches)

**Domain setup:**
- Configured to send from `noreply@shutterzilla.com` and `hello@shutterzilla.com`
- DNS: SPF/DKIM records added to Vercel DNS

**Cost:** FREE (for your use case - 3,000 emails/month is plenty for 10 users)

**Alternative considered:**
- **SendGrid** (100 emails/day free forever) - Lower limit, older API
- **Mailgun** (5,000 emails/month free) - More complex setup
- **AWS SES** - Requires AWS account, more complex

**Decision:** Resend chosen for simplicity and modern API

**Example:**
```typescript
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

await resend.emails.send({
  from: 'noreply@shutterzilla.com',
  to: user.email,
  subject: 'Verify your email',
  html: '<p>Click here to verify...</p>'
})
```

### Receiving Emails (Support)

**Question:** "I would need just one incoming email account hello@shutterzilla.com, but I do not want to waste/pay a full blown Google or Microsoft account just for that one, what do you suggest?"

**Solution:** Zoho Mail Free + Gmail forwarding

**Setup:**
1. **Zoho Mail Free** - Create `hello@shutterzilla.com` account
2. **Forwarding:** Auto-forwards all emails to personal Gmail
3. **Sending:** Configure Gmail "Send mail as" with Zoho SMTP credentials
4. **Result:** All emails appear in Gmail, no Zoho app needed on phone

**DNS Configuration:**
- **Question:** "Currently the registrar for my Domain is namecheap, but the DNS records are being managed by Vercel. How would that work if I go the CloudFlare option?"
- **Answer:** We don't need Cloudflare. Vercel DNS can handle MX records for Zoho Mail. No need to move DNS to Cloudflare.

**Cost:** FREE

**Alternative considered:**
- **Google Workspace** ($6/user/month) - Too expensive for one email
- **Microsoft 365** ($6/user/month) - Too expensive
- **Cloudflare Email Routing** - Free, but requires moving DNS to Cloudflare (unnecessary complexity)

**Decision:** Zoho Mail Free + Gmail forwarding chosen for simplicity and zero cost

**Drawback acknowledged:** "The only drawback in this option is using Zoho which will mean yet another app for email on my phone etc"
- **Solution:** Forwarding to Gmail eliminates this - all emails in one place

---

## 7. Hosting: Vercel

### Vercel vs Traditional Hosting

**Old way (LAMP):**
- Upload files via FTP to Apache server
- PHP runs on server
- MySQL database on same server
- Manual deployments
- Server management required

**Modern way (Vercel):**
- Push to GitHub → automatic deployment
- Serverless functions (like PHP but auto-scaling)
- Database separate (Supabase)
- CDN included (faster worldwide)
- No server management

**Why Vercel?**
- **FREE tier:** Unlimited personal projects
- Git-based deployments (push to GitHub → auto-deploy)
- Serverless functions (like PHP scripts but auto-scaling)
- Edge network (CDN) included
- Perfect for Vue.js SPAs
- Automatic HTTPS (SSL certificates)
- Preview deployments for every branch

**Cost:** FREE (for personal projects)

**What gets hosted:**
- Frontend (Vue.js app) - Your website
- Backend API (serverless functions) - Your API endpoints

**Free tier limits:**
- 100GB-hours/month for serverless functions (plenty for 10 users)
- Unlimited bandwidth for static assets
- Unlimited deployments

**Question:** "Can I control which push is actually deployed by Vercel on the cloud production environment? I mean as I work, dozens hundreds of commits are done and pushed and Vercel will always build. What is a good strategy? To have separate Dev, Test and PRD environment? Will that add too much complexity as I am a solo dev + AI help and small project?"

**Answer:** Simplified deployment strategy

**Strategy:**
- **Production:** `main` branch → Auto-deploys to production URL (`shutterzilla.com`)
- **Preview:** Feature branches → Preview deployments (test URLs like `feature-name-abc123.vercel.app`)
- **No separate dev/test environments needed** - Use preview deployments for testing

**Benefits:**
- Simple (no complex branching strategy)
- Every feature branch gets its own URL for testing
- Only `main` branch affects production
- Perfect for solo dev + AI workflow

**How it works:**
1. Create feature branch: `git checkout -b feature-name`
2. Make changes and push
3. Vercel automatically creates preview URL
4. Test on preview URL
5. Merge to `main` → Production deploys automatically

**Alternative considered:** Separate dev/test/prod environments
- **Rejected:** Too much complexity for solo dev + small project
- Preview deployments are sufficient for testing

---

## 8. Authentication: Supabase Auth

### What is Authentication?
The system that handles user login, signup, password reset, etc.

**What you'll use:**
- **Supabase Auth** - Complete authentication solution
- **JWT (JSON Web Tokens)** - Stateless authentication tokens
- **OAuth 2.0** - Protocol for social login

**Sign-up options:**
- **Email/Password** (default) - Traditional signup
- **Google OAuth** (included from start) - "Sign in with Google"
- **Facebook OAuth** (included from start) - "Sign in with Facebook"

**Question:** "I would like to have social login from the start, want to learn how that is done, this project is also about learning for myself"

**Answer:** Social login included from the start for learning purposes.

**How OAuth works:**
1. User clicks "Sign in with Google"
2. Redirected to Google login page
3. User authorizes your app
4. Google redirects back with authorization code
5. Supabase exchanges code for user info
6. User is logged in

**Email verification:**
- Via Resend (configured in Supabase)
- Sends verification email when user signs up

**Password reset:**
- Built-in to Supabase Auth
- Sends reset email via Resend

**Cost:** FREE (included with Supabase)

**How it works:**
- Supabase handles all authentication logic
- Returns JWT tokens for API requests
- Manages user sessions
- Handles OAuth flow for social login
- No custom auth code needed

**Example:**
```typescript
// Sign up with email
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123'
})

// Sign in with Google
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google'
})

// Get current user
const { data: { user } } = await supabase.auth.getUser()
```

**Setup required:**
1. Create OAuth apps in Google Cloud Console
2. Create OAuth app in Facebook Developers
3. Add client IDs/secrets to Supabase Auth settings
4. Configure redirect URLs

---

## 9. Monitoring & Observability

### Error Tracking

**Sentry** - Error tracking and monitoring

**Why Sentry?**
- **FREE tier:** 5,000 events/month, 1 project
- Tracks frontend errors (Vue.js), backend errors (API), crashes
- Features: Stack traces, user context, email alerts
- Easy to integrate

**Cost:** FREE (for your use case - 5,000 events/month is plenty)

**What it tracks:**
- JavaScript errors in Vue.js app
- API errors in serverless functions
- Unhandled exceptions
- User context (which user experienced the error)

**Alternative considered:**
- **Rollbar** - Similar, but Sentry is more popular
- **Bugsnag** - Paid plans start earlier

**Decision:** Sentry chosen for free tier and ease of use

### Analytics

**Vercel Analytics** - Page views and performance

**Why Vercel Analytics?**
- **FREE tier:** Built-in, automatic
- Tracks page views, load times, user locations
- Setup: Automatic (no code needed)
- Privacy-friendly (no cookies)

**Cost:** FREE

**What it tracks:**
- Page views
- Load times
- User locations (country-level)
- Device types

### Logs

**Vercel Logs** - Function execution logs

**Why Vercel Logs?**
- **FREE tier:** Built-in, automatic
- Tracks API requests, function execution, errors
- Setup: Automatic (no code needed)
- Real-time log streaming

**Cost:** FREE

**What it tracks:**
- API request logs
- Function execution logs
- Error logs
- Performance metrics

### Uptime Monitoring (Optional)

**UptimeRobot** - Site uptime checks

**Why UptimeRobot?**
- **FREE tier:** 50 monitors, 5-minute intervals
- Tracks site availability, response times
- Setup: Just add URL
- Email alerts when site is down

**Cost:** FREE

**What it tracks:**
- Site availability (is the site up?)
- Response times
- HTTP status codes

**Recommended Setup:**
- **Sentry** (error tracking) - Essential
- **Vercel Analytics/Logs** (built-in) - Automatic
- **UptimeRobot** (uptime) - Optional but useful

**Question:** "Did we discuss authentication and signing up options and also monitoring?"

**Answer:** Yes, both covered. Authentication includes social login from the start. Monitoring includes error tracking, analytics, logs, and optional uptime monitoring.

---

## Project Structure

```
shutterzilla/
├── apps/                   # Application code
│   ├── frontend/          # Vue.js application
│   │   ├── src/
│   │   │   ├── components/   # Vue components (reusable UI)
│   │   │   ├── views/        # Page views (Scraper, Collection, Admin)
│   │   │   ├── router/       # Vue Router config (navigation)
│   │   │   ├── stores/       # Pinia stores (state management)
│   │   │   ├── lib/          # Utilities (Supabase client, etc.)
│   │   │   └── main.ts       # App entry point
│   │   ├── public/           # Static assets
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   ├── backend/           # API serverless functions
│   │   └── api/
│   │       ├── auth/         # Authentication endpoints
│   │       ├── cameras/     # Camera listing endpoints
│   │       ├── collections/  # Collection endpoints
│   │       └── admin/        # Admin endpoints
│   │
│   └── scraper/           # Python scraping service
│       ├── main.py           # Entry point
│       ├── scrapers/
│       │   ├── mercari.py
│       │   ├── ebay.py
│       │   ├── buyee.py
│       │   └── jd_direct.py
│       ├── utils/
│       │   ├── database.py   # Supabase connection
│       │   └── helpers.py
│       └── requirements.txt
│
├── infrastructure/         # Infrastructure as code
│   ├── supabase/          # Database migrations
│   │   └── migrations/
│   │       ├── 20240101000000_initial_schema.sql
│   │       ├── 20240102000000_add_saved_searches.sql
│   │       └── ...
│   │
│   └── .github/           # GitHub Actions workflows
│       └── workflows/
│           └── scraper.yml    # GitHub Actions scraper schedule
│
├── documentation/         # Project documentation
│   ├── mockupsv1/        # Original desktop mockups
│   ├── mockupsv2/        # Mobile-responsive mockups
│   ├── branding/         # Logo and brand assets
│   ├── tech-stack-guide.md
│   ├── data-models.md
│   └── ...
│
├── .env.local             # Local environment variables (gitignored)
├── .gitignore
├── package.json           # Root package.json (monorepo)
└── README.md
```

**Question:** "When developing the real code, there will be changes to both the Vue, React etc code but also to Supabase DB, right? Where do you keep the DB logic? On Github? Separate on Supabase?"

**Answer:** Database migrations stored in GitHub

**Strategy:**
- **Migrations:** Stored in GitHub (`supabase/migrations/`)
- **Version control:** Each migration is a SQL file with timestamp
- **Two Supabase projects:** `shutterzilla-dev` and `shutterzilla-prod`
- **Workflow:** Create migration → Test on dev → Apply to prod when ready

**Benefits:**
- All code (frontend, backend, database) in one repository
- Version control for database schema
- Easy to rollback changes
- Team can see database changes in git history

**Question:** "Yes, it works, and does it require a local docker container to run supabase?"

**Answer:** No local Docker needed

**Strategy:**
- **Development:** Connect directly to Supabase cloud project (`shutterzilla-dev`)
- **No local Supabase:** Use cloud project for development
- **Trade-off:** Requires internet connection, but simpler setup

**Question:** "Agreed on this approach, I will only 'loose' offline deving which is not much frequent if ever happens."

**Answer:** Correct - offline development is rarely needed for this project.

---

## Development Workflow

### Daily Development

1. **Create feature branch:**
   ```bash
   git checkout -b feature-name
   ```

2. **Make changes** (with AI assistance)
   - Edit Vue.js components
   - Add API endpoints
   - Update database migrations

3. **Test locally:**
   ```bash
   # Frontend
   cd frontend && npm run dev
   
   # Backend (if needed)
   vercel dev
   ```

4. **Push to branch:**
   ```bash
   git push origin feature-name
   ```
   - Vercel automatically creates preview URL
   - Test on preview URL

5. **Merge to `main`:**
   ```bash
   git checkout main
   git merge feature-name
   git push origin main
   ```
   - Production deploys automatically

### Database Changes

1. **Create migration file:**
   ```bash
   # Create new migration
   touch supabase/migrations/$(date +%Y%m%d%H%M%S)_add_user_preferences.sql
   ```

2. **Write migration:**
   ```sql
   -- supabase/migrations/20240101000000_add_user_preferences.sql
   CREATE TABLE user_preferences (
     id SERIAL PRIMARY KEY,
     user_id UUID REFERENCES auth.users(id),
     theme VARCHAR(20) DEFAULT 'light',
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

3. **Test on dev Supabase project:**
   - Apply migration manually in Supabase dashboard
   - Or use Supabase CLI: `supabase db push`

4. **Commit migration to GitHub:**
   ```bash
   git add supabase/migrations/
   git commit -m "Add user preferences table"
   git push
   ```

5. **Apply to prod Supabase when ready:**
   - Apply migration in production Supabase dashboard
   - Or use Supabase CLI with prod connection string

### Scraping Updates

1. **Update Python scraper code:**
   ```bash
   # Edit scraper/scrapers/mercari.py
   ```

2. **Test locally (optional):**
   ```bash
   cd scraper
   python main.py
   ```

3. **Commit to GitHub:**
   ```bash
   git add scraper/
   git commit -m "Update Mercari scraper"
   git push
   ```

4. **GitHub Actions runs automatically:**
   - Runs on schedule (every 4 hours)
   - Check GitHub Actions logs for status

---

## Deployment Strategy

### Production Deployment

**Branch:** `main`  
**URL:** `shutterzilla.com` (production)  
**Trigger:** Automatic on push to `main`

**Process:**
1. Merge feature branch to `main`
2. Push to GitHub
3. Vercel detects push to `main`
4. Builds frontend and backend
5. Deploys to production
6. Site is live in ~2 minutes

### Preview Deployments

**Branch:** Any feature branch  
**URL:** `feature-name-abc123.vercel.app` (unique per branch)  
**Trigger:** Automatic on push to any branch

**Process:**
1. Create feature branch
2. Push to GitHub
3. Vercel creates preview URL
4. Share URL for testing
5. Delete branch → Preview URL is removed

**Benefits:**
- Test changes before merging to `main`
- Share with others for feedback
- No separate dev/test environments needed

### Database Deployment

**Dev Project:** `shutterzilla-dev`
- Used for development and testing
- Apply migrations here first

**Prod Project:** `shutterzilla-prod`
- Used for production
- Apply migrations after testing

**Strategy:**
- Migrations stored in GitHub
- Apply to dev first
- Test thoroughly
- Apply to prod when ready

---

## Database Migrations

### What are Migrations?

Migrations are version-controlled SQL files that define database schema changes. Think of them like git commits for your database.

### Migration Workflow

1. **Create migration file:**
   ```bash
   # Format: YYYYMMDDHHMMSS_description.sql
   touch supabase/migrations/20240101000000_initial_schema.sql
   ```

2. **Write migration:**
   ```sql
   -- supabase/migrations/20240101000000_initial_schema.sql
   CREATE TABLE camera_listings (
     id SERIAL PRIMARY KEY,
     title VARCHAR(255) NOT NULL,
     price DECIMAL(10, 2),
     url TEXT,
     source VARCHAR(50),
     created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE INDEX idx_camera_listings_source ON camera_listings(source);
   ```

3. **Apply to dev:**
   - Use Supabase dashboard SQL editor
   - Or Supabase CLI: `supabase db push`

4. **Commit to GitHub:**
   ```bash
   git add supabase/migrations/
   git commit -m "Add initial camera_listings table"
   git push
   ```

5. **Apply to prod:**
   - After testing on dev
   - Use Supabase dashboard or CLI with prod connection

### Migration Best Practices

- **One change per migration:** Easier to rollback
- **Never edit old migrations:** Create new ones
- **Test on dev first:** Always test before prod
- **Backup before prod:** Supabase has automatic backups

---

## DNS Configuration

### Current Setup

- **Domain Registrar:** Namecheap (`shutterzilla.com`)
- **DNS Management:** Vercel (nameservers pointed to Vercel)
- **Email Records:** Added to Vercel DNS

### DNS Records Needed

**For Vercel Hosting:**
- **A/CNAME records:** Automatic (Vercel handles this)
- **TXT records:** Domain verification (automatic)

**For Email Sending (Resend):**
- **SPF record:** `v=spf1 include:resend.com ~all`
- **DKIM record:** Provided by Resend (add to Vercel DNS)

**For Email Receiving (Zoho Mail):**
- **MX records:** Point to Zoho Mail servers
  - `mx.zoho.com` (priority 10)
  - `mx2.zoho.com` (priority 20)
- **TXT record:** Domain verification for Zoho

**Question:** "Currently the registrar for my Domain is namecheap, but the DNS records are being managed by Vercel. How would that work if I go the CloudFlare option?"

**Answer:** We don't need Cloudflare. Vercel DNS can handle all required records:
- A/CNAME for hosting (automatic)
- MX for Zoho Mail (manual)
- TXT for SPF/DKIM (manual)

No need to move DNS to Cloudflare.

---

## Architecture Comparison

### Old LAMP Stack (2000s):
```
Browser → Apache → PHP → MySQL
         (all on one server)
```

**Characteristics:**
- Everything on one server
- Manual deployments (FTP upload)
- Server management required
- Scaling = bigger server

### Modern Stack:
```
Browser
  ↓
Vercel (CDN + Vue.js SPA)
  ↓
Vercel Serverless Functions (Node.js API)
  ↓
Supabase (PostgreSQL + Auth + Storage)
  ↑
GitHub Actions (Python Scraper)
```

**Characteristics:**
- Separation of concerns (frontend, backend, database)
- Serverless (no server management)
- Git-based deployments (push to deploy)
- Auto-scaling (handles traffic automatically)
- CDN included (faster worldwide)

**Key differences:**
- **Separation of concerns:** Frontend, backend, database all separate
- **Serverless:** No server to manage (like shared hosting but better)
- **Git-based:** Deploy by pushing code (like `git push` → live site)
- **Auto-scaling:** Handles traffic spikes automatically
- **CDN:** Content delivered from edge locations worldwide

---

## Scaling Considerations

### Current Setup Supports

- **10 users comfortably:** All free tiers sufficient
- **Room to grow:** Within free tier limits
- **No bottlenecks:** All services have headroom

### Free Tier Limits

| Service | Free Tier | Current Usage | Headroom |
|---------|-----------|---------------|----------|
| Supabase Database | 500MB | ~10MB | 98% |
| Supabase Storage | 1GB | ~50MB | 95% |
| Resend | 3,000/month | ~100/month | 97% |
| Sentry | 5,000 events/month | ~50/month | 99% |
| GitHub Actions | 2,000 min/month | ~720 min/month | 64% |
| Vercel Functions | 100GB-hours/month | ~1GB-hours/month | 99% |

**Conclusion:** Plenty of room to grow within free tiers.

### When to Upgrade

**User base grows:**
- Beyond 50-100 users (still might fit in free tiers)
- Need more database storage (>500MB)
- Need more email sending (>3,000/month)
- Need more error tracking (>5,000 events/month)

### Upgrade Path

**Supabase Pro:** $25/month
- 8GB database
- 100GB file storage
- 100,000 monthly users

**Resend Pro:** $20/month
- 50,000 emails/month
- Better deliverability

**Sentry Pro:** $26/month
- 50,000 events/month
- More features

**Vercel Pro:** $20/month
- More features
- Better support

**For now:** All free tiers are more than sufficient. Don't upgrade until you actually need it.

---

## Complete Stack Summary

| Component | Technology | Free Tier | Cost | Why |
|-----------|-----------|-----------|------|-----|
| **Frontend Framework** | Vue 3 + Vite | ✅ Free | $0 | You specified Vue |
| **State Management** | Pinia | ✅ Free | $0 | Vue's official state management |
| **Backend Runtime** | Node.js + Express | ✅ Free | $0 | Same language as frontend |
| **Database** | PostgreSQL (Supabase) | ✅ 500MB free | $0 | Includes auth + storage |
| **File Storage** | Supabase Storage | ✅ 1GB free | $0 | Included with Supabase |
| **Authentication** | Supabase Auth | ✅ Free | $0 | Email/password + OAuth |
| **Email Sending** | Resend | ✅ 3,000/month | $0 | Automated emails |
| **Email Receiving** | Zoho Mail | ✅ Free | $0 | Forwards to Gmail |
| **Scraping** | Python + GitHub Actions | ✅ 2,000 min/month | $0 | Scheduled tasks |
| **Hosting** | Vercel | ✅ Free | $0 | Unlimited personal projects |
| **Error Tracking** | Sentry | ✅ 5,000 events/month | $0 | Error monitoring |
| **Analytics** | Vercel Analytics | ✅ Free | $0 | Built-in |
| **Logs** | Vercel Logs | ✅ Free | $0 | Built-in |
| **Uptime** | UptimeRobot | ✅ 50 monitors | $0 | Optional |

**Total Monthly Cost: $0** ✅

---

## Next Steps

### Phase 1: Setup (Week 1)

1. **Create Supabase projects**
   - `shutterzilla-dev` (development)
   - `shutterzilla-prod` (production)

2. **Set up Vercel project**
   - Connect GitHub repository
   - Configure domain (`shutterzilla.com`)
   - Set environment variables

3. **Configure OAuth providers**
   - Google Cloud Console (OAuth app)
   - Facebook Developers (OAuth app)
   - Add to Supabase Auth settings

4. **Set up email**
   - Resend account (sending)
   - Zoho Mail account (receiving)
   - Configure DNS records in Vercel

### Phase 2: Database (Week 1-2)

5. **Create database schema**
   - Write initial migration
   - Apply to dev Supabase
   - Test thoroughly

6. **Set up Prisma**
   - Initialize Prisma
   - Generate client
   - Test database connection

### Phase 3: Frontend (Week 2-3)

7. **Initialize Vue.js project**
   ```bash
   npm create vue@latest frontend
   cd frontend
   npm install
   ```

8. **Set up routing**
   - Install Vue Router
   - Create routes for all pages
   - Set up navigation

9. **Set up state management**
   - Install Pinia
   - Create stores (auth, cameras, collections)

10. **Connect to Supabase**
    - Install Supabase client
    - Set up authentication
    - Test login/signup

### Phase 4: Backend (Week 3-4)

11. **Create API endpoints**
    - Authentication endpoints
    - Camera listing endpoints
    - Collection endpoints
    - Admin endpoints

12. **Set up serverless functions**
    - Create Vercel functions
    - Test locally with `vercel dev`
    - Deploy to preview

### Phase 5: Scraping (Week 4-5)

13. **Write Python scraper**
    - Set up Python environment
    - Write scraper for one site (e.g., Mercari)
    - Test locally

14. **Set up GitHub Actions**
    - Create workflow file
    - Configure schedule (every 4 hours)
    - Test workflow

15. **Add more scrapers**
    - eBay
    - Buyee
    - JD Direct

### Phase 6: Monitoring (Week 5)

16. **Set up Sentry**
    - Create Sentry project
    - Install SDK in Vue.js
    - Install SDK in backend
    - Test error tracking

17. **Enable Vercel Analytics**
    - Automatic (no setup needed)
    - Verify in Vercel dashboard

18. **Set up UptimeRobot** (optional)
    - Create account
    - Add monitor for `shutterzilla.com`

### Phase 7: Testing & Launch (Week 6)

19. **Test all features**
    - Authentication (email + OAuth)
    - Scraper feed
    - Collection management
    - Admin features

20. **Deploy to production**
    - Merge to `main` branch
    - Verify production deployment
    - Test production site

21. **Launch!** 🎉

---

## Learning Resources

### Vue.js
- Official docs: https://vuejs.org
- Vue Router: https://router.vuejs.org
- Pinia: https://pinia.vuejs.org
- Vite: https://vitejs.dev

### Supabase
- Official docs: https://supabase.com/docs
- Auth guide: https://supabase.com/docs/guides/auth
- Database guide: https://supabase.com/docs/guides/database
- Storage guide: https://supabase.com/docs/guides/storage

### Vercel
- Official docs: https://vercel.com/docs
- Serverless functions: https://vercel.com/docs/functions
- Deployment: https://vercel.com/docs/deployments

### OAuth/Social Login
- OAuth 2.0 explained: https://oauth.net/2/
- Google OAuth: https://developers.google.com/identity/protocols/oauth2
- Facebook OAuth: https://developers.facebook.com/docs/facebook-login

### TypeScript
- Official docs: https://www.typescriptlang.org/docs
- TypeScript for JavaScript Programmers: https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html

### Prisma
- Official docs: https://www.prisma.io/docs
- Getting started: https://www.prisma.io/docs/getting-started

---

## Questions & Answers Summary

**Q: Can I control which push is deployed to production?**  
A: Yes - only `main` branch deploys to production. Feature branches get preview URLs.

**Q: Do I need separate dev/test/prod environments?**  
A: No - use preview deployments for testing. Only `main` affects production.

**Q: Where do I keep database logic?**  
A: Migrations stored in GitHub (`supabase/migrations/`). All code in one repo.

**Q: Do I need local Docker for Supabase?**  
A: No - connect directly to Supabase cloud projects. Simpler setup.

**Q: What about email receiving?**  
A: Zoho Mail Free + Gmail forwarding. All emails in Gmail, no extra app.

**Q: Can Vercel DNS handle email records?**  
A: Yes - Vercel DNS can handle MX records for Zoho Mail. No Cloudflare needed.

**Q: Should I include social login from the start?**  
A: Yes - included for learning purposes. Google and Facebook OAuth.

**Q: What about monitoring?**  
A: Sentry (errors), Vercel Analytics/Logs (built-in), UptimeRobot (optional).

---

**This tech stack is finalized and ready for implementation. All decisions documented, all questions answered, all options considered. Total cost: $0/month for up to 10 users.** ✅
