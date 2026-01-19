# Buyee Scraper - Extracted Fields

**Last Updated:** 2026-01-XX  
**Status:** Validated and Working

---

## Overview

The Buyee scraper operates in two phases:
- **Phase 1 (Search Results)**: Extracts basic fields from search result listings
- **Phase 2 (Detail Pages)**: Extracts additional detailed fields from individual listing pages

---

## Phase 1: Search Results Fields

Extracted from search results page (`buyee_search.py`):

### Common Fields (All Shops)
- ✅ **title** (string) - Item title/name
  - Translated to English if contains Japanese
  - Required field
- ✅ **image_url** (string) - Thumbnail image URL
  - Product image (not icon/badge)
  - Required field (warning if missing)
- ✅ **listing_url** (string) - Full URL to listing page
  - Format: `https://buyee.jp/item/{shop}/{listing_id}`
  - Required field
- ✅ **listing_id** (string) - Unique listing identifier
  - Extracted from URL
  - Required field
- ✅ **shop_name** (string) - Shop/marketplace name
  - Values: `Yahoo Japan Auctions`, `Yahoo Japan Fleamarket`, `Mercari`, `Rakuma`
  - Required field

### Shop-Specific Price Fields

#### Yahoo Japan Auctions
- ✅ **buyout_price** (string) - Buyout/即決価格 price
  - Format: `¥XX,XXX` or `XX,XXX` (may include currency symbol)
  - At least one price (buyout or current) required
- ✅ **current_price** (string) - Current bid/現在価格 price
  - Format: `¥XX,XXX` or `XX,XXX` (may include currency symbol)
  - At least one price (buyout or current) required

#### Other Shops (Mercari, Rakuma, Yahoo Japan Fleamarket)
- ✅ **price** (string) - Single price value
  - Format: `¥XX,XXX` or `XX,XXX` (may include currency symbol)
  - Required field

---

## Phase 2: Detail Page Fields

Extracted from individual listing detail pages (`buyee_details.py`):

### Common Fields (All Shops)
- ✅ **title** (string) - Item title (re-extracted, may be more complete)
  - Translated to English if contains Japanese
- ✅ **description** (string) - Item description/explanation
  - Extracted from `section#item-description` (inside iframe)
  - Translated to English if contains Japanese
  - Required field (warning if missing or very short)
- ✅ **status** (string) - Listing availability status
  - Values: `sold`, `available`
  - Required field (warning if missing)
- ✅ **all_images** (array of strings) - All product image URLs
  - Filtered to exclude icons, badges, logos
  - Required field (warning if empty)
- ✅ **shop_name** (string) - Shop name (re-extracted for accuracy)
- ✅ **listing_id** (string) - Listing ID (re-extracted for accuracy)
- ✅ **seller_info** (string) - Seller information
  - Translated to English if contains Japanese
  - Optional field
- ✅ **shipping_info** (string) - Shipping information
  - Translated to English if contains Japanese
  - Optional field

### Yahoo Japan Auctions-Specific Fields
- ✅ **buyout_price** (string) - Buyout price (more accurate than Phase 1)
  - Extracted from detail page
  - Format: `¥XX,XXX` or `XX,XXX`
- ✅ **current_price** (string) - Current bid price (more accurate than Phase 1)
  - Extracted from detail page
  - Format: `¥XX,XXX` or `XX,XXX`
- ✅ **condition** (string) - Item condition/状態
  - Extracted from `section#itemDetail_sec` table
  - Translated to English if contains Japanese
  - Optional field
- ✅ **number_of_bids** (string) - Number of bids/入札数
  - Extracted from `section#itemDetail_sec` table
  - Optional field
- ✅ **closing_time_jst** (string) - Auction closing time in JST
  - Extracted from `section#itemDetail_sec` table
  - Format: Date/time string
  - Optional field

---

## Field Extraction Notes

