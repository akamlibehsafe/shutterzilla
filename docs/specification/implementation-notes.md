# Implementation Notes

This document mirrors the structure of `implementation-plan.md` and provides space for notes, observations, learnings, and decisions for each step in the implementation plan.

**Purpose:** To capture the "why" behind decisions, document learnings, and provide context as we work through each phase step-by-step.

**How to Use:** Follow the steps in `implementation-plan.md` and add notes here for each corresponding step.

---

## Phase 0: Planning & Documentation Setup ✅

### Define planning documentation structure
**Notes:**
- Established planning documentation structure
- All implementation docs use `implementation-` prefix
- All docs stored in `docs/`

### Create implementation plan document
**Notes:**
- Created master plan with detailed steps
- Plan structured for step-by-step execution
- Each phase has clear deliverables

### Define mockup-to-code migration process
**Notes:**
- Defined screen-by-screen approach
- Process includes: Review → Refine → Implement → Test → Document
- Changes will be tracked in `implementation-mockup-to-code-changes.md`

---

## Phase 1: Complete Stack Setup

**Status:** Not Started

### 1.1 Repository Structure

#### Create `apps/` folder structure
**Notes:**
_(Add notes as you work through this step)_

#### Create `infrastructure/` folder structure
**Notes:**
_(Add notes as you work through this step)_

#### Set up root `package.json` (monorepo workspace)
**Notes:**
_(Add notes as you work through this step)_

#### Configure `.gitignore`
**Notes:**
_(Add notes as you work through this step)_

---

### 1.2 Supabase Setup

#### Create `shutterzilla-dev` project
**Notes:**
_(Add notes as you work through this step)_

#### Create `shutterzilla-prod` project
**Notes:**
_(Add notes as you work through this step)_

#### Configure Supabase Auth settings
**Notes:**
_(Add notes as you work through this step)_

#### Set up email templates (Resend integration)
**Notes:**
_(Add notes as you work through this step)_

#### Configure OAuth providers: Google OAuth
**Notes:**
_(Add notes as you work through this step)_

#### Configure OAuth providers: Facebook OAuth
**Notes:**
_(Add notes as you work through this step)_

#### Add OAuth credentials to Supabase Auth
**Notes:**
_(Add notes as you work through this step)_

#### Test email/password signup
**Notes:**
_(Add notes as you work through this step)_

#### Test OAuth flows (Google, Facebook)
**Notes:**
_(Add notes as you work through this step)_

#### Set up Supabase Storage buckets
**Notes:**
_(Add notes as you work through this step)_

#### Configure storage policies
**Notes:**
_(Add notes as you work through this step)_

---

### 1.3 Vercel Setup

#### Create Vercel project
**Notes:**
_(Add notes as you work through this step)_

#### Connect GitHub repository
**Notes:**
_(Add notes as you work through this step)_

#### Configure domain (`shutterzilla.com`)
**Notes:**
_(Add notes as you work through this step)_

#### Set up environment variables: Supabase URLs and keys
**Notes:**
_(Add notes as you work through this step)_

#### Set up environment variables: Resend API key
**Notes:**
_(Add notes as you work through this step)_

#### Set up environment variables: OAuth client IDs and secrets
**Notes:**
_(Add notes as you work through this step)_

#### Configure preview deployments
**Notes:**
_(Add notes as you work through this step)_

#### Test deployment workflow
**Notes:**
_(Add notes as you work through this step)_

---

### 1.4 Email Services Setup

#### Create Resend account
**Notes:**
_(Add notes as you work through this step)_

#### Verify domain (`shutterzilla.com`)
**Notes:**
_(Add notes as you work through this step)_

#### Configure SPF/DKIM records in Vercel DNS
**Notes:**
_(Add notes as you work through this step)_

#### Set up Zoho Mail account (`hello@shutterzilla.com`)
**Notes:**
_(Add notes as you work through this step)_

#### Configure email forwarding (Zoho → Gmail)
**Notes:**
_(Add notes as you work through this step)_

#### Configure Gmail "Send mail as" with Zoho SMTP
**Notes:**
_(Add notes as you work through this step)_

#### Test email sending (Resend)
**Notes:**
_(Add notes as you work through this step)_

#### Test email receiving (Zoho → Gmail)
**Notes:**
_(Add notes as you work through this step)_

---

### 1.5 Monitoring Setup

#### Create Sentry project
**Notes:**
_(Add notes as you work through this step)_

