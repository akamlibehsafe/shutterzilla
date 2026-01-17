# Detailed Specifications Breakdown

This document provides a detailed breakdown of all specification tasks needed in Phase 0.3 before beginning implementation.

**Purpose:** To ensure all UI, behavior, and architecture details are fully specified before writing code.

**Status:** Planning Phase

---

## Phase 0.3.1: UI Component Definitions

### Current State
- ✅ Basic component library exists (`docs/specification/design/component-library.md`)
- ✅ Design system defined (`docs/specification/design/design-system.md`)
- ⚠️ Missing: Detailed interaction patterns, states, responsive behaviors

### Tasks to Complete

#### 1. Component Library Completion
- [ ] **Review existing components**
  - [ ] Top Bar (navigation, logo, profile menu)
  - [ ] Footer
  - [ ] Cards (listing cards, collection cards)
  - [ ] Buttons (primary, secondary, icon buttons)
  - [ ] Forms (inputs, selects, checkboxes, radio buttons)
  - [ ] Tabs
  - [ ] View toggles (grid/list)
  - [ ] Modals/Dialogs
  - [ ] Badges (source badges, status badges)
  - [ ] Loading states
  - [ ] Empty states
  - [ ] Error states

- [ ] **Define missing components**
  - [ ] Search bar component
  - [ ] Filter components
  - [ ] Sort dropdown
  - [ ] Pagination component
  - [ ] Image gallery component
  - [ ] Statistics/chart components
  - [ ] Notification components
  - [ ] Toast messages
  - [ ] Tooltips
  - [ ] Dropdown menus
  - [ ] Mobile menu/hamburger menu

#### 2. Interaction Patterns
- [ ] **Define hover states** for all interactive elements
- [ ] **Define focus states** for accessibility
- [ ] **Define active/pressed states** for buttons
- [ ] **Define disabled states** for form elements
- [ ] **Define loading states** (skeletons, spinners, progress)
- [ ] **Define error states** (validation errors, API errors)
- [ ] **Define empty states** (no results, no data)
- [ ] **Define transition animations** (page transitions, component animations)

#### 3. Responsive Design Specifications
- [ ] **Define breakpoints**
  - [ ] Mobile (< 640px)
  - [ ] Tablet (640px - 1024px)
  - [ ] Desktop (> 1024px)
- [ ] **Define responsive behaviors** for each component
  - [ ] Top bar (mobile menu, desktop menu)
  - [ ] Cards (grid vs list, columns)
  - [ ] Forms (full width, stacked)
  - [ ] Navigation (tabs, mobile drawer)
- [ ] **Define touch interactions** (mobile gestures, swipe actions)

#### 4. Accessibility Requirements
- [ ] **Keyboard navigation** (tab order, shortcuts)
- [ ] **Screen reader support** (ARIA labels, roles)
- [ ] **Color contrast** (verify WCAG compliance)
- [ ] **Focus indicators** (visible focus states)
- [ ] **Form validation** (error messages, required fields)

#### 5. Component States Documentation
- [ ] **Loading states** - How each component shows loading
- [ ] **Error states** - How errors are displayed
- [ ] **Empty states** - What shows when no data
- [ ] **Success states** - Confirmation messages
- [ ] **Disabled states** - When and how components are disabled

**Deliverable:** Complete component library with all states, interactions, and responsive behaviors documented.

---

## Phase 0.3.2: Complete Scraper Behavior Specification

### Current State
- ✅ Basic scraper behavior questions outlined (`implementation-scraper-behavior-specification.md`)
- ✅ Buyee scraper validated (feasible with Playwright)
- ⚠️ Missing: Complete behavior specification

### Tasks to Complete

#### 1. General Behavior
- [ ] **Scraping frequency**
  - [ ] How often does scraper run? (every 4 hours)
  - [ ] Can frequency be configured?
  - [ ] Different frequencies per source?
- [ ] **Failure handling**
  - [ ] What happens if a scraper run fails?
  - [ ] Retry logic (how many retries, backoff strategy)
  - [ ] Notification on persistent failures
- [ ] **Rate limiting**
  - [ ] How to handle rate limits from sources?
  - [ ] Delays between requests
  - [ ] Exponential backoff strategy
