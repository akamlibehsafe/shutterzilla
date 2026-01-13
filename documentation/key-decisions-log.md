_This document logs key decisions made during the design and prototyping phase. It should be updated as the project evolves._

# Key Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-01-12 | **Adopt a Teal-based Primary Color Scheme** | The teal color (`#0d9488`) was chosen to evoke a sense of modernity and trust, differentiating the platform from more traditional vintage camera sites. It provides a vibrant accent against the clean, minimal gray and white layout. |
| 2026-01-12 | **Standardize on a Single Top Bar and Footer** | A consistent top bar and footer across all application pages (excluding landing/auth) ensures a predictable user experience and reinforces the brand identity. The top bar provides global navigation, while the footer offers access to legal and informational pages. |
| 2026-01-13 | **Separate Scraper and Collection into Two Distinct Apps** | Instead of a single, monolithic interface, the core functionalities were split into two applications accessible from a central App Switcher. This simplifies the user journey for each primary task—browsing listings versus managing a personal collection—and allows for more focused feature development. |
| 2026-01-13 | **Use HTML/CSS for Prototypes Instead of a Design Tool** | Building prototypes directly in HTML and CSS allows for immediate testing of responsiveness and interaction. It also provides a head start for the development team, as the structure and styling can be directly adapted for the final implementation. |
| 2026-01-13 | **Implement a Multi-Source Scraper with Visual Badges** | To provide comprehensive market data, the scraper aggregates listings from multiple sources (Mercari, Buyee, eBay, JD). Each source is clearly identified with a colored badge, giving users at-a-glance information about the listing's origin. |
| 2026-01-13 | **Fix Inconsistent Footer Logo** | The initial footer on the legal pages (`about.html`, `privacy.html`, `terms.html`) used an inline SVG for the logo, which was inconsistent with the rest of the site. This was corrected to use the standard `logo-footer.png` image to ensure brand consistency. |
| 2026-01-13 | **Link Profile Icon to Admin Dashboard** | To provide a consistent and intuitive way for administrators to access the backend, the user profile icon in the top bar of all application pages now links directly to the `admin_dashboard.html`. This simplifies navigation and makes the admin section easily discoverable. |
