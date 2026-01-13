# Implementation Validation Notes

This document captures notes, observations, and results from the validation phase. It mirrors the structure of `implementation-validation-plan.md`.

**Purpose:** To document what we learn during validation testing, especially scraping feasibility.

---

## Phase 0.1: High-Level Behavior & Requirements Discussion

**Status:** Not Started

### Define User Journeys

#### Landing Page
**Purpose:** Entry point for shutterzilla.com - shows marketing/information content and login options.

**Flow:**
- When a user visits shutterzilla.com, the landing page loads
- **If user is already logged in:** Automatically redirect to App Switcher
- **If user is not logged in:** Display landing page with:
  - Marketing/information content about Shutterzilla
  - Login form (email + password)
  - Social login options (if applicable)
  - "Create Account" link/button → navigates to Sign Up page
  - "Forgot Password" link → navigates to Forgot Password page

**User Actions:**
- Enter email and password to log in
- Click social login button (if available) → completes social authentication
- Click "Create Account" → goes to Sign Up page
- Click "Forgot Password" → goes to Forgot Password page

#### Authentication Pages
**Purpose:** Handle user authentication flows (sign up, sign in, password reset, email verification).

**Pages Included:**
1. **Sign Up Page** - Accessed via "Create Account" link from landing page
   - User enters: email, password, confirm password
   - After submission: Send email verification
   - Redirect to: Email Verification page or confirmation message

2. **Sign In Page** - The login form on landing page (or separate page if preferred)
   - User enters: email and password
   - On success: Redirect to App Switcher
   - Includes: "Forgot Password" link

3. **Forgot Password Page** - Accessed via "Forgot Password" link
   - User enters: email address
   - After submission: Send password reset email
   - Redirect to: Password Reset Sent confirmation page

4. **Password Reset Page** - Accessed via link in password reset email
   - User enters: new password and confirmation
   - After submission: Redirect to login/sign in page

5. **Email Verification Page** - Shows verification status or resend options
   - User clicks verification link from email
   - After verification: Can proceed to sign in

#### App Switcher
**Purpose:** Central hub where logged-in users choose which app (Scraper or Collection) to access.

**Access Control:**
- **If user is logged in and visits shutterzilla.com:** Automatically redirect to App Switcher
- **If unauthenticated user tries to access App Switcher:** Redirect to Landing page for login

**Flow:**
- User sees available apps (Scraper App, Collection App)
- User clicks on an app → navigates to that app's main page
- User can switch between apps from the app switcher
- User can log out from app switcher  


#### Scraper App user journey

**Purpose:** Discover new cameras on source websites (Mercari, Buyee, Yahoo Japan Auctions, eBay), and allow users to categorize, mark, and save them for later review.

**Entry Point:**
- User navigates to Scraper App from App Switcher
- Landing on: **Feed page** (scraper-feed.html / scraper-feed-list.html)

---

### Scraper App Pages

#### Page 1: Feed
**Mockup File:** `scraper-feed.html` / `scraper-feed-list.html`

**Purpose:** Display personalized feed of camera listings relevant to the user

**What it shows:**
- Listings that match user's saved searches (automatic matches)
- Listings from automated scrapes (background scraping results)
- _[Logic for how entries are included will be defined later]_
- **Sorting:** User can choose sorting options (default: "Most recent listing" - newest first)
  - Available options: Most recent, Price, and others
  - User can invert order (ascending/descending)
- **Filtering:** Dismissed listings are NOT shown in Feed

**User Actions:**
- Scroll/browse through listings
- Click on a listing → Navigate to **Detail page**
- Mark listing as "Watch" → Adds to Watch list
- **Mark listing as "Dismissed"** → Listing is grayed out and hidden from Feed and future search results
- Navigate to other pages: Search, Saved Search, Watch, App Switcher

**Navigation From:**
- App Switcher (entry point)
- Other Scraper App pages

**Navigation To:**
- Detail page (when clicking a listing)
- Search page
- Saved Search page
- Watch page
- App Switcher

---

#### Page 2: Search
**Mockup File:** `scraper-search.html`

**Purpose:** Perform searches on source websites (Mercari, Buyee, Yahoo Japan Auctions, eBay) to find camera listings

**What it shows:**
- Search interface/form with search criteria
- Search results (listings matching the search criteria)
- **Sorting:** User can choose sorting options (default: "Most recent listing" - newest first)
  - Available options: Most recent, Price, and others
  - User can invert order (ascending/descending)
- **Filtering:** Dismissed listings are NOT shown in search results

**User Actions:**
- Enter search criteria and perform search
- View search results
- **Save search** (optional) - Save search criteria for later or automated execution (saved searches add matches to Feed)
- Click on a listing → Navigate to **Detail page**
- Mark listing as "Watch" → Adds to Watch list
- **Mark listing as "Dismissed"** → Listing is grayed out and hidden from Feed and future search results
- Navigate to other pages: Feed, Saved Search, Watch, App Switcher

**Navigation From:**
- Feed page
- Other Scraper App pages

**Navigation To:**
- Detail page (when clicking a listing)
- Saved Search page (when saving a search)
- Watch page
- Feed page (saved searches add to feed)
- App Switcher

---

#### Page 3: Saved Search
**Mockup File:** `scraper-saved.html`

**Purpose:** List and maintain saved searches. Manage which searches are active (adding listings to Feed) or inactive.

**What it shows:**
- List of user's saved searches
- Status of each saved search (active/inactive)
- Search criteria for each saved search

**User Actions:**
- View all saved searches
- **Activate/Deactivate saved searches** - Toggle whether a saved search is active
  - Active saved searches → Automatically add matching listings to Feed
  - Inactive saved searches → Do not add to Feed
- Edit saved searches (modify criteria)
- Delete saved searches
- Create new saved searches (or navigate to Search page to create)
- View matches/results for a saved search (if applicable)
- Navigate to other pages: Feed, Search, Watch, App Switcher

**Navigation From:**
- Feed page
- Search page (after saving a search)
- Other Scraper App pages

**Navigation To:**
- Search page (when creating/editing searches)
- Feed page (active searches add listings here)
- Watch page
- App Switcher

---

#### Page 4: Watch
**Mockup File:** _[Not yet created - needs to be designed]_

**Purpose:** View all listings the user has marked to watch/follow

