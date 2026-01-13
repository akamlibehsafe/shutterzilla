# Page Inventory & Sitemap

This document provides a complete inventory of all 26 pages in the ShutterZilla platform and their relationships.

## Sitemap

_Note: All pages with a top bar (excluding auth and landing pages) have a profile icon that links to `admin_dashboard.html`._

```
/ (landing-page.html)
├── auth_sign-up.html
├── auth_forgot-password.html
├── auth_reset-password.html
├── auth_email-verification.html
├── auth_password-reset-sent.html
├── app-switcher.html
│   ├── scraper-feed.html
│   │   ├── scraper-feed-list.html
│   │   ├── scraper-search.html
│   │   ├── scraper-saved.html
│   │   ├── scraper-detail-nikon-fm2.html
│   │   ├── scraper-detail-leica-m3.html
│   │   └── scraper-detail-canon-ae1.html
│   └── collection_home.html
│       ├── collection_add.html
│       ├── collection_detail.html
│       └── collection_stats.html
├── admin_dashboard.html
│   ├── admin_users.html
│   ├── admin_scraper.html
│   ├── admin_logs.html
│   └── admin_settings.html
├── about.html
├── privacy.html
└── terms.html
```

## Page Inventory

| Section | Page | File | Purpose |
|---|---|---|---|
| **Core** | Landing Page | `landing-page.html` | Main entry point with login/signup options. |
| | App Switcher | `app-switcher.html` | Selection page to choose between Scraper and Collection apps. |
| **Authentication** | Sign Up | `auth_sign-up.html` | New user registration form. |
| | Forgot Password | `auth_forgot-password.html` | Form to request a password reset link. |
| | Reset Password | `auth_reset-password.html` | Form to set a new password via a tokenized link. |
| | Email Verification | `auth_email-verification.html` | Page instructing user to check their email to verify their account. |
| | Password Reset Sent | `auth_password-reset-sent.html` | Confirmation page after requesting a password reset. |
| **Scraper App** | Feed (Grid View) | `scraper-feed.html` | Main feed of camera listings in a visual grid. |
| | Feed (List View) | `scraper-feed-list.html` | Compact list view of camera listings. |
| | Search | `scraper-search.html` | Page with advanced filters to search for cameras. |
| | Saved Searches | `scraper-saved.html` | Displays a list of the user's saved search queries. |
| | Camera Detail (Nikon) | `scraper-detail-nikon-fm2.html` | Example detail page for a specific camera listing. |
| | Camera Detail (Leica) | `scraper-detail-leica-m3.html` | Example detail page for a specific camera listing. |
| | Camera Detail (Canon) | `scraper-detail-canon-ae1.html` | Example detail page for a specific camera listing. |
| **Collection App** | Home | `collection_home.html` | View of the user's personal camera collection. |
| | Add Camera | `collection_add.html` | Form to add a new camera to the collection. |
| | Camera Detail | `collection_detail.html` | Detailed view of a camera in the user's collection. |
| | Statistics | `collection_stats.html` | Visualization of collection data (e.g., value over time). |
| **Admin Section** | Dashboard | `admin_dashboard.html` | Overview of system statistics and activity. |
| | Users | `admin_users.html` | Manage platform users, roles, and status. |
| | Scraper Config | `admin_scraper.html` | Configure scraper sources and settings. |
| | System Logs | `admin_logs.html` | View and filter system-level logs. |
| | Settings | `admin_settings.html` | Manage general platform and security settings. |
| **Legal** | About | `about.html` | Information about the ShutterZilla platform. |
| | Privacy Policy | `privacy.html` | The platform's privacy policy. |
| | Terms of Service | `terms.html` | The platform's terms of service. |