- [ ] **Source changes**
  - [ ] How to detect HTML structure changes?
  - [ ] Alerting when scraping fails due to structure changes
  - [ ] Version tracking for selectors

#### 2. Data Collection
- [ ] **Data fields to collect** (per source)
  - [ ] Required fields (title, price, URL, images)
  - [ ] Optional fields (condition, seller, description)
  - [ ] Source-specific fields (bids, closing time for auctions)
- [ ] **Data normalization**
  - [ ] How to normalize prices (currency conversion, format)
  - [ ] How to normalize conditions (excellent, good, fair, poor)
  - [ ] How to normalize dates/timestamps
  - [ ] How to handle missing fields
- [ ] **Data updates**
  - [ ] How to detect price changes?
  - [ ] How to detect status changes (available → sold)?
  - [ ] Update frequency for existing listings
  - [ ] Historical data tracking (price history)

#### 3. Deduplication Strategy
- [ ] **Duplicate identification**
  - [ ] How to identify same listing across sources?
  - [ ] Matching criteria (URL, title similarity, image similarity)
  - [ ] Confidence thresholds for matching
- [ ] **Duplicate handling**
  - [ ] Store as separate records or merge?
  - [ ] How to display duplicates in UI?
  - [ ] Link duplicates together in database

#### 4. Status Tracking
- [ ] **Listing statuses**
  - [ ] Active (available)
  - [ ] Sold
  - [ ] Expired (auction ended)
  - [ ] Removed (listing deleted)
- [ ] **Status detection**
  - [ ] How to detect status changes?
  - [ ] How often to check status?
  - [ ] How long to keep inactive listings?
- [ ] **Status updates**
  - [ ] Automatic status updates
  - [ ] Manual status updates (admin)
  - [ ] Status change notifications

#### 5. Error Handling
- [ ] **Source downtime**
  - [ ] How to handle when source is down?
  - [ ] Retry strategy
  - [ ] Notification to admin
- [ ] **HTML structure changes**
  - [ ] Detection mechanism
  - [ ] Alerting
  - [ ] Recovery process
- [ ] **Logging**
  - [ ] What to log (errors, warnings, info)
  - [ ] Log format and structure
  - [ ] Log retention
- [ ] **Notifications**
  - [ ] Who gets notified on errors?
  - [ ] Notification channels (email, admin dashboard)
  - [ ] Error severity levels

#### 6. Performance
- [ ] **Scraping limits**
  - [ ] How many listings per run?
  - [ ] How many listings per source?
  - [ ] Time limits per run
- [ ] **Database optimization**
  - [ ] Batch inserts vs individual inserts
  - [ ] Indexing strategy
  - [ ] Query optimization
- [ ] **Resource usage**
  - [ ] Memory limits
  - [ ] CPU usage
  - [ ] Network bandwidth

#### 7. Integration
- [ ] **Database connection**
  - [ ] Connection pooling
  - [ ] Transaction handling
  - [ ] Error recovery
- [ ] **Saved search matching**
  - [ ] When to run matching (during scrape, after scrape)
  - [ ] Matching algorithm
  - [ ] Performance optimization
- [ ] **User notifications**
  - [ ] How to notify users of new matches?
  - [ ] Notification frequency (immediate, batched, daily digest)
  - [ ] Notification channels (email, in-app)

#### 8. Source-Specific Behaviors

**Buyee:**
- [ ] Scraping approach (Playwright confirmed)
- [ ] Fields available (title, price, images, description, condition, bids, closing time)
- [ ] Rate limits (tested, no issues with delays)
- [ ] Pagination handling
- [ ] Iframe content handling
- [ ] Translation handling

**eBay:**
- [ ] Scraping approach (API vs HTML scraping)
- [ ] API evaluation (if using API: rate limits, costs, fields)
- [ ] Fields available
- [ ] Rate limits
- [ ] Pagination handling
- [ ] Auction vs fixed price handling

**Deliverable:** Complete scraper behavior specification document with all decisions documented.

---

## Phase 0.3.3: Detailed Page Behavior Specifications

