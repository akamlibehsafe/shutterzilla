# Scraping Validation Tests

This directory contains test scripts to validate scraping feasibility for each source website.

## Structure

- `scrapers/` - Test scripts for each source
- `results/` - Test results and documentation

## Sources to Test

1. Mercari Japan (`mercari.jp`)
2. Buyee (`buyee.jp`)
3. Yahoo Japan Auctions (`auctions.yahoo.co.jp`)
4. eBay USA (`ebay.com`)

## Running Tests

Each test script can be run independently:

```bash
python validation/scrapers/test_mercari.py
python validation/scrapers/test_buyee.py
python validation/scrapers/test_yahoo_auctions.py
python validation/scrapers/test_ebay.py
```

## Requirements

Install required Python packages:

```bash
pip install requests beautifulsoup4
# If JavaScript rendering is needed:
pip install playwright
```

## Test Criteria

For each source, we test:
- Can we access the website?
- Can we find/search for camera listings?
- Can we extract key data fields (title, price, images, URL)?
- Are there rate limits or blocking mechanisms?
- Is the HTML structure stable enough to scrape?
- Do we need JavaScript rendering (Playwright) or can we use simple HTTP (BeautifulSoup)?
- Are there anti-bot measures we need to handle?