#### Get Sentry DSN
**Notes:**
_(Add notes as you work through this step)_

#### Configure Vercel Analytics
**Notes:**
_(Add notes as you work through this step)_

#### Set up UptimeRobot (optional)
**Notes:**
_(Add notes as you work through this step)_

#### Test error tracking
**Notes:**
_(Add notes as you work through this step)_

---

### 1.6 Development Environment

#### Install Node.js and npm
**Notes:**
_(Add notes as you work through this step)_

#### Install Python 3.11+
**Notes:**
_(Add notes as you work through this step)_

#### Set up local development environment
**Notes:**
_(Add notes as you work through this step)_

#### Configure `.env.local` template
**Notes:**
_(Add notes as you work through this step)_

#### Test Supabase local connection
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 2: Database Foundation

**Status:** Not Started

### 2.1 Data Model Refinement

#### Review `data-models.md` and `implementation-data-models-refinement.md`
**Notes:**
_(Add notes as you work through this step)_

#### Work through data model questions together
**Notes:**
_(Add notes as you work through this step)_

#### Define fields for Camera Listings
**Notes:**
_(Add notes as you work through this step)_

#### Define fields for Saved Searches
**Notes:**
_(Add notes as you work through this step)_

#### Define fields for Collection Cameras
**Notes:**
_(Add notes as you work through this step)_

#### Define fields for Users
**Notes:**
_(Add notes as you work through this step)_

#### Finalize relationships and constraints
**Notes:**
_(Add notes as you work through this step)_

#### Plan indexes for performance
**Notes:**
_(Add notes as you work through this step)_

---

### 2.2 Prisma Setup

#### Initialize Prisma in backend
**Notes:**
_(Add notes as you work through this step)_

#### Configure Prisma schema based on refined models
**Notes:**
_(Add notes as you work through this step)_

#### Set up database connection
**Notes:**
_(Add notes as you work through this step)_

#### Generate Prisma client
**Notes:**
_(Add notes as you work through this step)_

---

### 2.3 Database Migrations

#### Create initial migration
**Notes:**
_(Add notes as you work through this step)_

#### Apply to dev Supabase
**Notes:**
_(Add notes as you work through this step)_

#### Test schema
**Notes:**
_(Add notes as you work through this step)_

#### Create seed data (optional)
**Notes:**
_(Add notes as you work through this step)_

#### Document migration process
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 3: Backend API Foundation

**Status:** Not Started

### 3.1 Backend Setup

#### Initialize Node.js project in `apps/backend/`
**Notes:**
_(Add notes as you work through this step)_

#### Install dependencies (Express, TypeScript, Prisma, etc.)
**Notes:**
_(Add notes as you work through this step)_

#### Set up TypeScript configuration
**Notes:**
_(Add notes as you work through this step)_

#### Configure Vercel serverless functions structure
**Notes:**
_(Add notes as you work through this step)_

#### Set up basic Express app
**Notes:**
_(Add notes as you work through this step)_

#### Configure CORS and middleware
**Notes:**
_(Add notes as you work through this step)_

---

### 3.2 Authentication Endpoints

#### Set up Supabase client in backend
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: Sign up (email/password)
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: Sign in (email/password)
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: OAuth initiation (Google, Facebook)
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: OAuth callback handling
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: Sign out
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: Password reset request
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: Password reset confirmation
**Notes:**
_(Add notes as you work through this step)_

#### Create auth endpoints: Email verification
**Notes:**
_(Add notes as you work through this step)_

#### Implement JWT token handling
**Notes:**
_(Add notes as you work through this step)_

#### Create auth middleware for protected routes
**Notes:**
_(Add notes as you work through this step)_

#### Test all auth flows
**Notes:**
_(Add notes as you work through this step)_

---

### 3.3 Core API Endpoints

#### Camera listings endpoints (CRUD)
**Notes:**
_(Add notes as you work through this step)_

#### Collections endpoints (CRUD)
**Notes:**
_(Add notes as you work through this step)_

#### Saved searches endpoints (CRUD)
**Notes:**
_(Add notes as you work through this step)_

#### User profile endpoints
**Notes:**
_(Add notes as you work through this step)_

#### Error handling
**Notes:**
_(Add notes as you work through this step)_

#### Input validation (Zod)
**Notes:**
_(Add notes as you work through this step)_

#### API documentation
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 4: Frontend Foundation

**Status:** Not Started

### 4.1 Vue.js Project Setup