### Current State
- ✅ High-level user journeys documented (`implementation-validation-notes.md`)
- ✅ Screen specifications document exists (`implementation-screen-specifications.md`)
- ⚠️ Missing: Detailed behavior for each page

### Tasks to Complete

#### Scraper App Pages

**1. Feed Page**
- [ ] **Data loading**
  - [ ] How are listings loaded? (paginated, infinite scroll, all at once)
  - [ ] Initial load (how many listings?)
  - [ ] Refresh strategy (auto-refresh, manual refresh)
- [ ] **Filtering**
  - [ ] Available filters (source, price range, condition, date range)
  - [ ] Filter persistence (save in URL, localStorage)
  - [ ] Filter combinations (AND/OR logic)
- [ ] **Sorting**
  - [ ] Sort options (date, price, relevance)
  - [ ] Sort direction (ascending/descending)
  - [ ] Default sort
  - [ ] Sort persistence
- [ ] **View modes**
  - [ ] Grid view behavior
  - [ ] List view behavior
  - [ ] View toggle persistence
- [ ] **Interactions**
  - [ ] Click on listing → Detail page
  - [ ] Mark as watch → Add to watch list
  - [ ] Mark as dismissed → Hide from feed
  - [ ] Save search → Create saved search
- [ ] **Empty states**
  - [ ] No listings found
  - ] No saved searches active
- [ ] **Loading states**
  - [ ] Initial load
  - [ ] Loading more (pagination/infinite scroll)
  - [ ] Refreshing

**2. Search Page**
- [ ] **Search functionality**
  - [ ] Search fields (keywords, filters)
  - [ ] Search type (full-text, exact match, fuzzy)
  - [ ] Search scope (all sources, specific sources)
- [ ] **Search execution**
  - [ ] Real-time search vs button-triggered
  - [ ] Debouncing for real-time search
  - [ ] Search history
- [ ] **Results display**
  - [ ] Same as Feed page (filtering, sorting, views)
  - [ ] Result count display
  - [ ] "No results" state
- [ ] **Save search**
  - [ ] How to save current search
  - [ ] Saved search naming
  - [ ] Activate saved search immediately

**3. Saved Searches Page**
- [ ] **Display**
  - [ ] List of saved searches
  - [ ] Search criteria display
  - [ ] Match count (if available)
  - [ ] Last executed timestamp
- [ ] **Management**
  - [ ] Create new saved search
  - [ ] Edit saved search
  - [ ] Delete saved search
  - [ ] Activate/deactivate toggle
- [ ] **Notifications**
  - [ ] How to show new matches
  - [ ] Notification preferences per search

**4. Watch Page**
- [ ] **Display**
  - [ ] List of watched listings
  - [ ] Listing status (available, sold, expired)
  - [ ] Status indicators
- [ ] **Management**
  - [ ] Remove from watch list
  - [ ] Add to collection (link to Collection App)
- [ ] **Updates**
  - [ ] How to show status changes
  - [ ] Price change notifications

**5. Detail Page**
- [ ] **Information display**
  - [ ] All listing fields
  - [ ] Image gallery (swipe, zoom)
  - [ ] Source badge and link
- [ ] **Actions**
  - [ ] Mark as watch
  - [ ] Mark as dismissed
  - [ ] Add to collection
  - [ ] Share listing
  - [ ] View original listing (external link)
- [ ] **Related listings**
  - [ ] Show similar listings?
  - [ ] Show other listings from same seller?

#### Collection App Pages

**1. Home Page**
- [ ] **Display**
  - [ ] Grid vs list view
  - [ ] Items per page
  - [ ] Pagination or infinite scroll
- [ ] **Filtering**
  - [ ] Filter by type (camera, lens, other)
  - [ ] Filter by brand
  - [ ] Filter by condition
  - [ ] Search/filter by text
- [ ] **Sorting**
  - [ ] Sort options (date added, brand, value, etc.)
- [ ] **Empty state**
  - [ ] No items in collection
- [ ] **Quick actions**
  - [ ] Add new item button
  - [ ] View statistics link

**2. Add Item Page**
- [ ] **Form structure**
  - [ ] Required vs optional fields
  - [ ] Field validation rules
  - [ ] Conditional fields (show/hide based on item type)