**What it shows:**
- All listings user has marked to watch
- **Important:** Listings remain visible even if they become sold or unavailable on source websites
- Listing status/information for each watched listing (including sold/unavailable status if applicable)
- Options to remove listings from watch list

**User Actions:**
- View all watched listings
- Click on a watched listing → Navigate to **Detail page**
- Remove listing from watch list
- Navigate to other pages: Feed, Search, Saved Search, App Switcher

**Navigation From:**
- Feed page
- Search page
- Saved Search page
- Detail page (after marking as watch)
- Other Scraper App pages

**Navigation To:**
- Detail page (when clicking a watched listing)
- Feed page
- Search page
- Saved Search page
- App Switcher

---

#### Page 5: Detail
**Mockup File:** `scraper-detail-*.html` (e.g., scraper-detail-nikon-fm2.html)

**Purpose:** Display detailed information about a specific camera listing

**What it shows:**
- Full listing information
- Images
- Price, condition, source
- Seller information (if available)
- Link to original listing

**User Actions:**
- Mark listing as "Watch" → Adds to Watch list
- **Mark listing as "Dismissed"** → Listing is grayed out and hidden from Feed and future search results
- Add to Collection (links to Collection App)
- View original listing (external link)
- Share listing
- Navigate back to previous page
- Navigate to other pages: Feed, Search, Saved Search, Watch, App Switcher

**Navigation From:**
- Feed page (when clicking a listing)
- Search page (when clicking a listing)
- Saved Search page (when clicking a listing)
- Watch page (when clicking a watched listing)

**Navigation To:**
- Watch page (when marking as watch)
- Collection App (when adding to collection)
- External site (when viewing original listing)
- Previous page (back navigation)
- Feed, Search, Saved Search, Watch pages
- App Switcher

---

### Cross-Page Features

**Mark as Watch:**
- Available from: Feed, Search, Saved Search, Detail pages
- Action: Adds listing to user's Watch list
- Result: Listing appears on Watch page

**Mark as Dismissed:**
- Available from: Any page showing listings (Feed, Search results, Detail page)
- Action: Marks listing as dismissed
- Visual: Listing is grayed out (not yet mocked up)
- Result: Dismissed listings are hidden from:
  - Feed page
  - New search results
- Note: Dismissed listings remain in Watch list if previously marked as watch
- **Implementation Consideration:** Dismissed list can grow large over time. Need mechanism to clean up/remove listings from dismissed list when listings no longer exist on source websites (sold, removed, expired). Implementation approach to be determined.

**Sorting:**
- Available on: Feed page, Search results page
- Default: "Most recent listing" (newest first)
- User-configurable options:
  - Sort by: Most recent, Price, and other criteria
  - Order: Ascending/Descending (user can invert)
- User's sorting preference may be remembered per page

**Navigation:**

**Within Scraper App:**
- Top menu bar with pages listed (centered)
  - Pages shown: Feed, Search, Saved Search, Watch (and possibly others)
  - Users click on page names to navigate between pages
- Check mockups for exact navigation menu design

**Between Apps (Scraper ↔ Collection):**
- Click on main logo in topbar → Shows App Switcher
- From App Switcher, user can select which app to use (Scraper App or Collection App)

**General Navigation:**
- Users can navigate between pages using the top menu
- Users can return to App Switcher by clicking the logo in the topbar

**Notes:**
- **Dismissed Listings Cleanup:** The dismissed list can become large over time. Many dismissed listings may no longer exist on source websites (sold, removed, expired). Need to implement a cleanup mechanism to remove obsolete listings from the dismissed list. Implementation approach to be determined (e.g., periodic verification checks, user-initiated cleanup, automated background cleanup based on listing age, etc.).

#### Collection App user journey

**Purpose:** Store and display information and statistics of a collection of cameras, lenses, and other photography-related items (e.g., flashes, lightmeters, caps, etc.)

**Entry Point:**
- User navigates to Collection App from App Switcher
- Landing on: **Home page** (collection_home.html)

---

### Collection App Pages

#### Page 1: Home
**Mockup File:** `collection_home.html`

**Purpose:** Show a listing of all items in the collection (cameras, lenses, other photography items)

**What it shows:**
- Listing of all collection items
- Filtering options:
  - Toggles
  - Dropdown filter selector
  - Search terms/text input
- Items can be filtered by various criteria (to be defined: type, brand, condition, etc.)

**User Actions:**
- View all collection items
- Filter items using:
  - Toggles
  - Dropdown filter selector
  - Search terms
- Click on an item → Navigate to **Detail page**
- Navigate to other pages: Add, Stats, App Switcher

**Navigation From:**
- App Switcher (entry point)
- Other Collection App pages

**Navigation To:**
- Detail page (when clicking an item)
- Add page
- Stats page
- App Switcher

---

#### Page 2: Add
**Mockup File:** `collection_add.html`

**Purpose:** Add items to the collection by filling in all relevant information

**What it shows:**
- Form with all possible fields for item information:
  - Information about the item (model, brand, condition, etc.)
  - Photos
  - Notes
  - Other fields (see mockup for complete list)
- Form allows users to fill in/add information

**User Actions:**
- Fill in form fields with item information
- Add photos
- Add notes
- Fill in all relevant details
- Click "Add" button → Item is inserted into the collection
- Navigate back/cancel (if applicable)
- Navigate to other pages: Home, Stats, App Switcher

**Navigation From:**
- Home page
- Other Collection App pages

**Navigation To:**
- Home page (after adding item, or when canceling)
- Stats page
- App Switcher

---

#### Page 3: Detail
**Mockup File:** `collection_detail.html`

**Purpose:** Show detailed information about a specific item in the collection

**What it shows:**
- All fields/information entered for that item
- **Photo gallery** - Highlighted feature showing photos of the item
- Complete item details (model, brand, condition, notes, etc.)

**User Actions:**
- View all item details
- Browse photo gallery
- Edit item (if applicable)
- Delete item (if applicable)
- Navigate back to Home page
- Navigate to other pages: Add, Stats, App Switcher

**Navigation From:**
- Home page (when clicking a collection item)
- Other Collection App pages

**Navigation To:**
- Home page (back navigation, or after editing/deleting)
- Add page
- Stats page
- App Switcher

---

#### Page 4: Stats
**Mockup File:** `collection_stats.html`

