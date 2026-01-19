# Watchlist and Archived Pages Review

**Pages:** `scraper-watchlist.html`, `scraper-archived.html`  
**Date:** 2026-01-XX  
**Status:** ✅ Aligned with Feed design

## Changes Made

### 1. Topbar Updates (Both Pages)
- ✅ Replaced user icon SVG with profile picture image (`./assets/profile-pic.jpg`)
- ✅ Added CSS for profile picture image styling (`overflow: hidden`, `object-fit: cover`)
- ✅ Verified dropdown order: Scraper, Collections, Negative (already correct)
- ✅ Verified dropdown links are correct (already using `scraper-feed.html`)

### 2. Footer Updates (Both Pages)
- ✅ Added Negative app link to footer Apps section

### 3. Mobile Menu
- ✅ Verified order matches `scraper-feed.html` (already correct)

## Design Consistency

Both pages now match the design patterns established in `scraper-feed.html`:

- **Topbar:** Consistent structure with profile picture, app dropdown, and icon navigation
- **Footer:** Includes all three apps (Scraper, Collections, Negative)
- **Styling:** Uses the same CSS classes and design tokens

## Page-Specific Features

### Watchlist Page
- Maintains its unique card structure for watched items
- Uses the same card design patterns as Feed page (with source icons, prices, actions)

### Archived Page
- Maintains its unique card structure for archived items
- Uses the same card design patterns as Feed page (with source icons, prices, actions)

## Notes

- Both pages use the same card structure as the Feed page, so they already had good consistency
- All navigation and branding elements are now consistent with the Feed page
- The pages maintain their unique functionality while sharing the same visual design language
