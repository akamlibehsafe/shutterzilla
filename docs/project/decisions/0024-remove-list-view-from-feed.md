# 0024 - Remove List View from Feed Page

## Status
Accepted

## Context
The feed page initially had two view options:
- Grid view (card-based layout with images)
- List view (text-heavy, compact layout)

After evaluating the design and user experience, we determined:
- Grid view is more visual and effective for camera browsing
- List view adds complexity without clear benefit
- Maintaining two views increases development and maintenance overhead
- Grid view works well across all screen sizes with responsive design

## Decision
Remove the list view option and keep only the grid view for the feed page.

**Changes made:**
- Removed view toggle buttons from the feed page header
- Deleted `scraper-feed-list.html` mockup file
- Simplified feed page to use grid layout exclusively

## Consequences
**Positive:**
- Simpler UI with fewer controls
- Reduced maintenance overhead (one view to maintain)
- Better visual browsing experience for camera listings
- Cleaner header row without toggle buttons
- Easier responsive design (one layout to optimize)

**Negative:**
- No alternative compact view for users who prefer dense information
- Less flexibility for different browsing preferences

## Notes
If needed in the future, list view could be reintroduced, but current design prioritizes visual browsing over information density for camera discovery.
