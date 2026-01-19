# Buyee Scraper Fields - Quick Reference Table

**Last Updated:** 2026-01-XX

---

## Phase 1: Search Results Fields

| Field Name | Shop | Type | Required | Notes |
|------------|------|------|----------|-------|
| `title` | All | string | ✅ Yes | Translated if Japanese |
| `image_url` | All | string | ⚠️ Warning | Thumbnail image URL |
| `listing_url` | All | string | ✅ Yes | Full URL to listing page |
| `listing_id` | All | string | ✅ Yes | Extracted from URL |
| `shop_name` | All | string | ✅ Yes | Yahoo Japan Auctions, Mercari, Rakuma, Yahoo Japan Fleamarket |
| `buyout_price` | Yahoo Japan Auctions only | string | ✅ Yes* | At least one price required |
| `current_price` | Yahoo Japan Auctions only | string | ✅ Yes* | At least one price required |
| `price` | Mercari, Rakuma, Fleamarket | string | ✅ Yes | Single price value |

*For Yahoo Japan Auctions: At least one of `buyout_price` OR `current_price` is required.

---

## Phase 2: Detail Page Fields

| Field Name | Shop | Type | Required | Notes |
|------------|------|------|----------|-------|
| `title` | All | string | - | Re-extracted (may be more complete) |
| `description` | All | string | ⚠️ Warning | From iframe, translated if Japanese |
| `status` | All | string | ⚠️ Warning | Values: `sold`, `available` |
| `all_images` | All | array[string] | ⚠️ Warning | All product images (filtered) |
| `shop_name` | All | string | - | Re-extracted for accuracy |
| `listing_id` | All | string | - | Re-extracted for accuracy |
| `seller_info` | All | string | Optional | Translated if Japanese |
| `shipping_info` | All | string | Optional | Translated if Japanese |
| `buyout_price` | Yahoo Japan Auctions only | string | ⚠️ Warning* | More accurate than Phase 1 |
| `current_price` | Yahoo Japan Auctions only | string | ⚠️ Warning* | More accurate than Phase 1 |
| `condition` | Yahoo Japan Auctions only | string | Optional | Item condition/状態 |
| `number_of_bids` | Yahoo Japan Auctions only | string | Optional | Number of bids/入札数 |
| `closing_time_jst` | Yahoo Japan Auctions only | string | Optional | Auction closing time |

*For Yahoo Japan Auctions: At least one of `buyout_price` OR `current_price` should be present (warning if both missing).

---

## Legend

- ✅ **Yes** = Required field (validation fails if missing)
- ⚠️ **Warning** = Recommended field (validation warns if missing, but data is still collected)
- **Optional** = Field may be empty/null if not available
- **-** = Field is re-extracted in Phase 2 but not required

---

## Shop Name Values

- `Yahoo Japan Auctions`
- `Yahoo Japan Fleamarket`
- `Mercari`
- `Rakuma`

---

## Status Values

- `sold`
- `available`

---

## Price Format Notes

- Prices stored as strings (not converted to numbers)
- May include currency symbols: `¥`, `円`
- May include commas as thousands separators
- Examples: `¥89,850`, `89,850`, `¥35.93`

---

## Translation

Fields automatically translated from Japanese to English:
- `title`
- `description`
- `condition`
- `seller_info`
- `shipping_info`
