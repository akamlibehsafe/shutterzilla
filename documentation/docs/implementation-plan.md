# ShutterZilla Implementation Plan

This document tracks the step-by-step implementation plan for building ShutterZilla. It will be updated as we progress through each phase.

**Last Updated:** 2026-01-13  
**Status:** Planning Phase

---

## Planning Documentation Structure

All planning and implementation documentation will be stored in `documentation/docs/`:

- **`implementation-plan.md`** (this file) - Master plan with detailed steps to follow
- **`implementation-notes.md`** - Same structure as plan, with space for notes and observations for each step
- **`implementation-mockup-to-code-changes.md`** - Log of changes made when converting mockups to actual code
- Phase-specific docs as needed (e.g., `phase-1-setup-notes.md`)

---

## Implementation Phases

### Phase 0: Planning & Documentation Setup ✅
- [x] Define planning documentation structure
- [x] Create implementation plan document
- [x] Define mockup-to-code migration process

### Phase 0.1: High-Level Behavior & Requirements Discussion
**Goal:** Define overall app behavior and user flows at a high level

- [ ] Define user journeys (Scraper App, Collection App, Auth, Admin)
- [ ] Define core features for each app
- [ ] Define basic data requirements
- [ ] Document in `implementation-validation-notes.md`

**Deliverable:** High-level understanding of app behavior and basic data needs

### Phase 0.2: Scraping Feasibility Validation
**Goal:** Test if we can successfully scrape from all four target sources

- [ ] Create validation test scripts for each source
- [ ] Test Mercari Japan scraping
- [ ] Test Buyee scraping
- [ ] Test Yahoo Japan Auctions scraping
- [ ] Test eBay USA scraping (or evaluate API)
- [ ] Document results in `implementation-validation-notes.md`
- [ ] Make go/no-go decision based on results

**Deliverable:** Validation results and decision on scraping feasibility

**Note:** See `implementation-validation-plan.md` for detailed validation steps.

### Phase 1: Complete Stack Setup
**Goal:** Set up all infrastructure and services before writing any code

#### 1.1 Repository Structure
- [ ] Create `apps/` folder structure
- [ ] Create `infrastructure/` folder structure
- [ ] Set up root `package.json` (monorepo workspace)
- [ ] Configure `.gitignore`

#### 1.2 Supabase Setup
- [ ] Create `shutterzilla-dev` project
- [ ] Create `shutterzilla-prod` project
- [ ] Configure Supabase Auth settings
- [ ] Set up email templates (Resend integration)
- [ ] Configure OAuth providers:
  - [ ] Google OAuth (create app, get credentials)
  - [ ] Facebook OAuth (create app, get credentials)
- [ ] Add OAuth credentials to Supabase Auth
- [ ] Test email/password signup
- [ ] Test OAuth flows (Google, Facebook)
- [ ] Set up Supabase Storage buckets
- [ ] Configure storage policies

#### 1.3 Vercel Setup
- [ ] Create Vercel project
- [ ] Connect GitHub repository
- [ ] Configure domain (`shutterzilla.com`)
- [ ] Set up environment variables:
  - [ ] Supabase URLs and keys (dev + prod)
  - [ ] Resend API key
  - [ ] OAuth client IDs and secrets
- [ ] Configure preview deployments
- [ ] Test deployment workflow

#### 1.4 Email Services Setup
- [ ] Create Resend account
- [ ] Verify domain (`shutterzilla.com`)
- [ ] Configure SPF/DKIM records in Vercel DNS
- [ ] Set up Zoho Mail account (`hello@shutterzilla.com`)
- [ ] Configure email forwarding (Zoho → Gmail)
- [ ] Configure Gmail "Send mail as" with Zoho SMTP
- [ ] Test email sending (Resend)
- [ ] Test email receiving (Zoho → Gmail)

#### 1.5 Monitoring Setup
- [ ] Create Sentry project
- [ ] Get Sentry DSN
- [ ] Configure Vercel Analytics
- [ ] Set up UptimeRobot (optional)
- [ ] Test error tracking

#### 1.6 Development Environment
- [ ] Install Node.js and npm
- [ ] Install Python 3.11+
- [ ] Set up local development environment
- [ ] Configure `.env.local` template
- [ ] Test Supabase local connection

**Deliverable:** All services configured and tested, ready for code development

---

