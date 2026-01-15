# Scraper Behavior Specification

This document defines how the scraper service works: what it does, how it does it, and how it integrates with the rest of the system.

**Status:** To Be Defined  
**Approach:** Work through this together as we design the scraper

---

## Scraper Overview

The scraper service runs on a schedule (every 4 hours) and collects camera listings from multiple sources.

---

## Questions to Define

### General Behavior
- [ ] How often does the scraper run?
- [ ] What happens if a scraper run fails?
- [ ] How do we handle rate limiting from sources?
- [ ] How do we handle changes to source websites?
- [ ] How do we handle duplicate listings across sources?
- [ ] How do we track what's been scraped?

### Data Collection
- [ ] What data do we collect from each source?
- [ ] How do we normalize data across different sources?
- [ ] How do we handle missing data?
- [ ] How do we handle data that changes (price updates, status changes)?
- [ ] How do we store images (URLs only, or download and store)?

### Deduplication
- [ ] How do we identify duplicate listings?
- [ ] What makes a listing "the same" across sources?
- [ ] How do we handle the same listing on multiple sources?
- [ ] Do we merge data or keep separate records?

### Status Tracking
- [ ] How do we know if a listing is still active?
- [ ] How do we handle "sold" or "expired" listings?
- [ ] How long do we keep inactive listings?
- [ ] How do we update listing status?

### Error Handling
- [ ] What happens if a source is down?
- [ ] What happens if a source changes their HTML structure?
- [ ] How do we log errors?
- [ ] How do we notify about scraper issues?

### Performance
- [ ] How many listings do we scrape per run?
- [ ] How do we handle large result sets?
- [ ] How do we optimize database writes?
- [ ] How long should a scraper run take?

### Integration
- [ ] How does the scraper connect to the database?
- [ ] How do we trigger saved search matching?
- [ ] How do we notify users of new matches?
- [ ] How do we handle scraper configuration changes?

---

## Source-Specific Questions

### Buyee
- [ ] What's the scraping approach?
- [ ] What fields are available?
- [ ] What are the rate limits?
- [ ] How do we handle pagination?

### eBay
- [ ] What's the scraping approach?
- [ ] Do we use eBay API or scrape HTML?
- [ ] What fields are available?
- [ ] What are the rate limits?

---

## Current Specification

_(To be refined as we work through this together)_

---

## Notes

- We'll refine this specification as we design and implement the scraper
- Each source may have different approaches
- We'll document decisions and rationale as we go
- This will inform the database schema and API design
