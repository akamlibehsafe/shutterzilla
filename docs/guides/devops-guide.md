# DevOps Guide for ShutterZilla

**Last Updated:** 2026-01-15

Comprehensive guide to DevOps practices for ShutterZilla, including environment management, data seeding, project management, and deployment workflows.

---

## Table of Contents

1. [Environment Strategy](#environment-strategy)
2. [Data Seeding for Testing](#data-seeding-for-testing)
3. [GitHub Projects Setup](#github-projects-setup)
4. [Daily Workflow Examples](#daily-workflow-examples)
5. [Troubleshooting](#troubleshooting)

---

## Environment Strategy

### Overview

ShutterZilla uses a **configuration-based environment approach** (not branch-based). This means environments are controlled by configuration (environment variables) rather than Git branches.

**Key Principle:** Branches are for features, not environments.

### Environment Architecture

**Two-Environment Approach (Recommended for Solo Dev):**

```
┌─────────────────────────────────────────────────────────┐
│                    ENVIRONMENT SETUP                     │
└─────────────────────────────────────────────────────────┘

Feature Branch (feature/camera-search)
    │
    ├─→ Preview Deployment (DEV Environment)
    │   ├─→ URL: feature-camera-search-abc123.vercel.app
    │   ├─→ Supabase: shutterzilla-dev
    │   └─→ Environment Variables: DEV_*
    │
    ↓ Merge to main
    │
main Branch
    │
    └─→ Production Deployment (PRD Environment)
        ├─→ URL: shutterzilla.com
        ├─→ Supabase: shutterzilla-prod
        └─→ Environment Variables: PRD_*
```

### Why Configuration-Based (Not Branch-Based)

**❌ Branch-Based Approach (Complex, Risky):**
```
feature → develop → staging → main
  (merge conflicts, branch juggling, dangerous)
```

**✅ Configuration-Based Approach (Simple, Safe):**
```
feature → main
  (one merge, environments configured separately)
```

**Benefits:**
- ✅ No merge conflicts between environments
- ✅ Simple workflow (one branch: `main`)
- ✅ Environments controlled by configuration
- ✅ Easy to understand and maintain

### Setting Up Environments

#### Step 1: Create Supabase Projects

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Create two projects:
   - `shutterzilla-dev` (for development/testing)
   - `shutterzilla-prod` (for production)
3. Note the project URLs and API keys for each

**Cost:** Both projects use free tier = $0/month

#### Step 2: Configure Vercel Environment Variables

1. Go to Vercel Project Settings → Environment Variables
2. Add variables for each environment:

**Production Environment:**
```
SUPABASE_URL = https://xxx.supabase.co (prod project URL)
SUPABASE_ANON_KEY = eyJ... (prod project anon key)
SUPABASE_SERVICE_ROLE_KEY = eyJ... (prod project service role key)
```

**Preview Environment (for feature branches):**
```
SUPABASE_URL = https://yyy.supabase.co (dev project URL)
SUPABASE_ANON_KEY = eyJ... (dev project anon key)
SUPABASE_SERVICE_ROLE_KEY = eyJ... (dev project service role key)
```

**Development Environment (for local dev):**
```
SUPABASE_URL = https://yyy.supabase.co (dev project URL)
SUPABASE_ANON_KEY = eyJ... (dev project anon key)
```

3. Vercel automatically uses the correct values based on deployment type:
   - Production deployments → Production environment variables
   - Preview deployments → Preview environment variables

#### Step 3: Configure Branch Deployments

**In Vercel Dashboard:**
1. Go to Project Settings → Git
2. Configure:
   - **Production Branch:** `main` → Deploys to `shutterzilla.com`
   - **Preview Deployments:** All other branches → Create preview URLs

### Environment Workflow

**Daily Development:**
```
1. Create feature branch: git checkout -b feature/camera-search
2. Work on feature (days/weeks)
3. Push: git push origin feature/camera-search
   → Vercel creates preview URL automatically
   → Preview uses DEV Supabase (via environment variables)
4. Test on preview URL
5. Merge to main: git merge feature/camera-search
   → Vercel deploys to production automatically
   → Production uses PROD Supabase (via environment variables)
```

**No branch juggling. No merge conflicts. Simple.**

### Adding Staging Environment (Optional, Future)

If you need a staging environment later:

1. Create third Supabase project: `shutterzilla-test`
2. Create separate Vercel project: `shutterzilla-staging`
3. Configure staging to deploy from `main` branch
4. Set staging environment variables to use `shutterzilla-test`
5. Workflow: `main` → Staging (test) → Production (promote manually)

**When to add staging:**
- When you need more confidence before production
- When you need integration testing with other features
- When you have multiple developers

**For now:** Preview deployments are sufficient for solo dev.

---

## Data Seeding for Testing

### Overview

Preview deployments need realistic data for meaningful testing. ShutterZilla uses **artificial/generated test data** to seed the DEV Supabase database.

**Why Artificial Data:**
- ✅ Simple to implement
- ✅ Safe (no production data risk)
- ✅ Repeatable (generate anytime)
- ✅ Sufficient for most testing scenarios

### Data Seeding Strategy

#### What Gets Seeded

**Camera Listings:**
- 1000+ camera listings from various sources (Buyee, eBay)
- Various prices, conditions, brands
- Edge cases: Missing images, very high prices, sold items

**Users & Collections:**
- 10 test users with different collection sizes
- User 1: 50 cameras, 5 saved searches
- User 2: 2 cameras, 10 saved searches
- User 3: Empty collection (test empty states)

**Saved Searches:**
- Various search criteria (price ranges, brands, conditions)
- Some with matches, some without (test notifications)

### Implementation

#### Step 1: Create Seeding Script

Create `scripts/seed-dev-database.ts`:

```typescript
// scripts/seed-dev-database.ts
import { createClient } from '@supabase/supabase-js'
import { faker } from '@faker-js/faker'

const supabaseUrl = process.env.SUPABASE_DEV_URL!
const supabaseKey = process.env.SUPABASE_DEV_SERVICE_ROLE_KEY!
const supabase = createClient(supabaseUrl, supabaseKey)

// Generate realistic camera listing
function generateCameraListing() {
  const brands = ['Nikon', 'Canon', 'Leica', 'Pentax', 'Olympus', 'Minolta']
  const conditions = ['excellent', 'good', 'fair', 'poor']
  const sources = ['buyee', 'ebay']
  
  return {
    title: `${faker.helpers.arrayElement(brands)} ${faker.helpers.arrayElement(['FM2', 'AE-1', 'M6', 'K1000', 'OM-1', 'X-700'])} Camera ${faker.helpers.arrayElement(['Body', 'With Lens', 'Kit'])} ${faker.helpers.arrayElement(conditions).charAt(0).toUpperCase() + faker.helpers.arrayElement(conditions).slice(1)} Condition`,
    price: parseFloat(faker.commerce.price({ min: 50, max: 2000, dec: 2 })),
    source: faker.helpers.arrayElement(sources),
    condition: faker.helpers.arrayElement(conditions),
    url: `https://${faker.helpers.arrayElement(sources) === 'buyee' ? 'buyee.jp' : 'ebay.com'}/item/${faker.string.alphanumeric(10)}`,
    image_url: faker.image.url(),
    seller: faker.internet.userName(),
    created_at: faker.date.recent({ days: 30 }).toISOString(),
  }
}

// Generate test user
function generateTestUser(index: number) {
  return {
    email: `test_user_${index}@test.com`,
    password: 'TestPassword123!',
    // Supabase Auth will handle password hashing
  }
}

// Main seeding function
async function seedDatabase() {
  console.log('🌱 Starting database seeding...')
  
  // 1. Seed camera listings
  console.log('📷 Seeding camera listings...')
  const listings = []
  for (let i = 0; i < 1000; i++) {
    listings.push(generateCameraListing())
  }
  
  // Insert in batches of 100
  for (let i = 0; i < listings.length; i += 100) {
    const batch = listings.slice(i, i + 100)
    const { error } = await supabase
      .from('camera_listings')
      .insert(batch)
    
    if (error) {
      console.error('Error seeding listings:', error)
    } else {
      console.log(`✅ Seeded ${Math.min(i + 100, listings.length)}/${listings.length} listings`)
    }
  }
  
  // 2. Seed test users (via Supabase Auth)
  console.log('👥 Seeding test users...')
  for (let i = 1; i <= 10; i++) {
    const { data, error } = await supabase.auth.admin.createUser({
      email: `test_user_${i}@test.com`,
      password: 'TestPassword123!',
      email_confirm: true, // Auto-confirm email
    })
    
    if (error) {
      console.error(`Error creating user ${i}:`, error)
    } else {
      console.log(`✅ Created test user ${i}: test_user_${i}@test.com`)
      
      // Create collections for some users
      if (i <= 3) {
        // Create collections with varying sizes
        const collectionSize = i === 1 ? 50 : i === 2 ? 20 : 5
        // ... create collection entries
      }
    }
  }
  
  console.log('✅ Database seeding complete!')
}

// Run seeding
seedDatabase().catch(console.error)
```

#### Step 2: Add Dependencies

```bash
npm install --save-dev @faker-js/faker
```

#### Step 3: Add Script to package.json

```json
{
  "scripts": {
    "seed:dev": "tsx scripts/seed-dev-database.ts"
  }
}
```

#### Step 4: Set Up Environment Variables

Create `.env.local` for local seeding:

```bash
SUPABASE_DEV_URL=https://yyy.supabase.co
SUPABASE_DEV_SERVICE_ROLE_KEY=eyJ...
```

#### Step 5: Run Seeding

```bash
# Seed DEV Supabase with test data
npm run seed:dev
```

### Seeding Workflow

**Initial Setup:**
```bash
# After creating DEV Supabase project
npm run seed:dev
```

**Refresh Test Data:**
```bash
# Clear and reseed (add --refresh flag to script)
npm run seed:dev -- --refresh
```

**When to Reseed:**
- After major schema changes
- When test data becomes stale
- When you need fresh test data for new features

### Alternative: Production Data Snapshot (Advanced)

For more realistic testing, you can periodically copy production data (anonymized):

```typescript
// scripts/sync-dev-from-prod.ts
// 1. Export production data
// 2. Anonymize sensitive info (emails, names)
// 3. Import to DEV Supabase
```

**When to use:**
- When you need to test real production edge cases
- When artificial data doesn't catch real-world bugs
- As the project grows and data becomes more complex

**For now:** Artificial data is sufficient.

---

## GitHub Projects Setup

### Overview

GitHub Projects provides free, integrated project management for ShutterZilla. Perfect for solo dev learning project management basics.

**Why GitHub Projects:**
- ✅ Free and integrated with GitHub
- ✅ Simple Kanban boards
- ✅ Issues and PRs linked automatically
- ✅ Good for learning project management
- ✅ Perfect for solo dev workflow

### Setting Up GitHub Projects

#### Step 1: Create Project

1. Go to your GitHub repository
2. Click "Projects" tab
3. Click "New project"
4. Choose "Board" template
5. Name it: "ShutterZilla Development"

#### Step 2: Configure Columns

Set up Kanban columns:

- **Backlog** - Future work
- **To Do** - Ready to start
- **In Progress** - Currently working
- **In Review** - PR created, testing
- **Done** - Completed

#### Step 3: Create Issues from Implementation Plan

Convert your implementation plan checkboxes to GitHub Issues:

**Example:**
- Implementation Plan: "Set up Supabase Auth settings"
- GitHub Issue: "Set up Supabase Auth settings" #123
- Add labels: `phase-1`, `infrastructure`, `priority-high`

#### Step 4: Organize with Labels

Create labels for organization:

**By Phase:**
- `phase-1` - Phase 1: Complete Stack Setup
- `phase-2` - Phase 2: Database Foundation
- `phase-3` - Phase 3: Backend API Foundation
- etc.

**By Area:**
- `frontend` - Frontend work
- `backend` - Backend work
- `database` - Database work
- `infrastructure` - Infrastructure setup

**By Priority:**
- `priority-high` - High priority
- `priority-medium` - Medium priority
- `priority-low` - Low priority

**By Status:**
- `blocked` - Blocked by something
- `ready` - Ready to work on
- `in-progress` - Currently working

#### Step 5: Create Milestones

Create milestones for each phase:

- Milestone: "Phase 1: Complete Stack Setup"
- Milestone: "Phase 2: Database Foundation"
- Milestone: "Phase 3: Backend API Foundation"
- etc.

Link issues to milestones.

### GitHub Projects Workflow

**Daily Workflow:**
```
1. Pick issue from "To Do" column
2. Move to "In Progress"
3. Create feature branch: git checkout -b issue-123-setup-supabase
4. Work on issue
5. Create PR: "Fixes #123"
6. Move issue to "In Review"
7. Test on preview URL
8. Merge PR
9. Move issue to "Done"
```

**Linking PRs to Issues:**
- In PR description: `Fixes #123` or `Closes #123`
- GitHub automatically links PR to issue
- When PR merges, issue auto-closes

### Project Views

**Board View (Kanban):**
- Visual workflow
- Drag issues between columns
- See what's in progress

**Table View:**
- Detailed view with all fields
- Filter and sort issues
- Good for planning

**Roadmap View:**
- Timeline view
- See phases over time
- Good for long-term planning

### Best Practices

1. **One issue per task** - Keep issues focused
2. **Link PRs to issues** - Use `Fixes #123` in PR description
3. **Update issues regularly** - Add comments, update status
4. **Use labels consistently** - Makes filtering easier
5. **Close issues when done** - Keep board clean

---

## Daily Workflow Examples

### Example 1: Adding a New Feature

**Scenario:** Adding camera search functionality

```
Day 1: Planning
├─ Create GitHub Issue: "Add camera search feature" #45
├─ Add labels: phase-6, frontend, priority-high
├─ Move to "To Do" column
└─ Review mockup and specifications

Day 2-4: Development
├─ Move issue to "In Progress"
├─ Create branch: git checkout -b feature/camera-search
├─ Work on feature
├─ Push: git push origin feature/camera-search
│   └─→ Vercel creates preview URL automatically
│   └─→ Preview uses DEV Supabase (with seeded test data)
└─ Test on preview URL

Day 5: Review & Merge
├─ Create PR: "Adds camera search feature. Fixes #45"
├─ Move issue to "In Review"
├─ Test on preview URL again
├─ Merge PR to main
│   └─→ Vercel deploys to production automatically
│   └─→ Production uses PROD Supabase
└─ Move issue to "Done"
```

### Example 2: Fixing a Bug

**Scenario:** Login button not working

```
1. Create GitHub Issue: "Login button not working" #67
2. Add labels: bug, frontend, priority-high
3. Move to "To Do"
4. Move to "In Progress"
5. Create branch: git checkout -b fix/login-button
6. Fix bug
7. Push: git push origin fix/login-button
   └─→ Test on preview URL
8. Create PR: "Fixes login button. Fixes #67"
9. Move issue to "In Review"
10. Test on preview
11. Merge PR
12. Move issue to "Done"
```

### Example 3: Database Migration

**Scenario:** Adding user preferences table

```
1. Create GitHub Issue: "Add user preferences table" #89
2. Add labels: phase-2, database, priority-medium
3. Move to "In Progress"
4. Create migration file: supabase/migrations/20240101000000_add_user_preferences.sql
5. Write migration SQL
6. Test on DEV Supabase:
   ├─ Apply migration in Supabase dashboard
   └─ Verify schema
7. Commit migration: git commit -m "Add user preferences migration. Fixes #89"
8. Create PR
9. Move issue to "In Review"
10. Test migration on preview (uses DEV Supabase)
11. Merge PR
12. Apply migration to PROD Supabase manually
13. Move issue to "Done"
```

### Example 4: Seeding Fresh Test Data

**Scenario:** Need fresh test data for new feature testing

```
1. Run seeding script: npm run seed:dev
2. Wait for seeding to complete
3. Test new feature on preview URL
4. Verify test data is realistic and sufficient
```

---

## Troubleshooting

### Environment Issues

**Problem:** Preview deployment using wrong Supabase project

**Solution:**
1. Check Vercel environment variables
2. Verify Preview environment has DEV Supabase URL
3. Redeploy preview

**Problem:** Production deployment using wrong environment variables

**Solution:**
1. Check Vercel Project Settings → Environment Variables
2. Verify Production environment has correct values
3. Redeploy production

### Data Seeding Issues

**Problem:** Seeding script fails

**Solution:**
1. Check environment variables are set
2. Verify DEV Supabase project exists
3. Check service role key has correct permissions
4. Review error messages in console

**Problem:** Test data not realistic enough

**Solution:**
1. Enhance seeding script with more variety
2. Add more edge cases
3. Consider production data snapshot (anonymized)

### GitHub Projects Issues

**Problem:** Issues not linking to PRs

**Solution:**
1. Ensure PR description includes issue number: `Fixes #123`
2. Check issue exists and is open
3. Verify GitHub integration is enabled

**Problem:** Board view not updating

**Solution:**
1. Refresh page
2. Check issue status in table view
3. Verify filters aren't hiding issues

### Deployment Issues

**Problem:** Preview URL not created

**Solution:**
1. Check Vercel is connected to GitHub
2. Verify branch was pushed to GitHub
3. Check Vercel deployment logs

**Problem:** Production not deploying

**Solution:**
1. Check `main` branch was pushed
2. Verify Vercel production branch is set to `main`
3. Check Vercel deployment logs
4. Review `vercel.json` for build configuration

---

## Summary

**Environment Strategy:**
- ✅ Configuration-based (not branch-based)
- ✅ Two environments: Preview (DEV) + Production (PRD)
- ✅ Simple workflow: feature branch → preview → merge to main → production

**Data Seeding:**
- ✅ Artificial/generated test data
- ✅ Seeded DEV Supabase for realistic testing
- ✅ Repeatable and safe

**Project Management:**
- ✅ GitHub Projects for organization
- ✅ Issues linked to PRs
- ✅ Kanban workflow

**Daily Workflow:**
- ✅ Create issue → Work on feature → Test on preview → Merge to main → Production

---

## See Also

- [Tech Stack Guide](../specification/technical/tech-stack-guide.md) - Complete tech stack documentation
- [Runbook](../project/runbook.md) - Operations and troubleshooting guide
- [Implementation Plan](../specification/implementation/implementation-plan.md) - Step-by-step implementation plan
- [Vercel Configuration Location](./vercel-configuration-location.md) - Vercel setup details

---

**This guide will be updated as DevOps practices evolve.**