#### Initialize Vue 3 project in `apps/frontend/`
**Notes:**
_(Add notes as you work through this step)_

#### Install dependencies (Vue Router, Pinia, TypeScript, Tailwind)
**Notes:**
_(Add notes as you work through this step)_

#### Configure Vite
**Notes:**
_(Add notes as you work through this step)_

#### Set up TypeScript
**Notes:**
_(Add notes as you work through this step)_

#### Configure Tailwind CSS
**Notes:**
_(Add notes as you work through this step)_

#### Set up project structure (components, views, stores, lib)
**Notes:**
_(Add notes as you work through this step)_

---

### 4.2 Supabase Client Setup

#### Install Supabase client library
**Notes:**
_(Add notes as you work through this step)_

#### Configure Supabase client
**Notes:**
_(Add notes as you work through this step)_

#### Set up environment variables
**Notes:**
_(Add notes as you work through this step)_

#### Test connection
**Notes:**
_(Add notes as you work through this step)_

---

### 4.3 Routing Setup

#### Install Vue Router
**Notes:**
_(Add notes as you work through this step)_

#### Define all routes (from `page-inventory.md`)
**Notes:**
_(Add notes as you work through this step)_

#### Set up route guards (auth protection)
**Notes:**
_(Add notes as you work through this step)_

#### Configure navigation structure
**Notes:**
_(Add notes as you work through this step)_

---

### 4.4 State Management Setup

#### Install Pinia
**Notes:**
_(Add notes as you work through this step)_

#### Create auth store
**Notes:**
_(Add notes as you work through this step)_

#### Create camera listings store
**Notes:**
_(Add notes as you work through this step)_

#### Create collections store
**Notes:**
_(Add notes as you work through this step)_

#### Set up store persistence (if needed)
**Notes:**
_(Add notes as you work through this step)_

---

### 4.5 Layout Components

#### Create top bar component (from mockups)
**Notes:**
_(Add notes as you work through this step)_

#### Create footer component (from mockups)
**Notes:**
_(Add notes as you work through this step)_

#### Create app switcher component
**Notes:**
_(Add notes as you work through this step)_

#### Set up main layout wrapper
**Notes:**
_(Add notes as you work through this step)_

#### Implement mobile menu (from mockupsv2)
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 5: Authentication Flow (Frontend)

**Status:** Not Started

### 5.1 Auth Pages

#### Landing page
**Notes:**
_(Add notes as you work through this step)_

#### Sign up page (email/password)
**Notes:**
_(Add notes as you work through this step)_

#### Sign in page (email/password)
**Notes:**
_(Add notes as you work through this step)_

#### OAuth buttons (Google, Facebook)
**Notes:**
_(Add notes as you work through this step)_

#### Email verification page
**Notes:**
_(Add notes as you work through this step)_

#### Forgot password page
**Notes:**
_(Add notes as you work through this step)_

#### Password reset page
**Notes:**
_(Add notes as you work through this step)_

#### Password reset sent confirmation
**Notes:**
_(Add notes as you work through this step)_

---

### 5.2 Auth Integration

#### Connect auth pages to backend API
**Notes:**
_(Add notes as you work through this step)_

#### Implement OAuth flow
**Notes:**
_(Add notes as you work through this step)_

#### Handle auth state in Pinia store
**Notes:**
_(Add notes as you work through this step)_

#### Implement protected routes
**Notes:**
_(Add notes as you work through this step)_

#### Add auth error handling
**Notes:**
_(Add notes as you work through this step)_

#### Test all auth flows end-to-end
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 6: Mockup-to-Code Migration - Scraper App

**Status:** Not Started

### 6.1 Scraper Feed Screen

#### Review mockup and `implementation-screen-specifications.md`
**Notes:**
_(Add notes as you work through this step)_

#### Refine behavior and data requirements together
**Notes:**
_(Add notes as you work through this step)_

#### Document planned changes
**Notes:**
_(Add notes as you work through this step)_

#### Create components
**Notes:**
_(Add notes as you work through this step)_

#### Implement functionality
**Notes:**
_(Add notes as you work through this step)_

#### Connect to backend API
**Notes:**
_(Add notes as you work through this step)_

#### Test
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 6.2 Scraper Search Screen

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 6.3 Saved Searches Screen

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 6.4 Feed List View

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 6.5 Detail Pages

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 7: Mockup-to-Code Migration - Collection App

**Status:** Not Started