- [ ] **Item type selection**
  - [ ] Camera, Lens, Other
  - [ ] Different fields per type
- [ ] **Image upload**
  - [ ] Multiple images
  - [ ] Image upload method (drag-drop, file picker)
  - [ ] Image preview
  - [ ] Image limits (max number, max size)
- [ ] **Autocomplete/search**
  - [ ] Camera model autocomplete
  - [ ] Brand selection
- [ ] **Linking**
  - [ ] Link to marketplace listing (from Scraper App)
  - [ ] Pre-fill data from listing
- [ ] **Save/cancel**
  - [ ] Save button behavior
  - [ ] Cancel/discard changes
  - [ ] Form validation before save

**3. Detail Page**
- [ ] **Information display**
  - [ ] All item fields
  - [ ] Photo gallery
  - [ ] Simplified vs expanded view toggle
- [ ] **Editing**
  - [ ] Edit mode (inline vs separate page)
  - [ ] Save changes
  - [ ] Cancel editing
- [ ] **Deletion**
  - [ ] Delete confirmation
  - [ ] Soft delete vs hard delete
- [ ] **Related information**
  - [ ] Link to marketplace listing (if linked)
  - [ ] Service/repair history
  - [ ] Related items

**4. Statistics Page**
- [ ] **Statistics displayed**
  - [ ] Total market value
  - [ ] Total investment
  - [ ] Brand distribution
  - [ ] Type distribution (cameras, lenses, other)
  - [ ] Timeline charts
  - [ ] Manufacturing year distribution
- [ ] **Calculations**
  - [ ] How statistics are calculated
  - [ ] Caching strategy
  - [ ] Update frequency
- [ ] **Visualizations**
  - [ ] Chart types (bar, pie, line)
  - [ ] Chart libraries to use
- [ ] **Export**
  - [ ] Export whole collection
  - [ ] Export filtered selection
  - [ ] Export format (CSV, JSON)
  - [ ] Include photos in export?

#### Negative App Pages (To Be Designed)

**1. Home Page**
- [ ] **Display structure**
  - [ ] Films collection
  - [ ] Photos collection
  - [ ] Separate sections or unified view?
- [ ] **Filtering and sorting**
  - [ ] Similar to Collection App
- [ ] **Add items**
  - [ ] Add film
  - [ ] Add photo

**2. Add Film Page**
- [ ] **Film fields**
  - [ ] Film type (35mm, 120, etc.)
  - [ ] Brand
  - [ ] ISO/ASA
  - [ ] Expiration date
  - [ ] Storage conditions
  - [ ] Purchase information
  - [ ] Photos of film
- [ ] **Film status**
  - [ ] Unused
  - [ ] Exposed (waiting development)
  - [ ] Developed
  - [ ] Archived

**3. Add Photo Page**
- [ ] **Photo fields**
  - [ ] Photo metadata (camera, lens, film, settings)
  - [ ] Date taken
  - [ ] Location
  - [ ] Description
  - [ ] Photo file upload (scan or digital)
  - [ ] Print information (if applicable)
- [ ] **Photo organization**
  - [ ] Albums/collections
  - [ ] Tags
  - [ ] Categories

**4. Detail Pages**
- [ ] Film detail page
- [ ] Photo detail page
- [ ] Similar structure to Collection App detail pages

**5. Statistics Page**
- [ ] Film statistics
- [ ] Photo statistics
- [ ] Combined statistics

#### Authentication Pages

**1. Landing Page**
- [ ] **Content**
  - [ ] Marketing information
  - [ ] Features overview
  - [ ] Call-to-action buttons
- [ ] **Login form**
  - [ ] Email/password fields
  - [ ] Social login buttons
  - [ ] "Create Account" link
  - [ ] "Forgot Password" link
- [ ] **Logged-in state**
  - [ ] Auto-redirect to App Switcher
  - [ ] Or show different content?

**2. Sign Up Page**
- [ ] **Form fields**
  - [ ] Email
  - [ ] Password
  - [ ] Confirm password
  - [ ] Terms acceptance
- [ ] **Validation**
  - [ ] Email format
  - [ ] Password strength
  - [ ] Password match
