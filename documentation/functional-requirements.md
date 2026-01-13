# Functional Requirements

This document outlines the functional requirements for the ShutterZilla platform.

## 1. Authentication

- Users can sign up with email/password or social login (Google, Facebook).
- Users can log in with email/password or social login.
- Users can reset their password via an email link.
- New users must verify their email address.

## 2. Scraper App

- **Feed:** Displays a grid or list of recent camera listings from all sources.
- **Search:** Allows users to search for cameras with filters:
  - Keyword
  - Brand
  - Price Range (min/max)
  - Condition (Mint, Excellent, Good, Fair, Poor)
  - Sources (Mercari, Buyee, eBay USA, JD Direct Auctions)
  - "Available items only" toggle
- **Saved Searches:** Users can save search criteria and receive notifications for new matches.
- **Camera Detail:** Displays detailed information about a single camera listing.

## 3. Collection App

- **Home:** Displays the user's personal camera collection.
- **Add Camera:** Users can add a new camera to their collection with details:
  - Brand, Model, Year, Condition, Value, Photo
- **Camera Detail:** Displays detailed information about a camera in the collection.
- **Statistics:** Displays charts and tables with statistics about the collection.

## 4. Admin Section

- **Dashboard:** Displays an overview of system statistics.
- **Users:** Admins can manage users, roles, and status.
- **Scraper Config:** Admins can enable/disable scraper sources and configure settings.
- **System Logs:** Admins can view and filter system logs.
- **Settings:** Admins can manage general and security settings.

## 5. General

- **Navigation:** Consistent top bar and footer across all app pages.
- **Responsiveness:** All pages should be responsive and work on mobile devices.