**Purpose:** Show relevant and informative statistics about the collection

**What it shows:**
- Statistics about the collection, including:
  - Current total market value of the collection
  - Current total investment done
  - Share per brand
  - Types of items (cameras, lenses, other)
  - Timeline of market value and spent value
  - Distribution of manufacturing years
  - Other relevant statistics (see mockup)
- Visual representations of collection data (charts, graphs, etc.)

**User Actions:**
- View collection statistics
- Explore different statistics/metrics
- **Export items:**
  - Export whole collection OR
  - Export filtered selection (based on toggles, search, or filters)
  - Export includes: all fields and photos
  - Export format: CSV file (or another format to be defined during implementation)
- Navigate to other pages: Home, Add, Detail, App Switcher

**Navigation From:**
- Home page
- Other Collection App pages

**Navigation To:**
- Home page
- Add page
- Detail page (if stats are clickable/drill-down)
- App Switcher

---

### Cross-Page Features

**Navigation:**
- **Within Collection App:** Top menu bar with pages listed (centered)
  - Pages shown: Home, Add, Stats (and possibly Detail, or Detail accessed via Home)
  - Users click on page names to navigate between pages
  - Check mockups for exact navigation menu design
- **Between Apps (Collection ↔ Scraper):**
  - Click on main logo in topbar → Shows App Switcher
  - From App Switcher, user can select which app to use (Collection App or Scraper App)
- **General Navigation:**
  - Users can navigate between pages using the top menu
  - Users can return to App Switcher by clicking the logo in the topbar

**Notes:**
_(Additional observations or special considerations)_

#### Authentication flow

**Purpose:** Handle user account creation, sign in, email verification, and password reset processes.

---

### Authentication User Flows

#### Flow 1: New User Sign Up
**Goal:** Create a new user account and verify email address

**Steps:**
1. User visits shutterzilla.com → Lands on Landing Page
2. User clicks "Create Account" → Navigates to **Sign Up Page**
3. User fills in sign up form:
   - Email address
   - Password
   - Confirm password
   - Other required fields (if any)
4. User submits form
5. System creates account and sends email verification
6. User is redirected to **Email Verification Page** (or confirmation message)
7. User receives verification email with verification link
8. User clicks verification link in email → Email is verified
9. User can now sign in (redirected to Landing Page or Sign In)

**Pages Involved:**
- Landing Page
- Sign Up Page (auth_sign-up.html)
- Email Verification Page (auth_email-verification.html)

**Completion:** User account created and email verified → User can sign in

---

#### Flow 2: Existing User Sign In
**Goal:** Authenticate and log in existing user

**Steps:**
1. User visits shutterzilla.com → Lands on Landing Page
2. **If user is already logged in:** Automatically redirected to App Switcher
3. **If user is not logged in:** User sees login form on Landing Page
4. User enters credentials:
   - Email address
   - Password
5. User clicks "Sign In" / "Log In"
6. **On success:**
   - User is authenticated
   - User is redirected to **App Switcher**
   - User can now access Scraper App or Collection App
7. **On failure:**
   - Error message displayed
   - User can retry or use "Forgot Password" link

**Alternative: Social Login**
- User clicks social login button (if available)
- User completes social authentication (OAuth flow)
- On success: Redirected to App Switcher

**Pages Involved:**
- Landing Page (login form)
- App Switcher (on success)

**Completion:** User authenticated and logged in → Access to apps

---

#### Flow 3: Password Reset
**Goal:** Allow user to reset forgotten password

**Steps:**
1. User is on Landing Page (or Sign In page)
2. User clicks "Forgot Password" link → Navigates to **Forgot Password Page**
3. User enters email address
4. User submits form
5. System sends password reset email
6. User is redirected to **Password Reset Sent** confirmation page (or shown confirmation message)
7. User receives password reset email with reset link
8. User clicks reset link in email → Navigates to **Password Reset Page**
9. User enters new password and confirmation
10. User submits form
11. Password is updated
12. User is redirected to Landing Page / Sign In page
13. User can now sign in with new password

**Pages Involved:**
- Landing Page / Sign In Page
- Forgot Password Page (auth_forgot-password.html)
- Password Reset Sent Page (auth_password-reset-sent.html)
- Password Reset Page (auth_reset-password.html)

**Completion:** Password reset → User can sign in with new password

---

#### Flow 4: Email Verification (for new accounts)
**Goal:** Verify user's email address after account creation

**Steps:**
1. User completes sign up → Receives verification email
2. User clicks verification link in email
3. User is redirected to **Email Verification Page**
4. System verifies email address
5. **On success:**
   - Email is marked as verified
   - User sees success message
   - User can proceed to sign in
6. **On failure (link expired/invalid):**
   - User sees error message
   - Option to resend verification email

**Alternative Flow:**
- User is on Email Verification Page (after sign up)
- User can request resend of verification email
- User receives new verification email
- User clicks new link to verify

**Pages Involved:**
- Email Verification Page (auth_email-verification.html)
- Landing Page / Sign In (after verification)

**Completion:** Email verified → User account fully activated

---

### Authentication State Management

**Logged Out State:**
- User can access: Landing Page, Sign Up, Sign In, Forgot Password, Password Reset, Email Verification
- User cannot access: App Switcher, Scraper App, Collection App
- Attempting to access protected pages → Redirect to Landing Page

**Logged In State:**
- User can access: App Switcher, Scraper App, Collection App
- User cannot access: Sign Up, Sign In pages (redirected to App Switcher if attempted)
- Session persists until: User logs out, session expires, or user clears cookies

**Session Management:**
- User stays logged in across browser sessions (persistent session)
- User can log out via profile picture menu in topbar (when logged in)
- On logout: Session cleared, redirect to Landing Page

**Topbar Behavior:**
- **When user is logged in:** Profile picture is shown in topbar (no login/logout button)
  - Clicking profile picture shows menu with options:
    - **Normal users:** Profile, Logout
    - **Admin users:** Profile, Logout, Admin
  - Profile option: Navigate to Profile page (allows user to edit profile information - not yet mocked up)
- **When user is not logged in:** No profile picture shown
- **Access Control:** If any page is accessed while user is not logged in → User is redirected to Landing Page for login

---

### Notes:
- All authentication pages should be accessible when user is logged out
- Protected pages (apps) should redirect to Landing Page if user is not authenticated
- Email verification may be required before full access (implementation decision)
- Password requirements and validation rules to be defined during implementation
- Social login providers and implementation to be defined during implementation