### Translation
- Japanese text is automatically translated to English using `deep-translator` library
- Fields that may contain Japanese: `title`, `description`, `condition`, `seller_info`, `shipping_info`

### Price Formats
- Prices may include currency symbols (`¥`, `円`) or be numeric only
- Prices may include commas as thousands separators
- Prices are stored as strings (not converted to numbers)

### Image Handling
- Product images are filtered to exclude:
  - Icons (`icon_`, `icon.`, `common/icon`)
  - Badges (`badge`)
  - Logos (`logo`, `common/logo`)
  - Spacers (`spacer`, `1x1`)
- Images from known product sources are prioritized:
  - `auctions.yahoo.co.jp`
  - `mercdn.net`
  - `rakuten`
  - `buyee` (excluding common icons/logos)

### Shop Name Mapping
- `JDirectItems Auction` → `Yahoo Japan Auctions`
- `Mercari` → `Mercari`
- `Rakuten Rakuma` → `Rakuma`
- `JDirectItems Fleamarket` → `Yahoo Japan Fleamarket`

### Description Extraction
- Description is inside an iframe within `section#itemDescription`
- Multiple fallback strategies if iframe access fails
- Description is cleaned (script/style tags removed)
- Generic Buyee text is filtered out

---

## Validation

### Phase 1 Validation (`validate_search_result`)
**Required Fields:**
- `title` (min 3 characters)
- `listing_url` (must start with `https://buyee.jp`)
- `listing_id`
- `shop_name` (must be valid shop name)
- Price field (shop-specific):
  - Yahoo Japan Auctions: at least one of `buyout_price` or `current_price`
  - Other shops: `price`

**Optional Fields (warnings if missing):**
- `image_url` (warning if missing or invalid format)

### Phase 2 Validation (`validate_listing_details`)
**Required Fields:**
- `description` (min 10 characters) - warning if missing
- `all_images` (at least one image) - warning if empty
- `status` - warning if missing

**Shop-Specific Validation:**
- Yahoo Japan Auctions: at least one price (`buyout_price` or `current_price`) - warning if both missing

---

## Current Limitations

1. **Price Currency**: Prices are stored as strings with currency symbols, not normalized to a single currency
2. **Price Parsing**: Prices are not converted to numeric values (stored as strings)
3. **Date Parsing**: Closing time is stored as string, not parsed to datetime
4. **Condition Values**: Condition values are not standardized (free-form text)
5. **Image URLs**: All images stored as URLs, not downloaded locally (unless explicitly requested)
6. **Description Formatting**: Description is plain text, HTML formatting is removed

---

## Example Output Structure

### Phase 1 (Search Results)
```json
{
  "title": "Nikon FM2 Titanium",
  "image_url": "https://cdnyauction-pctr.buyee.jp/i/...",
  "listing_url": "https://buyee.jp/item/jdirectitems/auction/j1215962091",
  "listing_id": "j1215962091",
  "shop_name": "Yahoo Japan Auctions",
  "buyout_price": "¥89,850",
  "current_price": "¥35,000"
}
```

### Phase 2 (Detail Page - Yahoo Japan Auctions)
```json
{
  "title": "Nikon FM2 Titanium",
  "description": "Full item description text...",
  "status": "available",
  "all_images": ["https://...", "https://..."],
  "shop_name": "Yahoo Japan Auctions",
  "listing_id": "j1215962091",
  "buyout_price": "¥89,850",
  "current_price": "¥35,000",
  "condition": "Mint",
  "number_of_bids": "5",
  "closing_time_jst": "2026-01-20 15:00 JST",
  "seller_info": "Seller name and info",
  "shipping_info": "Shipping details"
}
```

---

## Notes

- All fields are extracted as strings (no type conversion)
- Japanese text is translated to English automatically
- Validation provides warnings but doesn't block data collection
- Phase 2 provides more accurate/complete data than Phase 1
- Some fields may be empty/null if not available on the page