- [ ] **After submission**
  - [ ] Email verification sent
  - [ ] Redirect to verification page

**3. Sign In Page**
- [ ] **Form fields**
  - [ ] Email
  - [ ] Password
  - [ ] "Remember me" option
- [ ] **Social login**
  - [ ] Google OAuth
  - [ ] Facebook OAuth
- [ ] **Error handling**
  - [ ] Invalid credentials
  - [ ] Account disabled
  - [ ] Email not verified

**4. Forgot Password Page**
- [ ] **Form**
  - [ ] Email input
- [ ] **After submission**
  - [ ] Confirmation message
  - [ ] Email sent notification

**5. Password Reset Page**
- [ ] **Form**
  - [ ] New password
  - [ ] Confirm password
- [ ] **Validation**
  - [ ] Password strength
  - [ ] Token validation
- [ ] **After submission**
  - [ ] Success message
  - [ ] Redirect to sign in

**6. Email Verification Page**
- [ ] **Content**
  - [ ] Verification status
  - [ ] Resend verification option
- [ ] **After verification**
  - [ ] Success message
  - [ ] Redirect to sign in

#### Admin Pages

**1. Dashboard**
- [ ] **Metrics displayed**
  - [ ] User count
  - [ ] Active users
  - [ ] Scraper runs
  - [ ] Listings scraped
  - [ ] System health
- [ ] **Charts/visualizations**
  - [ ] Usage over time
  - [ ] Activity charts

**2. User Management**
- [ ] **User list**
  - [ ] Display format (table, cards)
  - [ ] Pagination
  - [ ] Search/filter
- [ ] **Actions**
  - [ ] Enable/disable user
  - [ ] Change user type (user/admin)
  - [ ] View user details
  - [ ] Delete user (with confirmation)

**3. Scraper Configuration**
- [ ] **Source management**
  - [ ] Enable/disable sources
  - [ ] Source status display
  - [ ] Last run information
- [ ] **Configuration**
  - [ ] Scraping frequency
  - [ ] Other scraper settings

**4. System Logs**
- [ ] **Log display**
  - [ ] Log list format
  - [ ] Pagination
  - [ ] Filter by type
  - [ ] Filter by date
  - [ ] Search functionality
- [ ] **Log types**
  - [ ] User Activity
  - [ ] Scraping Activity
  - [ ] System/Errors
  - [ ] Admin Actions

**5. Settings**
- [ ] **Settings categories**
  - [ ] General (site name, maintenance mode)
  - [ ] Email/SMTP
  - [ ] Security (password requirements, session timeout)
  - [ ] Feature flags
- [ ] **Settings management**
  - [ ] Edit settings
  - [ ] Save changes
  - [ ] Validation

#### App Switcher

- [ ] **Display**
  - [ ] Three apps: [Scraper App - new name], Collection App, Negative App
  - [ ] App cards with icons
  - [ ] App descriptions
- [ ] **Navigation**
  - [ ] Click app → Navigate to app
  - [ ] Logout option
- [ ] **Access control**
  - [ ] Only show apps user has access to
  - [ ] Admin link (if admin user)

**Deliverable:** Complete page behavior specifications for all pages in all apps.

---

## Phase 0.3.4: App Architecture & Naming

### Tasks to Complete

#### 1. App Renaming
- [ ] **Decide on new name for "Scraper App"**
  - [ ] Options to consider:
    - [ ] Marketplace App
    - [ ] Discover App
    - [ ] Search App
    - [ ] Browse App
    - [ ] Other: _______________
- [ ] **Update all documentation**
  - [ ] Implementation plan
  - [ ] Validation notes
  - [ ] Screen specifications
  - [ ] User journey documentation
  - [ ] Mockup references
  - [ ] ADRs (create new ADR for renaming)

#### 2. Negative App Design

**2.1 User Journeys**
- [ ] **Define entry point**
  - [ ] From App Switcher
  - [ ] Landing page
- [ ] **Define main flows**
  - [ ] Add film → View films → Film detail
  - [ ] Add photo → View photos → Photo detail
  - [ ] Organize (albums, tags, categories)
  - [ ] Statistics view