### Phase 2: Database Foundation
**Goal:** Create database schema and set up database tooling

#### 2.1 Data Model Refinement
- [ ] Review `data-models.md` and `implementation-data-models-refinement.md`
- [ ] Work through data model questions together
- [ ] Define fields for Camera Listings
- [ ] Define fields for Saved Searches
- [ ] Define fields for Collection Cameras
- [ ] Define fields for Users
- [ ] Finalize relationships and constraints
- [ ] Plan indexes for performance

#### 2.2 Prisma Setup
- [ ] Initialize Prisma in backend
- [ ] Configure Prisma schema based on refined models
- [ ] Set up database connection
- [ ] Generate Prisma client

#### 2.3 Database Migrations
- [ ] Create initial migration
- [ ] Apply to dev Supabase
- [ ] Test schema
- [ ] Create seed data (optional)
- [ ] Document migration process

**Deliverable:** Database schema created and tested based on refined data models

---

### Phase 3: Backend API Foundation
**Goal:** Set up backend API structure and core endpoints

#### 3.1 Backend Setup
- [ ] Initialize Node.js project in `apps/backend/`
- [ ] Install dependencies (Express, TypeScript, Prisma, etc.)
- [ ] Set up TypeScript configuration
- [ ] Configure Vercel serverless functions structure
- [ ] Set up basic Express app
- [ ] Configure CORS and middleware

#### 3.2 Authentication Endpoints
- [ ] Set up Supabase client in backend
- [ ] Create auth endpoints:
  - [ ] Sign up (email/password)
  - [ ] Sign in (email/password)
  - [ ] OAuth initiation (Google, Facebook)
  - [ ] OAuth callback handling
  - [ ] Sign out
  - [ ] Password reset request
  - [ ] Password reset confirmation
  - [ ] Email verification
- [ ] Implement JWT token handling
- [ ] Create auth middleware for protected routes
- [ ] Test all auth flows

#### 3.3 Core API Endpoints
- [ ] Camera listings endpoints (CRUD)
- [ ] Collections endpoints (CRUD)
- [ ] Saved searches endpoints (CRUD)
- [ ] User profile endpoints
- [ ] Error handling
- [ ] Input validation (Zod)
- [ ] API documentation

**Deliverable:** Working backend API with authentication

---

### Phase 4: Frontend Foundation
**Goal:** Set up Vue.js application structure

#### 4.1 Vue.js Project Setup
- [ ] Initialize Vue 3 project in `apps/frontend/`
- [ ] Install dependencies (Vue Router, Pinia, TypeScript, Tailwind)
- [ ] Configure Vite
- [ ] Set up TypeScript
- [ ] Configure Tailwind CSS
- [ ] Set up project structure (components, views, stores, lib)

#### 4.2 Supabase Client Setup
- [ ] Install Supabase client library
- [ ] Configure Supabase client
- [ ] Set up environment variables
- [ ] Test connection

#### 4.3 Routing Setup
- [ ] Install Vue Router
- [ ] Define all routes (from `page-inventory.md`)
- [ ] Set up route guards (auth protection)
- [ ] Configure navigation structure

#### 4.4 State Management Setup
- [ ] Install Pinia
- [ ] Create auth store
- [ ] Create camera listings store
- [ ] Create collections store
- [ ] Set up store persistence (if needed)

#### 4.5 Layout Components
- [ ] Create top bar component (from mockups)
- [ ] Create footer component (from mockups)
- [ ] Create app switcher component
- [ ] Set up main layout wrapper
- [ ] Implement mobile menu (from mockupsv2)

**Deliverable:** Vue.js app structure ready for page implementation

---

### Phase 5: Authentication Flow (Frontend)
**Goal:** Implement complete authentication UI and flows

#### 5.1 Auth Pages
- [ ] Landing page
- [ ] Sign up page (email/password)
- [ ] Sign in page (email/password)
- [ ] OAuth buttons (Google, Facebook)
- [ ] Email verification page
- [ ] Forgot password page
- [ ] Password reset page
- [ ] Password reset sent confirmation

#### 5.2 Auth Integration
- [ ] Connect auth pages to backend API
- [ ] Implement OAuth flow
- [ ] Handle auth state in Pinia store
- [ ] Implement protected routes
- [ ] Add auth error handling
- [ ] Test all auth flows end-to-end

**Deliverable:** Complete authentication system working

