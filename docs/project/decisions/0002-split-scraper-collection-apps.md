# 0002 - Separate Scraper and Collection into Two Distinct Apps

## Status
Accepted

## Context
The platform has two primary user workflows:
1. **Discovery**: Browsing and searching for cameras from multiple marketplaces (Buyee, eBay)
2. **Collection Management**: Tracking personal camera collection, statistics, wishlist

These workflows have different:
- User goals (browsing vs. managing)
- Information needs (marketplace data vs. personal inventory)
- Interaction patterns (search/filter vs. CRUD operations)
- User mental models

Combining them into a single interface risked:
- Cognitive overload
- Navigation confusion
- Reduced focus on each task

## Decision
Split core functionality into two distinct applications accessible from a central App Switcher:
- **Scraper App**: Feed, search, saved searches, detail pages
- **Collection App**: Home, add camera, camera detail, statistics

## Alternatives considered
- **Single monolithic app**: Pros - simpler navigation, all features in one place. Cons - cognitive overload, hard to focus, confusing user journey
- **Tabs within single app**: Pros - easy switching. Cons - still feels cluttered, doesn't solve separation of concerns
- **Separate apps with switcher**: Pros - clear mental model, focused interfaces, simpler development. Cons - requires extra click to switch (minor)

## Consequences
- Each app has a focused, clean interface
- Users can mentally separate "browsing" from "managing"
- Easier to develop and maintain (clear boundaries)
- App Switcher provides easy navigation between contexts
- Can scale each app independently

## Links
- App Switcher mockup: `docs/mockups/v1/app-switcher.html`
- Functional Requirements: `docs/specification/functional/functional-requirements.md`
