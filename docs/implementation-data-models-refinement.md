# Data Models Refinement

This document captures the refinement process for data models. We'll work through each model together, defining fields, relationships, and behavior.

**Status:** In Progress  
**Approach:** Refine models screen-by-screen as we implement

---

## Camera Listings (Scraper Data)

**Source:** Scraped from external marketplaces

### Questions to Define:
- [ ] What fields do we capture from each source?
- [ ] How do we handle different field names across sources?
- [ ] What fields are required vs optional?
- [ ] How do we store pricing (currency, original vs converted)?
- [ ] How do we handle images (URLs, storage)?
- [ ] How do we track listing status (active, sold, expired)?
- [ ] How do we deduplicate listings across sources?
- [ ] What metadata do we store (scraped date, source, etc.)?

### Current Thinking:
_(To be refined as we work through screens)_

---

## Saved Searches

**Purpose:** User-defined search criteria that trigger notifications

### Questions to Define:
- [ ] What search criteria can users save?
- [ ] How do we store search parameters (JSON? separate fields?)?
- [ ] How do we handle price ranges?
- [ ] How do we handle multiple conditions (AND/OR)?
- [ ] How often do we check for matches?
- [ ] How do we notify users of matches?
- [ ] Do we store search history?

### Current Thinking:
_(To be refined as we work through screens)_

---

## Collection Cameras

**Purpose:** User's personal camera collection

### Questions to Define:
- [ ] What fields do we track for each camera?
- [ ] How do we handle camera variants/models?
- [ ] How do we store purchase information?
- [ ] How do we handle photos (user uploads)?
- [ ] What condition/status fields?
- [ ] How do we track accessories?
- [ ] How do we link to marketplace listings (wishlist)?

### Current Thinking:
_(To be refined as we work through screens)_

---

## Users

**Purpose:** User accounts and profiles

### Questions to Define:
- [ ] What profile information do we store?
- [ ] How do we handle OAuth user data?
- [ ] What preferences do we track?
- [ ] How do we handle user roles (admin, regular user)?

### Current Thinking:
_(To be refined as we work through screens)_

---

## Notes

- We'll refine each model as we work through the screens that use them
- Changes will be documented with rationale
- Final schema will be reflected in Prisma schema and migrations
