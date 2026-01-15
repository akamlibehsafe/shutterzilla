# Functional Requirements

This document outlines the functional requirements for the ShutterZilla platform, based on the finalized HTML/CSS mockups.

## 1. Core & Authentication

The core of the platform involves user authentication and navigation between the main applications.

| Feature | Requirement |
|---|---|
| **User Registration** | Users must be able to sign up using an email and password. The mockup also includes placeholders for social sign-up (Google, Facebook). |
| **User Login** | Registered users must be able to log in with their email and password. Social login is also an option. |
| **Password Reset** | Users must be able to request a password reset via an email link and set a new password. |
| **Email Verification** | New users should be prompted to verify their email address to activate their account. |
| **App Switcher** | After logging in, users are directed to a simple page allowing them to navigate to either the **Scraper App** or the **Collection App**. |

## 2. Scraper App

The Scraper App is focused on discovering vintage camera listings from various online marketplaces.

| Feature | Requirement |
|---|---|
| **Feed View** | The main feed must display recent camera listings. It must support both a **Grid View** (`scraper-feed.html`) for visual browsing and a **List View** (`scraper-feed-list.html`) for denser information display. |
| **Search & Filtering** | A dedicated search page (`scraper-search.html`) must provide filtering capabilities. All filter fields below are required. |
| **Saved Searches** | Users must be able to save a set of filter criteria as a "Saved Search" for quick access later (`scraper-saved.html`). |
| **Camera Details** | Clicking on a listing must lead to a detailed view (`scraper-detail-*.html`) showing all available information for that camera. |

### Search Filter Fields

| Field | Type | Options/Notes |
|---|---|---|
| **Keyword** | Text Input | Free-text search for camera names, models, etc. |
| **Brand** | Text Input | e.g., "Nikon", "Leica", "Canon" |
| **Price Range** | Min/Max Input | Two fields for minimum and maximum price. |
| **Condition** | Checkboxes | Mint, Excellent, Good, Fair, Poor |
| **Source** | Checkboxes | Buyee, eBay USA |
| **Availability** | Toggle Switch | "Available items only" |

## 3. Collection App

The Collection App allows users to manage their personal inventory of vintage cameras.

| Feature | Requirement |
|---|---|
| **Collection Home** | The main view (`collection_home.html`) displays the user's personal camera collection, with the ability to filter between "Owned" and "Wishlist" items. |
| **Add Camera** | Users must be able to add a new camera to their collection via a form (`collection_add.html`). See fields below. |
| **Camera Detail** | Viewing a camera from the collection (`collection_detail.html`) shows all its stored details and allows for editing. |
| **Statistics** | A statistics page (`collection_stats.html`) must visualize data about the user's collection, such as total value, brand distribution, etc., using charts (implemented with Chart.js in the mockup). |

### Add Camera Form Fields

| Field | Type | Notes |
|---|---|---|
| **Brand** | Text Input | e.g., "Nikon" |
| **Model** | Text Input | e.g., "FM2" |
| **Year** | Number Input | Year of manufacture |
| **Condition** | Select/Dropdown | Mint, Excellent, Good, Fair, Poor |
| **Purchase Price** | Number Input | The price the user paid |
| **Current Value** | Number Input | The estimated current market value |
| **Serial Number** | Text Input | Optional serial number |
| **Notes** | Text Area | User's personal notes |
| **Photo** | File Upload | An image of the camera |

## 4. Admin Section

The Admin Section provides administrative control over the platform.

| Feature | Requirement |
|---|---|
| **Dashboard** | (`admin_dashboard.html`) Must display key system statistics and activity metrics. |
| **User Management** | (`admin_users.html`) Admins must be able to view, search, and manage user accounts (e.g., change roles, suspend accounts). |
| **Scraper Configuration** | (`admin_scraper.html`) Admins must be able to enable/disable scraper sources and adjust scraping parameters. |
| **System Logs** | (`admin_logs.html`) Admins must be able to view and filter system logs for debugging and monitoring. |
| **Settings** | (`admin_settings.html`) Admins must be able to manage general platform settings. |

## 5. General Requirements

| Feature | Requirement |
|---|---|
| **Standardized Navigation** | All app pages (excluding landing and auth pages) must include the consistent **Top Bar** and **Footer** components. |
| **Responsiveness** | All pages must be fully responsive and provide a seamless experience on both desktop and mobile devices. |
| **Logo Linking** | The main logo in the top bar must always link back to the App Switcher page (`app-switcher.html`). |
