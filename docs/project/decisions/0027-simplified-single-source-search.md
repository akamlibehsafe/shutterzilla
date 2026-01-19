# 0027 - Simplified Single-Source Search (No Multi-Source Aggregation)

## Status
Accepted

## Context
The Search page initially included an "All" option in the source filter pills, suggesting that searches could aggregate results from multiple sources (Buyee and eBay) simultaneously.

However, implementing multi-source search aggregation adds significant complexity:
- Different APIs and data structures per source
- Different search capabilities and filters per source
- Complex result merging and deduplication
- Different pagination and rate limiting per source
- More complex error handling
- Performance considerations (waiting for slowest source)

## Decision
**Remove multi-source search aggregation for MVP. Users select one source at a time for searching.**

**Changes:**
- Removed "All" pill from Search page source filters
- Search page now requires selecting either "Buyee" or "eBay" as the source
- Each search query targets a single source
- Feed page can still show aggregated results (different use case - browsing vs searching)

**Rationale:**
- Simpler implementation - one API/source per search
- Clearer user experience - users know exactly which source they're searching
- Faster development - no complex aggregation logic needed
- Better performance - no waiting for multiple sources
- Easier error handling - single source failures don't affect others
- Can be enhanced later if needed

## Consequences
**Positive:**
- Simpler implementation and faster development
- Clearer user intent (searching specific source)
- Better performance (single API call)
- Easier to debug and maintain
- Can add multi-source aggregation later if user demand exists

**Negative:**
- Users must perform separate searches for each source
- Cannot see combined results from all sources in one search
- Slightly more clicks to search multiple sources

## Future Considerations
If user feedback indicates strong demand for multi-source search:
- Could add "All Sources" option later
- Would need to implement result aggregation logic
- Would need to handle different API response formats
- Would need to implement deduplication across sources
- Would need to handle different pagination strategies

## Notes
- Feed page still shows aggregated results from all sources (different use case)
- This decision applies specifically to the Search page functionality
- Saved searches can still target specific sources individually
