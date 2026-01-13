# Screen Specifications

This document captures detailed specifications for each screen, including behavior, data requirements, and interactions. We'll work through each screen together, refining as we implement.

**Approach:** Screen-by-screen refinement and implementation

---

## Scraper App Screens

### Scraper Feed (Main Feed)
**Mockup:** `mockupsv2/scraper-feed.html`

#### Questions to Define:
- [ ] How do we determine what listings to show (default sort/filter)?
- [ ] How do we handle pagination/infinite scroll?
- [ ] What filters are available?
- [ ] How do filters work together (AND/OR)?
- [ ] How do we handle real-time updates?
- [ ] What data is shown in each listing card?
- [ ] How do we handle "sold" or "expired" listings?
- [ ] How do we handle images (lazy loading, placeholders)?

#### Data Requirements:
- [ ] What fields from Camera Listings are needed?
- [ ] Do we need to join with other tables?
- [ ] What aggregations are needed?

#### Interactions:
- [ ] Click on listing → Detail page
- [ ] Filter changes → Update feed
- [ ] Save search → Create saved search
- [ ] Other interactions?

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Scraper Search
**Mockup:** `mockupsv2/scraper-search.html`

#### Questions to Define:
- [ ] What search fields are available?
- [ ] How does search work (full-text, exact match, fuzzy)?
- [ ] How do we handle search history?
- [ ] How do we save searches?
- [ ] How do filters interact with search?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Saved Searches
**Mockup:** `mockupsv2/scraper-saved.html`

#### Questions to Define:
- [ ] How do we display saved searches?
- [ ] How do we edit/delete saved searches?
- [ ] How do we show match counts?
- [ ] How do we trigger searches?
- [ ] How do we handle notifications?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Listing Detail
**Mockup:** `mockupsv2/scraper-detail-*.html`

#### Questions to Define:
- [ ] What information is shown?
- [ ] How do we handle multiple images?
- [ ] How do we link to original listing?
- [ ] How do we handle "add to collection"?
- [ ] How do we handle "save search" from detail?
- [ ] How do we track views?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

## Collection App Screens

### Collection Home
**Mockup:** `mockupsv2/collection_home.html`

#### Questions to Define:
- [ ] How do we display cameras (grid, list)?
- [ ] What sorting options?
- [ ] What filtering options?
- [ ] How do we handle empty state?
- [ ] How do we show statistics?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Add Camera
**Mockup:** `mockupsv2/collection_add.html`

#### Questions to Define:
- [ ] What fields are required vs optional?
- [ ] How do we handle image uploads?
- [ ] How do we validate input?
- [ ] How do we handle camera model selection (autocomplete, search)?
- [ ] How do we link to marketplace listings?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Camera Detail
**Mockup:** `mockupsv2/collection_detail.html`

#### Questions to Define:
- [ ] What information is shown?
- [ ] How do we handle editing?
- [ ] How do we handle deletion?
- [ ] How do we handle multiple photos?
- [ ] How do we show related marketplace listings?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Collection Statistics
**Mockup:** `mockupsv2/collection_stats.html`

#### Questions to Define:
- [ ] What statistics do we show?
- [ ] How do we calculate statistics?
- [ ] How do we handle charts/visualizations?
- [ ] What time periods (all time, by year, etc.)?

#### Data Requirements:
_(To be defined)_

#### Interactions:
_(To be defined)_

#### Current Specification:
_(To be refined as we work through this screen)_

---

## Authentication Screens

### Landing Page
**Mockup:** `mockupsv2/landing-page.html`

#### Questions to Define:
- [ ] What information is shown?
- [ ] How do we handle "already logged in" state?
- [ ] What CTAs are available?

#### Current Specification:
_(To be refined as we work through this screen)_

---

### Sign Up / Sign In
**Mockup:** `mockupsv2/auth_sign-up.html`, `mockupsv2/auth_forgot-password.html`, etc.

#### Questions to Define:
- [ ] What validation is needed?
- [ ] How do we handle OAuth flows?
- [ ] How do we handle errors?
- [ ] What happens after sign up/sign in?

#### Current Specification:
_(To be refined as we work through this screen)_

---

## Admin Screens

_(To be defined as we approach admin functionality)_

---

## Notes

- Each screen will be refined as we implement it
- Questions will be answered through discussion
- Specifications will be updated as we learn and refine
- Changes from mockups will be documented in `implementation-mockup-to-code-changes.md`
