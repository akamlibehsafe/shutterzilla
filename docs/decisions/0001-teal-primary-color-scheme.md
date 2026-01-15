# 0001 - Adopt Teal-based Primary Color Scheme

## Status
Accepted

## Context
ShutterZilla needed a distinctive visual identity that would:
- Differentiate from traditional vintage camera sites (often using brown/orange/sepia tones)
- Evoke modernity and trust
- Provide a vibrant accent against a clean, minimal gray and white layout
- Work well across all application pages (scraper, collection, admin)

## Decision
Adopt teal (`#0d9488`) as the primary brand color, with a lighter variant (`#14b8a6`) for hover states and accents.

## Alternatives considered
- **Brown/sepia tones**: Pros - traditional, vintage feel. Cons - overused, feels dated, doesn't stand out
- **Orange/red tones**: Pros - energetic. Cons - associated with urgency/alerts, can be overwhelming
- **Blue tones**: Pros - trustworthy. Cons - very common, less distinctive
- **Teal**: Pros - modern, distinctive, trustworthy, works well with grays. Cons - none significant for this use case

## Consequences
- Brand identity is established and consistent across all mockups
- Color scheme works well for both dark and light UI elements
- Provides clear visual hierarchy with accent color
- Easy to implement in CSS with CSS variables (already done in mockups)

## Links
- Design System: `docs/specification/design-system.md`
- Mockups: `docs/mockupsv1/`, `docs/mockupsv2/`