---

### Phase 6: Mockup-to-Code Migration - Scraper App
**Goal:** Convert Scraper App mockups to working code (screen-by-screen)

#### 6.1 Scraper Feed Screen
- [ ] Review mockup and `implementation-screen-specifications.md`
- [ ] Refine behavior and data requirements together
- [ ] Document planned changes
- [ ] Create components
- [ ] Implement functionality
- [ ] Connect to backend API
- [ ] Test
- [ ] Document changes

#### 6.2 Scraper Search Screen
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

#### 6.3 Saved Searches Screen
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

#### 6.4 Feed List View
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

#### 6.5 Detail Pages
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

**Deliverable:** Working Scraper App, refined screen-by-screen

---

### Phase 7: Mockup-to-Code Migration - Collection App
**Goal:** Convert Collection App mockups to working code (screen-by-screen)

#### 7.1 Collection Home Screen
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

#### 7.2 Add Camera Screen
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

#### 7.3 Camera Detail Screen
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

#### 7.4 Statistics Screen
- [ ] Review mockup and refine specifications
- [ ] Implement screen-by-screen
- [ ] Document changes

**Deliverable:** Working Collection App, refined screen-by-screen

---

### Phase 8: Scraper Service
**Goal:** Implement Python scraper and automation

#### 8.1 Scraper Behavior Specification
- [ ] Review `implementation-scraper-behavior-specification.md`
- [ ] Work through scraper behavior questions together
- [ ] Define scraping approach for each source
- [ ] Define data normalization strategy
- [ ] Define deduplication strategy
- [ ] Define error handling approach

#### 8.2 Scraper Setup
- [ ] Set up Python project in `apps/scraper/`
- [ ] Install dependencies (BeautifulSoup, Playwright, etc.)
- [ ] Create scraper structure
- [ ] Set up Supabase connection

#### 8.3 Implement Scrapers (One by One)
- [ ] Mercari scraper (refine and implement)
- [ ] eBay scraper (refine and implement)
- [ ] Buyee scraper (refine and implement)
- [ ] JD Direct scraper (refine and implement)
- [ ] Test each scraper
- [ ] Handle errors and edge cases

#### 8.4 GitHub Actions Setup
- [ ] Create workflow file
- [ ] Configure schedule (every 4 hours)
- [ ] Set up secrets (Supabase credentials)
- [ ] Test workflow execution
- [ ] Set up logging and monitoring

**Deliverable:** Automated scraper running on schedule, behavior fully specified

---

### Phase 9: Admin Dashboard
**Goal:** Implement admin functionality

#### 9.1 Admin Pages
- [ ] Admin Dashboard
- [ ] User Management
- [ ] Scraper Configuration
- [ ] System Logs
- [ ] Settings

#### 9.2 Admin Backend
- [ ] Admin API endpoints
- [ ] Admin authentication/authorization
- [ ] Admin middleware

**Deliverable:** Working admin dashboard

---

### Phase 10: Polish, Testing & Deployment
**Goal:** Finalize and deploy to production

#### 10.1 Testing
- [ ] End-to-end testing
- [ ] Error handling testing
- [ ] Performance testing
- [ ] Security review

#### 10.2 Monitoring
- [ ] Set up Sentry in frontend
- [ ] Set up Sentry in backend
- [ ] Configure alerts
- [ ] Set up analytics

#### 10.3 Production Deployment
- [ ] Final database migration to prod
- [ ] Deploy to Vercel production
- [ ] Test production environment
- [ ] Configure production monitoring

**Deliverable:** ShutterZilla live in production

---

## Mockup-to-Code Migration Process

When converting mockups to code, we will:

1. **Review the mockup** - Understand the design and functionality
2. **Document planned changes** - Note any deviations from mockup
3. **Create components** - Break down into reusable Vue components
4. **Implement functionality** - Connect to backend API
5. **Test** - Ensure it works as expected
6. **Document changes** - Log all changes in `implementation-mockup-to-code-changes.md`

**Change Log Format:**
- Date
- Page/Component
- Change description
- Reason for change
- Impact

---

## Notes

- Each phase should be completed and tested before moving to the next
- Changes from mockups will be documented, not hidden
- Learning is part of the process - questions and exploration are encouraged
- We'll iterate and refine as we go

---

**Next Step:** Begin Phase 1 - Complete Stack Setup
