# Page Inventory & Sitemap

This document provides a complete inventory of all pages in the ShutterZilla platform and their relationships.

## Sitemap

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
│   │   └── scraper-detail-*.html
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
| **Core** | Landing Page | `landing-page.html` | Main entry point with login |
| | App Switcher | `app-switcher.html` | Choose between Scraper and Collection apps |
| **Authentication** | Sign Up | `auth_sign-up.html` | New user registration |
| | Forgot Password | `auth_forgot-password.html` | Request password reset |
| | Reset Password | `auth_reset-password.html` | Set new password |
| | Email Verification | `auth_email-verification.html` | Confirm email after registration |
| | Password Reset Sent | `auth_password-reset-sent.html` | Confirmation after reset request |
| **Scraper App** | Feed (Grid) | `scraper-feed.html` | Main feed of camera listings |
| | Feed (List) | `scraper-feed-list.html` | List view of camera listings |
| | Search | `scraper-search.html` | Search for cameras with filters |
| | Saved Searches | `scraper-saved.html` | Manage saved searches and notifications |
| | Camera Detail | `scraper-detail-*.html` | Detailed view of a single camera listing |
| **Collection App** | Home | `collection_home.html` | View personal camera collection |
| | Add Camera | `collection_add.html` | Add a new camera to the collection |
| | Camera Detail | `collection_detail.html` | Detailed view of a camera in the collection |
| | Statistics | `collection_stats.html` | View statistics about the collection |
| **Admin Section** | Dashboard | `admin_dashboard.html` | Overview of system stats |
| | Users | `admin_users.html` | Manage users and roles |
| | Scraper Config | `admin_scraper.html` | Configure scraper sources and settings |
| | System Logs | `admin_logs.html` | View system logs |
| | Settings | `admin_settings.html` | Manage general and security settings |
| **Legal** | About | `about.html` | Information about ShutterZilla |
| | Privacy Policy | `privacy.html` | Privacy policy |
| | Terms of Service | `terms.html` | Terms of service |