### 7.1 Collection Home Screen

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 7.2 Add Camera Screen

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 7.3 Camera Detail Screen

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

### 7.4 Statistics Screen

#### Review mockup and refine specifications
**Notes:**
_(Add notes as you work through this step)_

#### Implement screen-by-screen
**Notes:**
_(Add notes as you work through this step)_

#### Document changes
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 8: Scraper Service

**Status:** Not Started

### 8.1 Scraper Behavior Specification

#### Review `implementation-scraper-behavior-specification.md`
**Notes:**
_(Add notes as you work through this step)_

#### Work through scraper behavior questions together
**Notes:**
_(Add notes as you work through this step)_

#### Define scraping approach for each source
**Notes:**
_(Add notes as you work through this step)_

#### Define data normalization strategy
**Notes:**
_(Add notes as you work through this step)_

#### Define deduplication strategy
**Notes:**
_(Add notes as you work through this step)_

#### Define error handling approach
**Notes:**
_(Add notes as you work through this step)_

---

### 8.2 Scraper Setup

#### Set up Python project in `apps/scraper/`
**Notes:**
_(Add notes as you work through this step)_

#### Install dependencies (BeautifulSoup, Playwright, etc.)
**Notes:**
_(Add notes as you work through this step)_

#### Create scraper structure
**Notes:**
_(Add notes as you work through this step)_

#### Set up Supabase connection
**Notes:**
_(Add notes as you work through this step)_

---

### 8.3 Implement Scrapers (One by One)

#### Buyee scraper (refine and implement)
**Notes:**
- ✅ Playwright-based scraper working
- ✅ Successfully extracts all required fields
- ✅ Handles iframe content for descriptions
- ✅ Extracts structured data from detail tables
- ✅ Translation support for Japanese content

#### eBay scraper (refine and implement)
**Notes:**
_(Add notes as you work through this step)_

#### Test each scraper
**Notes:**
_(Add notes as you work through this step)_

#### Handle errors and edge cases
**Notes:**
_(Add notes as you work through this step)_

---

### 8.4 GitHub Actions Setup

#### Create workflow file
**Notes:**
_(Add notes as you work through this step)_

#### Configure schedule (every 4 hours)
**Notes:**
_(Add notes as you work through this step)_

#### Set up secrets (Supabase credentials)
**Notes:**
_(Add notes as you work through this step)_

#### Test workflow execution
**Notes:**
_(Add notes as you work through this step)_

#### Set up logging and monitoring
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 9: Admin Dashboard

**Status:** Not Started

### 9.1 Admin Pages

#### Admin Dashboard
**Notes:**
_(Add notes as you work through this step)_

#### User Management
**Notes:**
_(Add notes as you work through this step)_

#### Scraper Configuration
**Notes:**
_(Add notes as you work through this step)_

#### System Logs
**Notes:**
_(Add notes as you work through this step)_

#### Settings
**Notes:**
_(Add notes as you work through this step)_

---

### 9.2 Admin Backend

#### Admin API endpoints
**Notes:**
_(Add notes as you work through this step)_

#### Admin authentication/authorization
**Notes:**
_(Add notes as you work through this step)_

#### Admin middleware
**Notes:**
_(Add notes as you work through this step)_

---

## Phase 10: Polish, Testing & Deployment

**Status:** Not Started

### 10.1 Testing

#### End-to-end testing
**Notes:**
_(Add notes as you work through this step)_

#### Error handling testing
**Notes:**
_(Add notes as you work through this step)_

#### Performance testing
**Notes:**
_(Add notes as you work through this step)_

#### Security review
**Notes:**
_(Add notes as you work through this step)_

---

### 10.2 Monitoring

#### Set up Sentry in frontend
**Notes:**
_(Add notes as you work through this step)_

#### Set up Sentry in backend
**Notes:**
_(Add notes as you work through this step)_

#### Configure alerts
**Notes:**
_(Add notes as you work through this step)_

#### Set up analytics
**Notes:**
_(Add notes as you work through this step)_

---

### 10.3 Production Deployment

#### Final database migration to prod
**Notes:**
_(Add notes as you work through this step)_

#### Deploy to Vercel production
**Notes:**
_(Add notes as you work through this step)_

#### Test production environment
**Notes:**
_(Add notes as you work through this step)_

#### Configure production monitoring
**Notes:**
_(Add notes as you work through this step)_

---

## General Learnings & Decisions

_(Space for cross-phase learnings, architectural decisions, and insights that don't fit in specific steps)_
