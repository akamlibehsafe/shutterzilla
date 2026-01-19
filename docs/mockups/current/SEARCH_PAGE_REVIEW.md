# Scraper Search Page UI Review

**Date:** 2026-01-XX  
**Status:** ✅ Reviewed and Updated  
**Reference:** `scraper-feed.html` (Design Foundation)

---

## Review Summary

The Search page has been reviewed and updated to align with Feed page design decisions and styling patterns.

---

## Changes Made

### 1. Topbar Updates ✅
- **Fixed dropdown link**: Changed `../option3/scraper-feed.html` → `scraper-feed.html`
- **Updated user icon**: Replaced SVG with profile picture image (`./assets/profile-pic.jpg`)
- **Added CSS**: Added `.topbar-option3__user-icon img` styles for proper image display

### 2. Header Row Added ✅
- **Added header row** above search container with:
  - Source filter pills (Buyee, eBay) - single source selection (no "All" option)
  - Sort dropdown (Newest, Price: Low to High, Price: High to Low) - matching Feed pattern
- **Styling**: Applied Feed header row styles for consistency
- **Decision**: Removed "All" pill - users select one source at a time (see Decision 0027)

### 3. Card Structure Updated ✅
- **Source icons**: Updated to use `source-icon-wrapper` with proper icon images (matching Feed)
  - Buyee icon with Mercari subtype badge
  - eBay icon with badge image
- **Price format**: Changed to `card__prices` with `card__price-row` structure (matching Feed)
  - Price labels and values properly structured
  - Supports dual price rows (for auctions)
- **Card actions**: Added watch and archive buttons (matching Feed)
  - Watch button with eye icon
  - Archive/dismiss button with archive icon
- **Data attributes**: Added proper data attributes (`data-source`, `data-availability`, `data-shop`, `data-is-new`)
- **Grid**: Changed from `grid--3` to `grid--6` for consistency with Feed

### 4. Footer Updated ✅
- **Added Negative link**: Added Negative app to footer Apps section

### 5. Styling Consistency ✅
- **Card image container**: Updated to match Feed styling (140px height, proper image sizing)
- **Header row styles**: Applied Feed header row CSS patterns
- **Responsive design**: Ensured mobile/tablet/desktop breakpoints match Feed

---

## Design Decisions

### Search-Specific Features Retained
- **Filter sidebar**: Kept the left sidebar with advanced filters (Brand, Price Range, Condition, Source)
  - This is appropriate for Search page as it provides more filtering options than Feed
  - Sidebar is 300px wide on desktop, full width on mobile
- **Grid layout**: Changed to `grid--6` to match Feed, but sidebar takes space on desktop
  - Results area adapts to available space

### Consistency with Feed
- **Card structure**: Fully matches Feed card structure
- **Header controls**: Uses same pills and sort dropdown pattern
- **Topbar**: Identical to Feed topbar
- **Footer**: Same footer structure with all apps

---

## Remaining Considerations

### Unused Styles
- `.search-results__header`, `.search-results__title`, `.search-results__count` styles exist but are not used
- **Decision**: Keep for potential future use (results count display)
- Could be added above results grid if needed

### Grid Size
- Changed from `grid--3` to `grid--6` for consistency
- With sidebar, results may appear narrower than Feed
- **Consideration**: May want to adjust sidebar width or grid columns based on user feedback

---

## Testing Checklist

- [x] Topbar renders correctly
- [x] Dropdown links work
- [x] Profile picture displays
- [x] Header row displays with pills and sort
- [x] Filter sidebar works on mobile and desktop
- [x] Cards match Feed card structure
- [x] Source icons display correctly
- [x] Price format matches Feed
- [x] Watch/Archive buttons work
- [x] Footer includes all apps
- [ ] Responsive design tested (mobile/tablet/desktop)
- [ ] Filter functionality works
- [ ] Sort functionality works

---

## Next Steps

1. **Test responsive design** - Verify layout on mobile, tablet, desktop
2. **Test interactions** - Verify filter, sort, and card actions work
3. **Review with stakeholders** - Get feedback on Search page design
4. **Proceed to next page** - Review Saved Searches page

---

## Notes

- Search page maintains its unique filter sidebar while aligning card structure with Feed
- Header row provides consistent navigation and sorting across Scraper pages
- Cards are now fully consistent with Feed, enabling shared component reuse in implementation