#### Admin flow

**Purpose:** _[To be defined]_

**Access Control:**
- **Topbar Behavior:**
  - When user is logged in: Profile picture is shown (no login/logout button)
  - When user is not logged in: Redirect to Landing Page for any page access
- **Profile Picture Menu:**
  - **Normal users see:** Profile, Logout
  - **Admin users see:** Profile, Logout, Admin (link to admin area)
  - Profile page: Allows user to edit profile information (not yet mocked up)
- **Admin Access:**
  - User must be logged in AND have admin privileges
  - Entry point: User clicks on profile picture in topbar → Selects "Admin" from menu
  - User clicks "Admin" option → Navigate to Admin area

**Entry Point:**
- User with admin privileges clicks profile picture → Selects "Admin" from menu
- Landing on: **Dashboard** (admin_dashboard.html)

---

### Admin Pages

#### Page 1: Dashboard
**Mockup File:** `admin_dashboard.html`

**Purpose:** Show a selection of relevant information about the usage of shutterzilla.com

**What it shows:**
- Usage statistics and key metrics about Shutterzilla
- Priority: Usage stats (specific metrics to be determined)
- Dashboard will evolve based on adoption and needs
- See mockup for current design

**User Actions:**
- View usage statistics and metrics
- Navigate to other admin pages: Users, Scraper, Logs, Settings
- Navigate back to apps via profile picture menu

**Navigation From:**
- Profile picture menu → Admin option (entry point)
- Other admin pages

**Navigation To:**
- Users page
- Scraper page
- Logs page
- Settings page
- Back to apps (via profile picture menu)

---

#### Page 2: Users
**Mockup File:** `admin_users.html`

**Purpose:** Manage users - enable/disable users and change user types (user/admin)

**What it shows:**
- List of all users
- User information (email, name, status, type, etc.)
- User status (enabled/disabled)
- User type (user/admin)

**User Actions:**
- View list of all users
- **Enable/Disable users** - Toggle user account status
  - Disabled users cannot log in or access the platform
  - Enabled users can access the platform
- **Change user type** - Switch between "user" and "admin"
  - Users with "admin" type have access to admin area
  - Users with "user" type have normal access (no admin access)
- Navigate to other admin pages: Dashboard, Scraper, Logs, Settings
- Navigate back to apps via profile picture menu

**Navigation From:**
- Dashboard
- Other admin pages

**Navigation To:**
- Dashboard
- Scraper page
- Logs page
- Settings page
- Back to apps (via profile picture menu)

**Priority:** This page will be the first admin page to be usable/implemented

---

#### Page 3: Scraper
**Mockup File:** `admin_scraper.html`

**Purpose:** Configure scraper-related settings, starting with source enable/disable management

**What it shows:**
- List of scraping sources (e.g., Mercari Japan, Buyee, Yahoo Japan Auctions, eBay)
- Status of each source (enabled/disabled)

**User Actions:**
- View list of scraping sources
- **Enable/Disable sources** - Toggle whether each source is active for scraping
  - Enabled sources: Scraping is active for this source
  - Disabled sources: Scraping is inactive for this source
- Navigate to other admin pages: Dashboard, Users, Logs, Settings
- Navigate back to apps via profile picture menu

**Navigation From:**
- Dashboard
- Other admin pages

**Navigation To:**
- Dashboard
- Users page
- Logs page
- Settings page
- Back to apps (via profile picture menu)

**Note:** Starting with source enable/disable functionality; additional scraper configurations may be added later

---

#### Page 4: Logs
**Mockup File:** `admin_logs.html`

**Purpose:** View system logs and activity logs for monitoring and debugging

**What it shows:**
- List of log entries
- Log entries include: timestamp, log type, message/details, severity level (if applicable)
- **Suggested minimal log types:**
  1. **User Activity** - User logins, signups, account changes
  2. **Scraping Activity** - Scraping runs, scraping errors, source status changes
  3. **System/Errors** - Application errors, warnings, system issues
  4. **Admin Actions** - Changes made by admin users (user management, settings changes)

**User Actions:**
- View log entries
- **Filter logs by type:**
  - Select log type from filter dropdown/selector (User Activity, Scraping Activity, System/Errors, Admin Actions)
  - Filter by date range (if applicable)
  - Filter by severity level (if applicable)
- Search logs (if applicable)
- Navigate to other admin pages: Dashboard, Users, Scraper, Settings
- Navigate back to apps via profile picture menu

**Navigation From:**
- Dashboard
- Other admin pages

**Navigation To:**
- Dashboard
- Users page
- Scraper page
- Settings page
- Back to apps (via profile picture menu)

**Note:** Log types and filtering options to be refined during implementation based on monitoring needs

---

#### Page 5: Settings
**Mockup File:** `admin_settings.html`

**Purpose:** Manage platform-wide settings and configurations

**What it shows:**
- Settings form/sections with configurable options
- **Suggested minimal settings categories:**
  1. **General Settings**
     - Site name/branding
     - Maintenance mode (enable/disable access)
  2. **Email/SMTP Settings**
     - SMTP server configuration (for sending emails: verification, password reset, etc.)
     - Email sender address
  3. **Security Settings**
     - Password requirements (minimum length, complexity rules)
     - Session timeout duration
  4. **Feature Flags** (optional)
     - Enable/disable specific features (if needed)

**User Actions:**
- View current settings
- Edit/update settings values
- Save settings changes
- Navigate to other admin pages: Dashboard, Users, Scraper, Logs
- Navigate back to apps via profile picture menu

**Navigation From:**
- Dashboard
- Other admin pages

**Navigation To:**
- Dashboard
- Users page
- Scraper page
- Logs page
- Back to apps (via profile picture menu)

**Note:** Settings categories and options to be refined during implementation based on platform needs

---

### Cross-Page Features

**Navigation:**
- **Within Admin Area:** Top menu bar with pages listed (centered)
  - Pages shown: Dashboard, Users, Scraper, Logs, Settings
  - Users click on page names to navigate between admin pages
  - Check mockups for exact navigation menu design
- **Back to Apps:**
  - Click on main logo in topbar → Shows App Switcher
  - From App Switcher, user can select which app to use (Scraper App or Collection App)
