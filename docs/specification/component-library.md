# Component Library Reference

This document provides a reference for the reusable UI components in the ShutterZilla platform, based on the `styles.css` file.

## 1. Core Layout

| Component | CSS Class | Description |
|---|---|---|
| **Top Bar** | `.topbar` | The main header navigation bar present on all application pages. It has a fixed height of 70px and a teal bottom border. |
| **Footer** | `.footer` | The main footer present on all application pages. It has a dark slate background and contains branding and navigation links. |
| **Page Content** | `.page-content` | A wrapper for the main content area of a page, providing consistent padding. |

## 2. Navigation

| Component | CSS Class | Description |
|---|---|---|
| **Tabs** | `.tabs` | A tab-based navigation element used within apps (e.g., Scraper, Collection). The active tab is indicated by a teal bottom border. |
| **View Toggle** | `.view-toggle` | A two-button toggle to switch between views, such as the Grid and List views in the Scraper feed. |

## 3. Cards

| Component | CSS Class | Description |
|---|---|---|
| **Card** | `.card` | The base component for displaying individual items like camera listings or collection entries. It features a white background, rounded corners, and a subtle shadow. |
| **Card Image** | `.card__image` | The container for the main image within a card. |
| **Card Body** | `.card__body` | The container for the text content within a card, including title, price, and metadata. |

## 4. Buttons & Interactive Elements

| Component | CSS Class | Description |
|---|---|---|
| **Button** | `.btn` | The base class for all buttons. |
| **Primary Button** | `.btn--primary` | A solid teal button used for primary actions (e.g., "Add Camera"). |
| **Outline Button** | `.btn--outline` | A button with a gray border and transparent background, used for secondary actions. |
| **Select/Dropdown** | `.select` | A styled dropdown element used in forms and for sorting controls. |

## 5. Badges, Pills & Icons

| Component | CSS Class | Description |
|---|---|---|
| **Badge** | `.badge` | Small, colored indicators used for status. Variants include `.badge--success`, `.badge--new`, and `.badge--sold`. |
| **Pill** | `.pill` | Rounded, tag-like elements used for filters and categories. Variants include `.pill--primary`, `.pill--secondary`, and `.pill--outline`. |
| **Ribbon** | `.ribbon` | An angled banner, typically used to indicate a "SOLD" status on a camera listing. |
| **Source Icon** | `.source-icon` | Small, colored icons that indicate the source of a scraper listing. Variants include `.source-icon--buyee` and `.source-icon--ebay`. |

## 6. Grid System

| Component | CSS Class | Description |
|---|---|---|
| **Grid** | `.grid` | The base class for creating a grid layout. |
| **3-Column Grid** | `.grid--3` | A grid with three equally-sized columns. |
| **4-Column Grid** | `.grid--4` | A grid with four equally-sized columns. |
| **5-Column Grid** | `.grid--5` | A grid with five equally-sized columns, used for the camera collection view. |
