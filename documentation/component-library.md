# Component Library Reference

This document provides a reference for the reusable components in the ShutterZilla platform.

## 1. Top Bar (`.topbar`)

The top bar is a consistent header across all app pages.

- **Structure:** `div.topbar` > `div.topbar__logo`, `div.topbar__title`, `div.topbar__right`
- **Styling:** White background, teal bottom border, 70px height.

## 2. Footer (`.footer`)

The footer is a consistent footer across all app pages.

- **Structure:** `footer.footer` > `div.footer__container` > `div.footer__brand`, `div.footer__section`
- **Styling:** Dark slate background, white/gray text.

## 3. Tabs (`.tabs`)

Tabs are used for navigation within an app.

- **Structure:** `div.tabs` > `a.tabs__item`
- **Styling:** Active tab has a teal bottom border.

## 4. Cards (`.card`)

Cards are used to display camera listings and other content.

- **Structure:** `div.card` > `div.card__image`, `div.card__body`
- **Styling:** White background, rounded corners, subtle shadow.

## 5. Badges (`.badge`)

Badges are used to display status and other information.

- **Classes:** `.badge--success`, `.badge--new`, `.badge--sold`
- **Styling:** Colored background with rounded corners.

## 6. Buttons (`.btn`)

Buttons are used for actions.

- **Classes:** `.btn--primary`, `.btn--outline`
- **Styling:** Teal primary button, gray outline button.

## 7. Pills (`.pill`)

Pills are used for tags and filters.

- **Classes:** `.pill--primary`, `.pill--secondary`, `.pill--outline`
- **Styling:** Colored background with rounded corners.

## 8. Source Icons (`.source-icon`)

Source icons are used to indicate the source of a camera listing.

- **Classes:** `.source-icon--mercari`, `.source-icon--buyee`, `.source-icon--ebay`
- **Styling:** Colored background with a single letter.