- [ ] **Define navigation**
  - [ ] Page structure
  - [ ] Navigation menu
  - [ ] Breadcrumbs (if needed)

**2.2 Data Model**
- [ ] **Film entity**
  - [ ] Fields (type, brand, ISO, expiration, storage, purchase info, photos, status)
  - [ ] Relationships (to photos if developed)
- [ ] **Photo entity**
  - [ ] Fields (metadata, date, location, description, file, print info)
  - [ ] Relationships (to film, to albums, to tags)
- [ ] **Album/Collection entity**
  - [ ] Fields (name, description, photos)
- [ ] **Tag entity**
  - [ ] Fields (name, photos)
- [ ] **Relationships**
  - [ ] User → Films (one-to-many)
  - [ ] User → Photos (one-to-many)
  - [ ] Film → Photos (one-to-many, if film was used)
  - [ ] Photo → Albums (many-to-many)
  - [ ] Photo → Tags (many-to-many)

**2.3 Pages and Features**
- [ ] **Home page**
  - [ ] Display structure (films section, photos section)
  - [ ] Filtering and sorting
  - [ ] Quick actions
- [ ] **Add Film page**
  - [ ] Form fields
  - [ ] Validation
  - [ ] Image upload
- [ ] **Add Photo page**
  - [ ] Form fields
  - [ ] File upload (scan or digital)
  - [ ] Metadata entry
  - [ ] Album/tag assignment
- [ ] **Film Detail page**
  - [ ] Information display
  - [ ] Photos from this film (if developed)
  - [ ] Edit/delete
- [ ] **Photo Detail page**
  - [ ] Photo display (zoom, fullscreen)
  - [ ] Metadata display
  - [ ] Edit/delete
  - [ ] Album/tag management
- [ ] **Albums page**
  - [ ] Album list
  - [ ] Create/edit/delete albums
  - [ ] Add photos to albums
- [ ] **Statistics page**
  - [ ] Film statistics
  - [ ] Photo statistics
  - [ ] Combined statistics
  - [ ] Charts/visualizations

**2.4 Integration**
- [ ] **Integration with Collection App**
  - [ ] Link photos to cameras/lenses used
  - [ ] Link films to cameras used
- [ ] **Integration with Scraper App**
  - [ ] Any integration needed?

#### 3. App Switcher Updates
- [ ] **Update to three apps**
  - [ ] [Scraper App - new name] card
  - [ ] Collection App card
  - [ ] Negative App card
- [ ] **App descriptions**
  - [ ] Brief description for each app
  - [ ] Icons for each app
- [ ] **Navigation**
  - [ ] Click app → Navigate to app home
  - [ ] Consistent navigation pattern

#### 4. Documentation Updates
- [ ] **Update implementation plan**
  - [ ] Rename all "Scraper App" references
  - [ ] Add Negative App phases
- [ ] **Update validation notes**
  - [ ] Update user journey references
  - [ ] Add Negative App user journeys
- [ ] **Update screen specifications**
  - [ ] Rename Scraper App pages
  - [ ] Add Negative App pages
- [ ] **Create ADR**
  - [ ] Document app renaming decision
  - [ ] Document Negative App addition decision
- [ ] **Update mockup references**
  - [ ] Note any mockup updates needed

**Deliverable:** Complete app architecture with renamed app, new Negative App fully specified, and all documentation updated.

---

## Summary

Phase 0.3 ensures that before we start implementation (Phase 1), we have:

1. ✅ **Complete UI specifications** - All components, states, interactions defined
2. ✅ **Complete scraper behavior** - How scraper works in all scenarios
3. ✅ **Complete page behaviors** - Detailed behavior for every page
4. ✅ **Complete app architecture** - Three apps fully specified

This prevents rework during implementation and ensures we have a clear roadmap.

---

**Next Steps:**
1. Work through Phase 0.3.1 (UI Components)
2. Work through Phase 0.3.2 (Scraper Behavior)
3. Work through Phase 0.3.3 (Page Behaviors)
4. Work through Phase 0.3.4 (App Architecture)
5. Review all specifications
6. Proceed to Phase 0.4 (Final Validation & Decision)