- **Access Control:**
  - Only users with admin privileges can access admin pages
  - Non-admin users attempting to access admin pages → Redirect appropriately

**Notes:**
_(Additional observations or special considerations)_

---

### Define Core Features

#### Scraper App features

Based on the Scraper App user journey documentation, here are the core features:

**1. Discovery & Browsing**
- Browse personalized feed of camera listings from multiple sources (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- View listings automatically matched from saved searches
- View listings from automated scrapes

**2. Search Functionality**
- Perform searches on source websites to find camera listings
- View search results with filtering and sorting options
- Save search criteria for later use

**3. Saved Searches Management**
- Create and save search criteria
- Activate/deactivate saved searches
- Active saved searches automatically add matching listings to Feed
- Edit and delete saved searches
- View saved search status and criteria

**4. Watch List**
- Mark listings to watch/follow
- View all watched listings on dedicated Watch page
- Watched listings persist even if they become sold/unavailable on source websites
- Remove listings from watch list

**5. Listing Management**
- View detailed listing information (title, price, images, condition, source, seller info)
- Mark listings as dismissed (hide from Feed and search results)
- View original listing on source website
- Share listings

**6. Integration with Collection App**
- Add listings to Collection App from Detail page

**7. Sorting & Filtering**
- Sort listings by various criteria (Most recent, Price, etc.)
- Invert sort order (ascending/descending)
- Filter out dismissed listings from Feed and search results

**8. Multi-Source Aggregation**
- Aggregate listings from multiple sources (Mercari Japan, Buyee, Yahoo Japan Auctions, eBay)
- Display unified listing information across sources

#### Collection App features

Based on the Collection App user journey documentation, here are the core features:

**1. Collection Management**
- Store and display information about cameras, lenses, and other photography-related items (flashes, lightmeters, caps, etc.)
- Add items to collection via form with all relevant fields (information, photos, notes, etc.)
- View all collection items on Home page

**2. Item Details & Photo Gallery**
- View detailed information about each item in the collection
- Display all fields entered for each item
- Photo gallery feature - highlight photos of items

**3. Search & Filtering**
- Filter collection items using toggles, dropdown filter selectors, and search terms
- View filtered/sorted collection listings

**4. Statistics & Analytics**
- View comprehensive statistics about the collection:
  - Current total market value of the collection
  - Current total investment done
  - Share per brand
  - Types of items (cameras, lenses, other)
  - Timeline of market value and spent value
  - Distribution of manufacturing years
  - Other relevant statistics

**5. Export Functionality**
- Export collection items (whole collection or filtered selection)
- Export includes all fields and photos
- Export format: CSV file (or another format to be defined during implementation)
- Export filtered selections based on toggles, search, or filters

**6. Item Organization**
- Organize items by type (cameras, lenses, other photography items)
- Track detailed information for each item (model, brand, condition, purchase info, photos, notes, etc.)

#### Data storage requirements

Based on the documented features and user journeys, here are the core data storage requirements:

**1. User Accounts & Authentication**
- User profiles (email, password hash, profile information)
- User types (user, admin)
- User status (enabled/disabled)
- Email verification status
- Session data
- Authentication tokens (if using token-based auth)

**2. Scraper App Data**

**2.1. Listings (from source websites)**
- Listing ID (unique identifier)
- Source website (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- Source listing URL
- Listing type (fixed price, auction)
- Title
- Price (fixed price listings) OR
  - Current price (auctions)
  - Buyout price (auctions, if available)
  - Auction end time/date (auctions)
- Images/photo URLs
- Condition
- Warning keywords (junk, repair) - Important for Japanese sites, especially Buyee
- Seller information (if available)
- Listing status (available, sold, unavailable, ended)
- Scraped timestamp
- Last updated timestamp

**Notes:**
- Auction-specific fields (current price, buyout price, auction end) to be included if scrapable from source websites.
- Warning keywords (junk, repair) should be tracked for Japanese sites, especially Buyee, as these indicate item condition issues.

**2.2. Saved Searches**
- Search ID (unique identifier)
- User ID (owner of the search)
- Search name
- Search criteria (keywords, filters, etc.)
- Sources included (Mercari, Buyee, Yahoo Japan Auctions, eBay) - which sources to search
- Search status (active/inactive) - toggle on/off
- Created timestamp
- Last executed timestamp

**2.3. User Watch List**
- Watch entry ID
- User ID
- Listing ID (reference to listing)
- Source (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- Watched timestamp
- Listing snapshot data (to preserve data even if listing becomes unavailable)

**2.4. Dismissed Listings**
- Dismissed entry ID
- User ID
- Listing ID (reference to listing)
- Source (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- Dismissed timestamp
- Listing snapshot data (for cleanup verification)

**2.5. Feed Entries**
- Feed entry ID
- User ID
- Listing ID (reference to listing)
- Source (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- Entry source type (saved search match, automated scrape, etc.)
- Added to feed timestamp

**3. Collection App Data**

**3.1. Collection Items**

**Item Types:** Cameras, Lenses, Other (flashes, lightmeters, caps, filters, cases, straps, etc.)

**Common Fields (All Types):**
- Item ID (unique identifier)
- User ID (owner)
- Item type (camera, lens, other)
- Created timestamp
- Last updated timestamp

**3.1.1. Camera Items**

**Basic Identification:**
- Brand
- Model
- Variant/Type/Version
- Serial Number
- Manufacturing Year

**Technical Specifications:**
- Film Format
- Lens Mount Type
- Shutter Type
- Shutter Speed Range
- ISO/ASA Range
- Metering System
- Viewfinder Type
- Flash Sync Type
- Battery Type

**Physical Details:**
- Body Color/Finish
- Body Material
- Weight
- Dimensions (optional)
- Condition Rating
- Condition Notes

**Acquisition Information:**
- Purchase Date
- Purchase Price (USD - stored)
- Purchase Freight from Seller to Storage (USD - stored)
- Purchase Storage Fee (USD - stored)
- Purchase Freight from Storage (USD - stored)
- Exchange Rate (from purchase date - for USD to BRL conversion)
- Purchase Source
- Purchase URL
- Purchase Country
- Purchase Address
- Purchase Condition
- Purchase Notes

**Valuation:**
- Current Market Value (USD - stored, converted to BRL for display using purchase date exchange rate)
- Value Date (when value was assessed)
- Total Investment/Spent Value (USD - sum of purchase components, converted to BRL for display)

**Additional Information:**
- Photos/Images
- Notes/Description
- Included Accessories
- Service/Repair History (multiple entries - each entry: date, type, description, cost, provider, etc.)
- Special Features/Modifications
- Reference URLs (variable amount - multiple URLs)

**3.1.2. Lens Items**

**Basic Identification:**
- Brand
- Model/Lens Name
- Variant/Version/Series
- Serial Number
- Manufacturing Year

**Technical Specifications:**
- Focal Length
- Maximum Aperture
- Minimum Aperture
- Lens Type (Prime, Zoom, Macro, etc.)
- Mount Type
- Format Coverage
- Angle of View
- Optical Formula (elements/groups)
- Filter Thread Size
- Minimum Focus Distance
- Image Stabilization
- Auto Focus
- Aperture Blades

**Physical Details:**
- Body Color/Finish
- Body Material
- Weight
- Dimensions (length, diameter)
- Condition Rating
- Condition Notes
- Lens Cap Included
- Lens Hood Included
- Front/Back Cap Condition

**Acquisition Information:**
- Purchase Date
- Purchase Price (USD - stored)
- Purchase Freight from Seller to Storage (USD - stored)
- Purchase Storage Fee (USD - stored)
- Purchase Freight from Storage (USD - stored)
- Exchange Rate (from purchase date - for USD to BRL conversion)
- Purchase Source
- Purchase URL
- Purchase Country
- Purchase Address
- Purchase Condition
- Purchase Notes

**Valuation:**
- Current Market Value (USD - stored, converted to BRL for display using purchase date exchange rate)
- Value Date (when value was assessed)
- Total Investment/Spent Value (USD - sum of purchase components, converted to BRL for display)

**Additional Information:**
- Photos/Images
- Notes/Description
- Included Accessories
- Service/Repair History (multiple entries - each entry: date, type, description, cost, provider, etc.)
- Special Features/Modifications
- Compatibility Notes
- Reference URLs (variable amount - multiple URLs)

**3.1.3. Other Items**

**Basic Identification:**
- Item Type/Category (Flash, Lightmeter, Cap, Filter, Case, Strap, Battery, Cable, etc.)
- Brand
- Model/Name
- Variant/Version
- Serial Number (if applicable)
- Manufacturing Year (if known)

**Physical Details:**
- Condition Rating
- Condition Notes
- Weight (if applicable)
- Dimensions (if applicable)
- Color/Finish

**Acquisition Information:**
- Purchase Date
- Purchase Price (USD - stored)
- Purchase Freight from Seller to Storage (USD - stored)
- Purchase Storage Fee (USD - stored)
- Purchase Freight from Storage (USD - stored)
- Exchange Rate (from purchase date - for USD to BRL conversion)
- Purchase Source
- Purchase URL
- Purchase Country
- Purchase Address
- Purchase Condition
- Purchase Notes

**Valuation:**
- Current Market Value (USD - stored, converted to BRL for display using purchase date exchange rate)
- Value Date (when value was assessed)
- Total Investment/Spent Value (USD - sum of purchase components, converted to BRL for display)

**Additional Information:**
- Photos/Images
- Description/Notes (for item-specific details, specifications, features, compatibility, etc.)
- Reference URLs (variable amount - multiple URLs)
- Included Items/Accessories
- Service/Repair History (multiple entries - each entry: date, type, description, cost, provider, etc.)
- Compatibility/Use Notes

**Notes:**
- Valuation System: All values stored in USD, converted to BRL for display using exchange rate from purchase date. Cameras/lenses are always valuated in Brazil context.
- Detail Page: Items have simplified view (subset of fields) and expanded view (all fields) - user can toggle between views.
- Service/Repair History: Multiple entries supported (separate data structure needed).
- Field Management: Item field definitions (for Cameras, Lenses, Other) are code-based - fields are defined in source code and changed by editing code (no admin UI for field management needed).

**4. Admin Data**

**4.1. Admin Settings**
- Settings key
- Settings value
- Settings category (general, email/SMTP, security, feature flags)
- Last updated timestamp

**4.2. Source Configuration**
- Source ID (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- Source status (enabled/disabled)
- Source configuration data
- Last updated timestamp

**4.3. System Logs**
- Log ID
- Log type (User Activity, Scraping Activity, System/Errors, Admin Actions)
- Timestamp
- Log message/details
- Severity level (if applicable)
- Related user ID (if applicable)
- Related entity ID (if applicable)

**5. Statistics & Analytics Data**

**5.1. Collection Statistics (calculated/aggregated)**
- User ID
- Statistics type (total market value, total investment, brand distribution, etc.)
- Calculated values
- Calculation timestamp

**Note:** Some statistics may be calculated on-the-fly rather than stored, depending on implementation approach.

**6. Integration Data**

**6.1. Scraper to Collection Links**
- Link ID
- User ID
- Listing ID (from Scraper App)
- Collection Item ID (from Collection App)
- Created timestamp

**Key Relationships:**
- Users → Saved Searches (one-to-many)
- Users → Watch List (one-to-many)
- Users → Dismissed Listings (one-to-many)
- Users → Collection Items (one-to-many)
- Users → Feed Entries (one-to-many)
- Listings → Watch List (one-to-many, via users)
- Listings → Dismissed Listings (one-to-many, via users)
- Saved Searches → Feed Entries (one-to-many, via matches)

#### Key interactions

Based on the documented user journeys and features, here are the key interactions across the platform:

**Scraper App Interactions:**

1. **Browse & Discover**
   - Browse personalized Feed of listings
   - View listings from multiple sources (Mercari, Buyee, Yahoo Japan Auctions, eBay)
   - Sort listings (Most recent, Price, etc. - ascending/descending)
   - Filter listings (dismissed listings are automatically hidden)

2. **Search**
   - Perform searches with criteria
   - View search results
   - Save search criteria for later use

3. **Listing Actions**
   - **Mark as Watch** - Add listing to watch list (available from Feed, Search, Saved Search, Detail pages)
   - **Mark as Dismissed** - Hide listing from Feed and search results (available from any page showing listings)
   - View listing details (click on listing)
   - View original listing on source website (external link)
   - Share listing
   - Add listing to Collection App

4. **Saved Searches Management**
   - Create saved searches
   - Activate/deactivate saved searches (toggle on/off)
   - Edit saved searches
   - Delete saved searches
   - View saved search status and criteria

5. **Watch List Management**
   - View all watched listings
   - Remove listings from watch list

**Collection App Interactions:**

1. **Collection Management**
   - Add items to collection (Cameras, Lenses, Other items)
   - View collection items (Home page listing)
   - Filter collection items (toggles, dropdown, search terms)
   - View item details (simplified view / expanded view toggle)

2. **Item Actions**
   - Edit item information
   - Delete items
   - Browse photo gallery
   - Add service/repair history entries

3. **Statistics & Export**
   - View collection statistics (market value, investment, brand distribution, timelines, etc.)
   - Export collection (whole collection or filtered selection)
   - Export includes all fields and photos

**Authentication Interactions:**

1. **Account Management**
   - Sign up (create account)
   - Sign in (log in)
   - Sign out (logout)
   - Reset password (forgot password flow)
   - Verify email address

2. **Profile**
   - Access profile via profile picture menu
   - Edit profile information (Profile page - not yet mocked up)

**Navigation Interactions:**

1. **Page Navigation**
   - Navigate between pages using top menu bar
   - Click logo to access App Switcher
   - Profile picture menu (Profile, Logout, Admin if admin user)

2. **App Switching**
   - Switch between Scraper App and Collection App via App Switcher
   - Access App Switcher by clicking main logo

**Admin Interactions (Admin users only):**

1. **User Management**
   - View list of users
   - Enable/disable users
   - Change user type (user/admin)

2. **Scraper Configuration**
   - Enable/disable scraping sources
   - View source configuration

3. **System Management**
   - View system logs (filter by type: User Activity, Scraping Activity, System/Errors, Admin Actions)
   - Manage settings (General, Email/SMTP, Security, Feature Flags)
   - View dashboard statistics

**Cross-App Interactions:**

1. **Scraper → Collection**
   - Add listing to Collection App from Scraper App Detail page

2. **Data Flow**
   - Saved searches (when active) automatically populate Feed
   - Automated scrapes populate Feed
   - Watch list persists listings even when unavailable on source websites

---

### Define Basic Data Requirements

**Note:** Detailed data requirements are documented in the "Data Storage Requirements" section above. This section provides a high-level summary.

#### Camera listings fields

Camera listings (scraped from source websites) require the following fields:
- Basic identification: Listing ID, Source, Source URL, Title
- Listing type: Fixed price or Auction
- Price information: Price (fixed) OR Current price, Buyout price, Auction end time (auctions)
- Images: Photo URLs
- Condition and warnings: Condition, Warning keywords (junk, repair)
- Seller information
- Listing status and metadata: Status, Scraped timestamp, Last updated timestamp

**Detailed field list:** See "2.1. Listings (from source websites)" in Data Storage Requirements section.

#### Saved searches fields

Saved searches require the following fields:
- Search identification: Search ID, User ID, Search name
- Search criteria: Search criteria (keywords, filters, etc.)
- Source selection: Sources included (Mercari, Buyee, Yahoo Japan Auctions, eBay)
- Status: Search status (active/inactive - toggle on/off)
- Timestamps: Created timestamp, Last executed timestamp

**Detailed field list:** See "2.2. Saved Searches" in Data Storage Requirements section.

#### Collection cameras fields

Collection items are organized into three types: Cameras, Lenses, and Other items. Each type has specific fields.

**Cameras** require fields for:
- Basic identification (Brand, Model, Variant, Serial Number, Manufacturing Year)
- Technical specifications (Film Format, Lens Mount, Shutter Type, etc.)
- Physical details (Body Color, Material, Weight, Condition, etc.)
- Acquisition information (Purchase Date, Purchase Price, Freight costs, Storage Fee, Exchange Rate, Purchase Source, URL, Country, Address, Notes)
- Valuation (Current Market Value in USD, Value Date, Total Investment in USD - converted to BRL for display)
- Additional information (Photos, Notes, Accessories, Service/Repair History, Reference URLs)

**Lenses** require similar structure with lens-specific technical specifications (Focal Length, Aperture, Lens Type, Mount Type, etc.).

**Other items** use a more flexible structure with Type/Category and Description/Notes fields for item-specific details.

**Detailed field lists:** See "3.1. Collection Items" in Data Storage Requirements section (3.1.1 Cameras, 3.1.2 Lenses, 3.1.3 Other Items).

#### Data relationships

Key relationships between data entities:

**User-Centric Relationships (One-to-Many):**
- Users → Saved Searches
- Users → Watch List entries
- Users → Dismissed Listings
- Users → Collection Items
- Users → Feed Entries

**Listing-Centric Relationships:**
- Listings → Watch List entries (via users)
- Listings → Dismissed Listings (via users)
- Listings → Feed Entries (via users)

**Search-Centric Relationships:**
- Saved Searches → Feed Entries (via matches)

**Collection Relationships:**
- Collection Items → Service/Repair History entries (one-to-many)
- Users → Collection Items (one-to-many)

**Integration Relationships:**
- Listings → Collection Items (via Scraper to Collection links)

**Detailed relationships:** See "Key Relationships" section in Data Storage Requirements.

---

## Phase 0.2: Scraping Feasibility Validation

**Status:** Not Started

### 0.2.1 Mercari Japan Scraping Test

**Date Tested:** 2026-01-13  
**Tester:** Validation Script

**Results:**
- Access: ✅ PASS (with improved headers)
- Search: ✅ PASS (can access search pages with improved headers)
- Data Extraction: ✅ PASS (with Playwright - JavaScript rendering required)
- Rate Limiting: ✅ PASS (no issues with reasonable delays)
- JavaScript Required: **Yes** (REQUIRED - Next.js/React application)
- Anti-Bot Measures: ⚠️ Moderate (403 errors with basic headers, but works with improved headers)

**Challenges Encountered:**
1. **JavaScript Rendering Required:** Mercari uses Next.js/React framework. Listings are loaded client-side via JavaScript/API calls after page load. The initial HTML contains only page structure, not listing data.
2. **Anti-Bot Protection:** Basic HTTP requests get 403 Forbidden. Solution: Improved headers (realistic User-Agent, Accept headers, Referer, etc.) and session management allow access.
3. **Dynamic Content:** Listings are not in the initial HTML - they're loaded via API calls after JavaScript execution.

**Solutions Found:**
1. **Improved Headers:** Using realistic browser headers (updated User-Agent, Accept headers, Referer, Sec-Fetch headers) allows access to search pages.
2. **Session Management:** Using requests.Session() to maintain cookies helps with access.
3. **JavaScript Rendering Needed:** Playwright or Selenium is REQUIRED to:
   - Execute JavaScript on the page
   - Wait for listings to load
   - Extract listing data from the rendered DOM

**Sample Data Extracted:**
```json
{
  "title": "Nikon FM2",
  "price": "BRL1,329.22",
  "image_url": "https://static.mercdn.net/thumb/item/webp/m26068059510_1.jpg",
  "listing_url": "https://jp.mercari.com/en/item/m26068059510",
  "all_images": [
    "https://static.mercdn.net/item/detail/orig/photos/m26068059510_1.jpg",
    "https://static.mercdn.net/item/detail/orig/photos/m26068059510_2.jpg",
    "..."
  ]
}
```

**Note:** Data extraction successfully works with Playwright. The initial HTTP-only test failed because listings are loaded via JavaScript, but Playwright successfully extracts all required fields (titles, prices, URLs, images).

**Technical Details:**
- Search URL format: `https://www.mercari.com/jp/search/?keyword={search_term}`
- HTML structure: Next.js/React application
- Listings loaded via: Client-side JavaScript/API calls
- HTML contains: Page structure, but listings are loaded dynamically

**Recommendation:** ✅ **Proceed** - Feasible with Playwright for JavaScript rendering

**Implementation Notes:**
- ✅ Cannot use simple HTTP requests + BeautifulSoup (listings loaded client-side)
- ✅ Must use browser automation (Playwright recommended) - **TESTED AND WORKING**
- ✅ Playwright successfully extracts listing data:
  - Titles: ✅ Working (e.g., "ニコン Nikon New FM2 シルバー")
  - Prices: ✅ Working (e.g., "BRL1,329.22")
  - URLs: ✅ Working (e.g., "/item/m26068059510")
  - Images: ⚠️ Needs refinement (structure identified)
- ✅ Need to wait for listings to load after page navigation (5+ seconds recommended)
- ✅ Improved headers help avoid 403 errors
- ✅ Rate limiting appears reasonable with delays between requests

**Test Results (Playwright):**
- Access Test: ✅ PASS
- Search Test: ✅ PASS  
- Extraction Test: ❌ **FAIL** - Virtual Scrolling Limitation
- Listings Found: Only 12 items extracted (expected: 101 items)
- Root Cause: **Virtual Scrolling** - Only ~10-15 items exist in DOM at any time, even though 101 are visually rendered

**Critical Issue - Virtual Scrolling:**
- **Problem:** Mercari uses aggressive virtual scrolling. Only items currently in viewport (or slightly outside) exist in the DOM.
- **Evidence:** HTML snapshot shows only 9 `merListItem-container` elements and 11 item links, despite 101 items being visually present in a 20×5+1 grid layout.
- **Impact:** Traditional DOM-based extraction fails because items are dynamically added/removed as user scrolls.
- **Attempted Solutions:**
  1. ❌ Aggressive scrolling (600+ scrolls with waits) - Only found 12 items
  2. ❌ Collecting items during scroll - Still only found 12 items
  3. ⏳ API response interception - In progress (may contain all 101 items)
  4. ⏳ __NEXT_DATA__ extraction - In progress (React state may contain all items)

**Current Status:** ❌ **FAIL** - Cannot reliably extract all 101 items using DOM-based methods

**Next Steps:**
1. ✅ Implement Playwright-based scraper - **COMPLETED**
2. ✅ Wait for listings to load - **WORKING**
3. ❌ Extract listing data from rendered DOM - **FAILING due to virtual scrolling**
4. ⏳ **PRIORITY:** Extract items from API response (`api.mercari.jp/v2/entities:search`) - May contain all 101 items
5. ⏳ **PRIORITY:** Extract items from `__NEXT_DATA__` script tag - React state may contain all items
6. ⚠️ **Alternative:** Accept limitation and extract only visible items (~10-15 per page load)
7. ⚠️ **Alternative:** Implement pagination/scroll-based collection (slow but may work)

---

### 0.2.2 Buyee Scraping Test

**Date Tested:** _TBD_  
**Tester:** _TBD_

**Results:**
_(Same structure as Mercari)_

**Challenges Encountered:**
_(To be filled)_

**Solutions Found:**
_(To be filled)_

**Sample Data Extracted:**
_(To be filled)_

**Recommendation:** _TBD_

**Notes:**
_(To be filled)_

---

### 0.2.3 Yahoo Japan Auctions Scraping Test

**Date Tested:** _TBD_  
**Tester:** _TBD_

**Results:**
_(Same structure as Mercari)_

**Challenges Encountered:**
_(To be filled)_

**Solutions Found:**
_(To be filled)_

**Sample Data Extracted:**
_(To be filled)_

**Recommendation:** _TBD_

**Notes:**
_(To be filled)_

---

### 0.2.4 eBay USA Scraping Test

**Date Tested:** _TBD_  
**Tester:** _TBD_

**Results:**
_(Same structure as Mercari)_

**API vs Scraping Analysis:**
- eBay API Available: Yes / No
- API Limitations: _TBD_
- Scraping Challenges: _TBD_
- Recommendation: Use API / Use Scraping / Hybrid

**Challenges Encountered:**
_(To be filled)_

**Solutions Found:**
_(To be filled)_

**Sample Data Extracted:**
_(To be filled)_

**Recommendation:** _TBD_

**Notes:**
_(To be filled)_

---

## Phase 0.3: Validation Results & Decision

**Date:** _TBD_

### Overall Assessment

**Summary:**
_(Overall assessment of scraping feasibility)_

**Key Findings:**
1. _TBD_
2. _TBD_
3. _TBD_

**Decision:**
- [ ] Proceed with full implementation
- [ ] Proceed with adjustments (document in plan)
- [ ] Reassess approach
- [ ] Pause project

**Rationale:**
_(Why we made this decision)_

**Next Steps:**
_(What we'll do based on validation results)_

---

## General Validation Learnings

_(Space for cross-source learnings, common challenges, and insights)_
