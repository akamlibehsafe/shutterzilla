# 0016 - Use Tailwind CSS for Styling

## Status
Accepted

## Context
Need CSS framework/styling approach for Vue.js frontend. Options include:
- Traditional CSS files
- CSS modules
- CSS-in-JS (styled-components, etc.)
- Utility-first CSS (Tailwind)

Requirements:
- Fast development
- Consistent design
- Good developer experience
- Works well with Vue.js
- Responsive design support

## Decision
Use **Tailwind CSS** (utility-first CSS framework) for all styling in the Vue.js frontend.

## Alternatives considered
- **Traditional CSS/SCSS**: Pros - familiar, full control. Cons - more verbose, slower development, need to write custom responsive code
- **CSS Modules**: Pros - scoped styles. Cons - still need to write CSS, slower than utility classes
- **Styled-components (CSS-in-JS)**: Pros - component-scoped. Cons - runtime overhead, different mental model, less popular with Vue
- **Bootstrap/Bulma**: Pros - component library. Cons - less flexible, larger bundle, opinionated design
- **Tailwind CSS**: Pros - very fast development, utility classes, responsive design built-in, small bundle (purged unused), consistent design system, great Vue.js integration. Cons - different approach (utility-first), but easy to learn

## Consequences
- Much faster UI development (utility classes)
- Consistent spacing and colors (design system)
- Built-in responsive design utilities
- Small bundle size (unused CSS purged)
- Easy to maintain (no separate CSS files for most cases)
- Great developer experience (autocomplete, IntelliSense)
- Can still use custom CSS when needed
- Different mental model (utility-first) but easy to learn

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Design System: `docs/specification/design/design-system.md`
