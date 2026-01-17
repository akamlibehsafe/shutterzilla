# Topbar & Navigation Options Comparison - Scraper App

This folder contains **2 design options** (Option 3 and Option 4) for the topbar and navigation structure for the **Scraper App**. Each option has been rendered across all Scraper pages so you can test complete navigation flows.

## How to View

Navigate to the `option3/` or `option4/` folders and open any HTML file in your browser. All pages within each option link to other pages in the same option folder, so you can test complete navigation flows.

**Option 3 Folder:** `option3/`
**Option 4 Folder:** `option4/`

## Options Overview

### Option 3: Icon Navigation in Topbar
**Folder:** `option3/`

**Description:**
- Icons only in topbar (no text labels)
- Tooltips on hover show labels
- Very compact, modern look
- Minimalist design
- Navigation centered in topbar

**Best for:** Minimalist, icon-based navigation

**Pages Available:**
- `scraper-feed.html` - Main feed page
- `scraper-search.html` - Search with filters
- `scraper-saved.html` - Saved searches management

---

### Option 4: Sidebar Navigation
**Folder:** `option4/`

**Description:**
- Sidebar on left side for navigation
- Topbar stays minimal (logo + profile)
- Common in admin/desktop apps
- More space for navigation items
- Icons + text labels in sidebar

**Best for:** Desktop-focused, admin-style apps

**Pages Available:**
- `scraper-feed.html` - Main feed page
- `scraper-search.html` - Search with filters
- `scraper-saved.html` - Saved searches management
- `scraper-detail-nikon-fm2.html` - Camera detail page (Nikon)
- `scraper-detail-leica-m3.html` - Camera detail page (Leica)
- `scraper-detail-canon-ae1.html` - Camera detail page (Canon)

---

## Testing Navigation

**Within each option folder:**
- All links point to other pages in the same folder
- You can navigate between Feed, Search, and Saved Searches
- Detail pages link back to Feed
- Complete navigation flows are testable

**To test:**
1. Open `option3/scraper-feed.html` or `option4/scraper-feed.html` in your browser
2. Click through the navigation to test the flow
3. Compare how Option 3 vs Option 4 feels

---

## Comparison Notes

**On Mobile:**
- Both options use hamburger menu for mobile navigation
- Desktop navigation hidden on small screens
- Mobile menu provides full navigation access

**On Desktop:**
- **Option 3:** Icons in topbar center, tooltips on hover
- **Option 4:** Sidebar on left with icons + text labels
- Both maintain logo left, profile right in topbar

---

## Next Steps

1. Test both options by navigating through their pages
2. Compare how they look and feel
3. Choose your preferred option
4. We'll then apply it to all remaining Scraper App pages (detail pages for Option 3, etc.)

---

## File Structure

```
topbar-options-comparison/
├── option3/
│   ├── scraper-feed.html
│   ├── scraper-search.html
│   └── scraper-saved.html
├── option4/
│   ├── scraper-feed.html
│   ├── scraper-search.html
│   ├── scraper-saved.html
│   ├── scraper-detail-nikon-fm2.html
│   ├── scraper-detail-leica-m3.html
│   └── scraper-detail-canon-ae1.html
└── README.md
```
