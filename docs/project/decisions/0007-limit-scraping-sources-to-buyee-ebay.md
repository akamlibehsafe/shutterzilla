# 0007 - Limit Scraping Sources to Buyee and eBay

## Status
Accepted

## Context
ShutterZilla needs to aggregate camera listings from marketplace sources to provide comprehensive market data. The project scope is limited to friends/family (max 10 users) with a $0/month budget constraint. We need to balance:
- Coverage of major vintage camera markets (Japan and USA)
- Maintenance burden (each source requires custom scraper)
- API availability and scraping complexity
- Data quality and reliability

## Decision
Limit scraping to two sources only: **Buyee** (Japan) and **eBay** (USA). Each source is identified with a visual badge in the UI.

## Alternatives considered
- **Add Mercari (Japan)**: Initially considered as a separate source. However, Mercari scraping proved to be very complicated due to the site's structure, while Buyee was easier to implement and more reliable. Additionally, Mercari listings are available on Buyee as a shop, so Mercari coverage is already included through Buyee. Pros - would provide direct Mercari access. Cons - complex scraping implementation, redundant coverage (already via Buyee), additional maintenance burden
- **Add Yahoo Auctions (Japan)**: Pros - large Japanese marketplace. Cons - complex scraping, additional maintenance
- **Add Facebook Marketplace**: Pros - local listings. Cons - requires location, complex authentication, lower data quality
- **Add Craigslist**: Pros - local listings. Cons - no API, complex scraping, low data quality, geographic limitations
- **Buyee + eBay only**: Pros - covers two major markets (Japan/USA), manageable maintenance, clear source identification. Cons - less coverage than multiple sources (acceptable for small user base)

## Consequences
- Simpler scraper architecture (only 2 sources to maintain)
- Clear source identification with visual badges
- Sufficient coverage for initial 10-user target
- Lower maintenance burden
- Can add more sources later if needed (architecture supports it)
- Less comprehensive than multi-source aggregator (acceptable trade-off)

## Links
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
- Scraper Behavior Spec: `docs/specification/implementation/implementation-scraper-behavior-specification.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
