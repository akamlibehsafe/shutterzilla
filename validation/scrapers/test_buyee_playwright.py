#!/usr/bin/env python3
"""
⚠️  DEPRECATED / BACKUP FILE ⚠️

This file has been refactored into modular scripts:
- buyee_utils.py (shared utilities)
- buyee_search.py (Phase 1: search results)
- buyee_details.py (Phase 2: detail pages)

This file is kept as backup only. Use the refactored scripts instead.
After testing confirms the new scripts work, this file will be deleted.

---
Buyee Scraping Test - Playwright Version

This script tests Buyee scraping using Playwright for JavaScript rendering.
Buyee is a proxy service for Japanese marketplaces

FUTURE FEATURES (Require Database Integration):
==============================================

1. FILTER_NEW_LISTINGS_ONLY:
   - Returns only listings that haven't been scraped before
   - Requires: Database with listings table
   - Functions to implement:
     * check_listing_exists(listing_id) -> bool
     * mark_listing_as_scraped(listing_id, scraped_at) -> None

2. STATUS_UPDATE_MODE:
   - For existing listings, only updates status field (sold/available)
   - Skips full Phase 2 scraping for existing listings (faster)
   - Requires: Database with listings table and status field
   - Functions to implement:
     * get_existing_listing(listing_id) -> dict or None
     * update_listing_status(listing_id, status) -> None
     * is_listing_status_changed(listing_id, new_status) -> bool

See placeholders in code for implementation details.
"""

import json
import time
import os
import requests
import logging
import argparse
import sys
from datetime import datetime
from urllib.parse import urlparse, quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")

# Test configuration
BASE_URL = "https://buyee.jp"
DEFAULT_SEARCH_TERM = "Nikon FM2"  # Default search term if not provided as argument

# Phase 2 parallelization settings
PHASE2_PARALLEL = True  # Set to False to process sequentially
PHASE2_MAX_WORKERS = 3  # Number of concurrent detail page scrapes (3-5 recommended for stability)
PHASE2_RETRY_ATTEMPTS = 2  # Number of retry attempts for failed scrapes
PHASE2_DELAY_BETWEEN_REQUESTS = 0.5  # Delay in seconds between requests (helps avoid rate limiting)
PHASE2_RATE_LIMIT_THRESHOLD = 3  # Number of rate limit errors before switching to sequential
PHASE2_FAILURE_THRESHOLD = 0.3  # Fraction of failures (0.3 = 30%) before switching to sequential

# Pagination settings
PAGINATION_ENABLED = True  # Set to False to only scrape first page
PAGINATION_MAX_PAGES = None  # Maximum pages to scrape (None = all pages, or set a number like 5)
PAGINATION_DELAY_BETWEEN_PAGES = 1.0  # Delay in seconds between page loads

# Logging settings
LOG_ENABLED = True  # Enable/disable logging
LOG_DIR = 'validation/results/logs'  # Directory for log files
LOG_LEVEL = logging.INFO  # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_CONSOLE = True  # Also output to console (in addition to log file)
LOG_FILE_PREFIX = 'buyee_scraper'  # Prefix for log file names

# Future features (require database integration - not yet implemented)
# ====================================================================
# FEATURE 1: Filter New Listings Only
# ====================================================================
# When enabled, only returns listings that haven't been scraped before.
# Requires:
# - Database connection to check existing listings
# - Function: check_listing_exists(listing_id) -> bool
# - Function: mark_listing_as_scraped(listing_id, scraped_at) -> None
FILTER_NEW_LISTINGS_ONLY = False  # Set to True when database is ready

# ====================================================================
# FEATURE 2: Status-Only Updates for Existing Listings
# ====================================================================
# When enabled, for listings that already exist in database:
# - Only updates status field (sold/available)
# - Skips Phase 2 detail scraping (faster updates)
# - Only scrapes Phase 1 data to get current status
# Requires:
# - Database connection to check existing listings
# - Function: get_existing_listing(listing_id) -> dict or None
# - Function: update_listing_status(listing_id, status) -> None
# - Function: is_listing_status_changed(listing_id, new_status) -> bool
STATUS_UPDATE_MODE = False  # Set to True when database is ready
STATUS_UPDATE_SKIP_PHASE2 = True  # Skip Phase 2 for status-only updates (faster)

def translate_japanese(text, target_lang='en'):
    """Translate Japanese text to English (or other language)"""
    if not text:
        return text
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='ja', target=target_lang)
        translated = translator.translate(text)
        return translated
    except ImportError:
        print("Warning: deep-translator not installed. Install with: pip install deep-translator")
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def contains_japanese(text):
    """Check if text contains Japanese characters"""
    if not text:
        return False
    return any(ord(char) > 127 and (
        (0x3040 <= ord(char) <= 0x309F) or  # Hiragana
        (0x30A0 <= ord(char) <= 0x30FF) or  # Katakana
        (0x4E00 <= ord(char) <= 0x9FAF)     # Kanji
    ) for char in text[:100])

def extract_listing_id(listing_url):
    """Extract unique Listing ID from Buyee listing URL
    
    URL patterns for all shops:
    - Yahoo Japan Auctions: https://buyee.jp/item/jdirectitems/auction/{ID}
    - Yahoo Japan Fleamarket: https://buyee.jp/paypayfleamarket/item/{ID}
    - Mercari: https://buyee.jp/mercari/item/{ID}
    - Rakuma: https://buyee.jp/rakuma/item/{ID}
    
    Returns the ID (last segment of path before query params) or None if not found.
    """
    if not listing_url:
        return None
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(listing_url)
        path = parsed.path.strip('/')
        
        if not path:
            return None
        
        # Split path and get the last segment (should be the ID)
        path_parts = [p for p in path.split('/') if p]
        
        if path_parts:
            # The ID is typically the last segment
            # Examples: 't1215619702', 'f1215860415', etc.
            listing_id = path_parts[-1]
            
            # Remove query parameters if any (though they shouldn't be in path)
            if '?' in listing_id:
                listing_id = listing_id.split('?')[0]
            
            return listing_id
        
        return None
    except Exception as e:
        print(f"Error extracting listing ID from {listing_url}: {e}")
        return None

def validate_listing_details(detail, shop_name):
    """Validate a listing's detail page data
    
    Returns (is_valid, errors) tuple where:
    - is_valid: boolean indicating if detail data is valid
    - errors: list of validation error messages
    """
    errors = []
    
    # Description should be present (important field)
    if not detail.get('description') or len(detail.get('description', '').strip()) < 10:
        errors.append("Warning: Missing or very short description")
    
    # Shop-specific validation for Yahoo Japan Auctions
    if shop_name == 'Yahoo Japan Auctions':
        # Yahoo Japan Auctions should have at least one price in detail page (more accurate than search results)
        if not detail.get('buyout_price') and not detail.get('current_price'):
            errors.append("Warning: Yahoo Japan Auctions listing missing both buyout_price and current_price in detail page")
    
    # Images validation
    all_images = detail.get('all_images', [])
    if not all_images or len(all_images) == 0:
        errors.append("Warning: No product images found")
    else:
        # Check for valid image URLs
        invalid_images = [img for img in all_images if not img.startswith(('http://', 'https://'))]
        if invalid_images:
            errors.append(f"Warning: {len(invalid_images)} invalid image URL(s)")
    
    # Status should be present
    if not detail.get('status'):
        errors.append("Warning: Missing status (sold/available)")
    
    # All errors are warnings for Phase 2 (we still want the data even if some fields are missing)
    is_valid = True  # Phase 2 is more lenient - we keep the data even with warnings
    return is_valid, errors

# ====================================================================
# LOGGING SETUP
# ====================================================================

def setup_logging():
    """Setup logging configuration
    
    Creates a log file with timestamp and configures logging to both
    file and console (if enabled).
    """
    if not LOG_ENABLED:
        # Disable logging
        logging.disable(logging.CRITICAL)
        return None
    
    # Create log directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{LOG_FILE_PREFIX}_{timestamp}.log"
    log_filepath = os.path.join(LOG_DIR, log_filename)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # File handler (always enabled if logging is enabled)
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (if enabled)
    if LOG_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = logging.Formatter(log_format, date_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Log initial message
    logger.info("=" * 60)
    logger.info("Buyee Scraper - Logging Started")
    logger.info("=" * 60)
    logger.info(f"Log file: {log_filepath}")
    logger.info(f"Log level: {logging.getLevelName(LOG_LEVEL)}")
    logger.info(f"Console output: {LOG_CONSOLE}")
    logger.info("")
    
    return log_filepath

def log_info(message):
    """Log info message"""
    if LOG_ENABLED:
        logging.info(message)
    if LOG_CONSOLE:
        print(message)

def log_warning(message):
    """Log warning message"""
    if LOG_ENABLED:
        logging.warning(message)
    if LOG_CONSOLE:
        print(f"⚠️ {message}")

def log_error(message):
    """Log error message"""
    if LOG_ENABLED:
        logging.error(message)
    if LOG_CONSOLE:
        print(f"❌ {message}")

def log_debug(message):
    """Log debug message"""
    if LOG_ENABLED:
        logging.debug(message)
    if LOG_CONSOLE:
        print(f"🔍 {message}")

def log_success(message):
    """Log success message"""
    if LOG_ENABLED:
        logging.info(f"✅ {message}")
    if LOG_CONSOLE:
        print(f"✅ {message}")

# ====================================================================
# FUTURE FEATURE PLACEHOLDERS - Database Integration Required
# ====================================================================

def check_listing_exists(listing_id):
    """PLACEHOLDER: Check if a listing already exists in database
    
    TODO: Implement database query to check if listing_id exists
    Returns: bool - True if listing exists, False if new
    
    Example implementation:
        connection = get_database_connection()
        query = "SELECT COUNT(*) FROM listings WHERE listing_id = ?"
        result = connection.execute(query, (listing_id,))
        return result.fetchone()[0] > 0
    """
    # Placeholder - always returns False (assume all listings are new)
    return False

def mark_listing_as_scraped(listing_id, scraped_at=None):
    """PLACEHOLDER: Mark a listing as scraped in database
    
    TODO: Implement database insert/update to mark listing as scraped
    Args:
        listing_id: Unique listing identifier
        scraped_at: Timestamp (defaults to current time)
    
    Example implementation:
        connection = get_database_connection()
        query = "INSERT INTO listings (listing_id, scraped_at) VALUES (?, ?)"
        connection.execute(query, (listing_id, scraped_at or datetime.now()))
        connection.commit()
    """
    # Placeholder - no-op
    pass

def get_existing_listing(listing_id):
    """PLACEHOLDER: Get existing listing data from database
    
    TODO: Implement database query to retrieve existing listing
    Returns: dict with listing data or None if not found
    
    Example implementation:
        connection = get_database_connection()
        query = "SELECT * FROM listings WHERE listing_id = ?"
        result = connection.execute(query, (listing_id,))
        row = result.fetchone()
        return dict(row) if row else None
    """
    # Placeholder - always returns None (assume no existing listings)
    return None

def update_listing_status(listing_id, status):
    """PLACEHOLDER: Update only the status field of an existing listing
    
    TODO: Implement database update to change listing status
    Args:
        listing_id: Unique listing identifier
        status: New status ('sold' or 'available')
    
    Example implementation:
        connection = get_database_connection()
        query = "UPDATE listings SET status = ?, updated_at = ? WHERE listing_id = ?"
        connection.execute(query, (status, datetime.now(), listing_id))
        connection.commit()
    """
    # Placeholder - no-op
    pass

def is_listing_status_changed(listing_id, new_status):
    """PLACEHOLDER: Check if listing status has changed
    
    TODO: Implement database query to compare current status with new status
    Returns: bool - True if status changed, False if same
    
    Example implementation:
        existing = get_existing_listing(listing_id)
        if not existing:
            return True  # New listing, consider it changed
        return existing.get('status') != new_status
    """
    # Placeholder - always returns True (assume status changed)
    return True

def filter_new_listings(listings):
    """Filter listings to return only new ones (not yet in database)
    
    This function uses check_listing_exists() to filter out listings
    that have already been scraped.
    
    Args:
        listings: List of listing dictionaries
    
    Returns:
        List of new listings only
    """
    if not FILTER_NEW_LISTINGS_ONLY:
        return listings
    
    new_listings = []
    for listing in listings:
        listing_id = listing.get('listing_id')
        if listing_id and not check_listing_exists(listing_id):
            new_listings.append(listing)
        else:
            log_info(f"  ⏭️  Skipping existing listing: {listing_id}")
    
    log_info(f"  📊 Filtered: {len(new_listings)} new listings out of {len(listings)} total")
    return new_listings

def process_status_updates(listings):
    """Process listings for status-only updates
    
    For listings that already exist in database, only update their status
    without doing full Phase 2 scraping.
    
    Args:
        listings: List of listing dictionaries from Phase 1
    
    Returns:
        Tuple of (listings_to_update_status, listings_to_scrape_fully)
    """
    if not STATUS_UPDATE_MODE:
        return [], listings
    
    status_updates = []
    new_listings = []
    
    for listing in listings:
        listing_id = listing.get('listing_id')
        if not listing_id:
            new_listings.append(listing)
            continue
        
        existing = get_existing_listing(listing_id)
        if existing:
            # Listing exists - check if status update is needed
            # Note: Status is extracted in Phase 2, so we'll need to do
            # a lightweight Phase 2 check or extract status from Phase 1
            # For now, we'll mark it for status update check in Phase 2
            status_updates.append(listing)
        else:
            # New listing - needs full scrape
            new_listings.append(listing)
    
    log_info(f"  📊 Status updates: {len(status_updates)} existing, {len(new_listings)} new")
    return status_updates, new_listings

def validate_search_result(listing):
    """Validate a listing from search results
    
    Returns (is_valid, errors) tuple where:
    - is_valid: boolean indicating if listing is valid
    - errors: list of validation error messages
    """
    errors = []
    
    # Required fields
    if not listing.get('title') or len(listing.get('title', '').strip()) < 3:
        errors.append("Missing or invalid title")
    
    if not listing.get('listing_url'):
        errors.append("Missing listing URL")
    elif not listing['listing_url'].startswith('https://buyee.jp'):
        errors.append(f"Invalid listing URL format: {listing.get('listing_url')}")
    
    if not listing.get('listing_id'):
        errors.append("Missing listing ID")
    
    if not listing.get('shop_name'):
        errors.append("Missing shop name")
    elif listing['shop_name'] not in ['Yahoo Japan Auctions', 'Yahoo Japan Fleamarket', 'Mercari', 'Rakuma']:
        errors.append(f"Unknown shop name: {listing.get('shop_name')}")
    
    # Shop-specific price validation
    shop_name = listing.get('shop_name')
    if shop_name == 'Yahoo Japan Auctions':
        # Yahoo Japan Auctions should have at least one price (buyout or current)
        if not listing.get('buyout_price') and not listing.get('current_price'):
            errors.append("Yahoo Japan Auctions listing missing both buyout_price and current_price")
    else:
        # Other shops should have price
        if not listing.get('price'):
            errors.append(f"{shop_name} listing missing price")
    
    # Optional but recommended fields
    if not listing.get('image_url'):
        errors.append("Warning: Missing thumbnail image URL")
    elif not listing['image_url'].startswith(('http://', 'https://')):
        errors.append(f"Warning: Invalid image URL format: {listing.get('image_url')}")
    
    is_valid = len([e for e in errors if not e.startswith('Warning:')]) == 0
    return is_valid, errors

def download_image(image_url, output_dir, listing_index, image_index=0):
    """Download an image from URL and save it locally"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=10, stream=True)
        if response.status_code == 200:
            parsed_url = urlparse(image_url)
            ext = os.path.splitext(parsed_url.path)[1] or '.jpg'
            if '?' in ext:
                ext = ext.split('?')[0]
            filename = f"listing_{listing_index}_image_{image_index}{ext}"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")
    return None

def scrape_search_results(page):
    """Phase 1: Scrape search results page
    
    Extracts limited fields from search results:
    - Title
    - Shop Name
    - Price (general price for all shops)
    - Thumbnail Image URL
    - Listing URL
    - Listing ID (derived from URL)
    """
    try:
        # Wait for page to load
        log_info("Waiting for page to load...")
        page.wait_for_load_state('networkidle', timeout=30000)
        time.sleep(3)  # Additional wait for content to render
        
        # Extract listings using JavaScript
        log_info("Extracting listings from page...")
        listings_data = page.evaluate(r'''
            () => {
                const listings = [];
                
                // Debug: Log page structure
                console.log('Page title:', document.title);
                console.log('Page URL:', window.location.href);
                console.log('Body text preview:', document.body.textContent.substring(0, 200));
                
                // Try Buyee-specific selectors first
                const selectors = [
                    'li.itemCard',  // Buyee's actual listing container
                    'li[class*="itemCard"]',
                    'div.item-card',
                    'div.product-item',
                    'div.search-result-item',
                    'article.item',
                    'li.item',
                ];
                
                let items = [];
                for (const selector of selectors) {
                    const found = document.querySelectorAll(selector);
                    if (found.length > 0) {
                        console.log(`Found ${found.length} items with selector: ${selector}`);
                        items = Array.from(found);
                        break;
                    }
                }
                
                // If no items found, try to find any links that might be listings
                if (items.length === 0) {
                    // Try Buyee-specific patterns
                    const buyeeLinks = Array.from(document.querySelectorAll('a[href*="/item/"]'));
                    const mercariLinks = Array.from(document.querySelectorAll('a[href*="mercari"]'));
                    const yahooLinks = Array.from(document.querySelectorAll('a[href*="yahoo"]'));
                    
                    const allLinks = [...buyeeLinks, ...mercariLinks, ...yahooLinks];
                    if (allLinks.length > 0) {
                        console.log(`Found ${allLinks.length} item links (Buyee: ${buyeeLinks.length}, Mercari: ${mercariLinks.length}, Yahoo: ${yahooLinks.length})`);
                        items = allLinks.map(link => {
                            // Try to find the parent container - prioritize li.itemCard
                            let container = link.closest('li.itemCard') ||
                                          link.closest('li[class*="itemCard"]') ||
                                          link.closest('div[class*="item"]') || 
                                          link.closest('div[class*="card"]') ||
                                          link.closest('div[class*="product"]') ||
                                          link.closest('li') ||
                                          link.parentElement;
                            return container || link;
                        });
                    }
                }
                
                // Also try looking for images that might indicate listings
                if (items.length === 0) {
                    const productImages = Array.from(document.querySelectorAll('img[src*="item"], img[src*="product"], img[alt*="item" i]'));
                    if (productImages.length > 0) {
                        console.log(`Found ${productImages.length} product images`);
                        items = productImages.map(img => {
                            let container = img.closest('div[class*="item"]') || 
                                          img.closest('div[class*="card"]') ||
                                          img.closest('a')?.parentElement ||
                                          img.parentElement;
                            return container || img;
                        });
                    }
                }
                
                items.forEach((item, index) => {
                    const listing = {};
                    
                    // Extract title - use Buyee's specific selector first
                    const titleSelectors = [
                        '.itemCard__itemName',  // Buyee's actual title selector
                        '[class*="itemCard__itemName"]',
                        '.item-name',
                        'h2', 
                        'h3', 
                        '.title', 
                        '.item-title', 
                        '[class*="title"]'
                    ];
                    for (const sel of titleSelectors) {
                        const titleElem = item.querySelector(sel);
                        if (titleElem) {
                            const titleText = titleElem.textContent.trim();
                            // Skip generic titles like "Buyout Price", "Current Price", page titles
                            if (titleText && 
                                titleText !== 'Buyout Price' && 
                                titleText !== 'Current Price' &&
                                !titleText.includes('Buyee - Japanese Proxy Service') &&
                                titleText.length > 3) {
                                listing.title = titleText;
                                break;
                            }
                        }
                    }
                    if (!listing.title) {
                        const link = item.querySelector('a[href*="/item/"]');
                        if (link) {
                            const linkText = link.textContent.trim();
                            if (linkText && linkText.length > 3) {
                                listing.title = linkText;
                            }
                        }
                    }
                    
                    // Extract shop name from itemCard__storeName
                    const storeNameElem = item.querySelector('.itemCard__storeName, [class*="itemCard__storeName"]');
                    if (storeNameElem) {
                        const fontElem = storeNameElem.querySelector('font');
                        if (fontElem) {
                            const storeNameText = fontElem.textContent.trim();
                            // Map store name text to shop names
                            if (storeNameText === 'JDirectItems Auction') {
                                listing.shopName = 'Yahoo Japan Auctions';
                            } else if (storeNameText === 'Mercari') {
                                listing.shopName = 'Mercari';
                            } else if (storeNameText === 'Rakuten Rakuma') {
                                listing.shopName = 'Rakuma';
                            } else if (storeNameText === 'JDirectItems Fleamarket') {
                                listing.shopName = 'Yahoo Japan Fleamarket';
                            } else {
                                listing.shopName = storeNameText; // Fallback: use as-is
                            }
                        } else {
                            // Fallback: get text directly from storeName element
                            const storeNameText = storeNameElem.textContent.trim();
                            if (storeNameText === 'JDirectItems Auction') {
                                listing.shopName = 'Yahoo Japan Auctions';
                            } else if (storeNameText === 'Mercari') {
                                listing.shopName = 'Mercari';
                            } else if (storeNameText === 'Rakuten Rakuma') {
                                listing.shopName = 'Rakuma';
                            } else if (storeNameText === 'JDirectItems Fleamarket') {
                                listing.shopName = 'Yahoo Japan Fleamarket';
                            } else if (storeNameText) {
                                listing.shopName = storeNameText;
                            }
                        }
                    }
                    
                    // Extract price - different logic for Yahoo Japan Auctions vs other shops
                    if (listing.shopName === 'Yahoo Japan Auctions') {
                        // For Yahoo Japan Auctions, try to extract Buyout Price and Current Price separately
                        // Strategy: Look for text patterns and price elements
                        
                        // Get all text content from the item card
                        const itemText = item.textContent || '';
                        
                        // Try to find Buyout Price by looking for labels and nearby price values
                        const buyoutLabelPatterns = [
                            /Buyout\s+Price[:\s]*([^\n]+)/i,
                            /即決価格[:\s]*([^\n]+)/i,
                            /即決[:\s]*([^\n]+)/i
                        ];
                        
                        for (const pattern of buyoutLabelPatterns) {
                            const match = itemText.match(pattern);
                            if (match && match[1]) {
                                const buyoutText = match[1].trim();
                                // Extract price value - prioritize JPY (¥, 円) over other currencies
                                // First try to find JPY price
                                let priceMatch = buyoutText.match(/((?:¥|円)\s*[\d,]+\.?\d*)/);
                                if (!priceMatch) {
                                    // Fallback: try any currency
                                    priceMatch = buyoutText.match(/((?:¥|円|YEN|BRL|USD)?\s*[\d,]+\.?\d*\s*(?:¥|円|YEN|BRL|USD)?)/i);
                                }
                                if (priceMatch) {
                                    listing.buyoutPrice = priceMatch[1].trim();
                                    break;
                                }
                            }
                        }
                        
                        // If not found by pattern, try CSS selectors
                        if (!listing.buyoutPrice) {
                            const buyoutSelectors = [
                                '.itemCard__buyoutPrice',
                                '[class*="buyoutPrice"]',
                                '[class*="buyout-price"]',
                                '[class*="itemCard"][class*="buyout"]',
                                'div:has-text("Buyout Price")',
                                'div:has-text("即決価格")'
                            ];
                            for (const sel of buyoutSelectors) {
                                try {
                                    const buyoutElem = item.querySelector(sel);
                                    if (buyoutElem) {
                                        const buyoutText = buyoutElem.textContent.trim();
                                        // Clean up - remove label if present
                                        const cleaned = buyoutText.replace(/Buyout\s+Price[:\s]*/i, '').replace(/即決価格[:\s]*/i, '').trim();
                                        if (cleaned && cleaned.length > 0 && /\d/.test(cleaned)) {
                                            listing.buyoutPrice = cleaned;
                                            break;
                                        }
                                    }
                                } catch (e) {
                                    // Selector might not be supported (e.g., :has-text)
                                    continue;
                                }
                            }
                        }
                        
                        // Try to find Current Price
                        const currentLabelPatterns = [
                            /Current\s+Price[:\s]*([^\n]+)/i,
                            /現在価格[:\s]*([^\n]+)/i,
                            /入札価格[:\s]*([^\n]+)/i
                        ];
                        
                        for (const pattern of currentLabelPatterns) {
                            const match = itemText.match(pattern);
                            if (match && match[1]) {
                                const currentText = match[1].trim();
                                // Extract price value - prioritize JPY (¥, 円) over other currencies
                                // First try to find JPY price
                                let priceMatch = currentText.match(/((?:¥|円)\s*[\d,]+\.?\d*)/);
                                if (!priceMatch) {
                                    // Fallback: try any currency
                                    priceMatch = currentText.match(/((?:¥|円|YEN|BRL|USD)?\s*[\d,]+\.?\d*\s*(?:¥|円|YEN|BRL|USD)?)/i);
                                }
                                if (priceMatch) {
                                    listing.currentPrice = priceMatch[1].trim();
                                    break;
                                }
                            }
                        }
                        
                        // If not found by pattern, try CSS selectors
                        if (!listing.currentPrice) {
                            const currentSelectors = [
                                '.itemCard__currentPrice',
                                '[class*="currentPrice"]',
                                '[class*="current-price"]',
                                '[class*="itemCard"][class*="current"]',
                                'div:has-text("Current Price")',
                                'div:has-text("現在価格")'
                            ];
                            for (const sel of currentSelectors) {
                                try {
                                    const currentElem = item.querySelector(sel);
                                    if (currentElem) {
                                        const currentText = currentElem.textContent.trim();
                                        // Clean up - remove label if present
                                        const cleaned = currentText.replace(/Current\s+Price[:\s]*/i, '').replace(/現在価格[:\s]*/i, '').trim();
                                        if (cleaned && cleaned.length > 0 && /\d/.test(cleaned)) {
                                            listing.currentPrice = cleaned;
                                            break;
                                        }
                                    }
                                } catch (e) {
                                    continue;
                                }
                            }
                        }
                        
                        // Fallback: Look for any price elements and try to identify them
                        if (!listing.buyoutPrice || !listing.currentPrice) {
                            const allPriceElements = item.querySelectorAll('[class*="price"], [class*="Price"], .price, .Price');
                            for (const priceElem of allPriceElements) {
                                const priceText = priceElem.textContent.trim();
                                const parentText = priceElem.parentElement ? priceElem.parentElement.textContent : '';
                                
                                // Check if this is a buyout price
                                if (!listing.buyoutPrice && (parentText.includes('Buyout') || parentText.includes('即決'))) {
                                    const priceMatch = priceText.match(/((?:¥|円|YEN|BRL|USD)?\s*[\d,]+\.?\d*\s*(?:¥|円|YEN|BRL|USD)?)/i);
                                    if (priceMatch) {
                                        listing.buyoutPrice = priceMatch[1].trim();
                                    }
                                }
                                
                                // Check if this is a current price
                                if (!listing.currentPrice && (parentText.includes('Current') || parentText.includes('現在') || parentText.includes('入札'))) {
                                    const priceMatch = priceText.match(/((?:¥|円|YEN|BRL|USD)?\s*[\d,]+\.?\d*\s*(?:¥|円|YEN|BRL|USD)?)/i);
                                    if (priceMatch) {
                                        listing.currentPrice = priceMatch[1].trim();
                                    }
                                }
                            }
                        }
                    } else {
                        // For other shops, get general price
                        const priceSelectors = ['.price', '.item-price', '[class*="price"]'];
                        for (const sel of priceSelectors) {
                            const priceElem = item.querySelector(sel);
                            if (priceElem) {
                                listing.price = priceElem.textContent.trim();
                                break;
                            }
                        }
                    }
                    
                    // Extract image - filter out icons/badges and find the actual product thumbnail
                    const allImages = Array.from(item.querySelectorAll('img'));
                    let productImageUrl = '';
                    
                    // Filter out icons, badges, logos
                    const excludePatterns = ['icon_', 'icon.', 'badge', 'logo', 'common/icon', 'common/logo', 'spacer', '1x1'];
                    const productImagePatterns = ['mercdn.net', 'auctions.yahoo.co.jp', 'rakuten', 'item', 'product'];
                    
                    // First, try to find a product image (from known product image sources)
                    for (const img of allImages) {
                        const imgSrc = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '';
                        if (!imgSrc) continue;
                        
                        // Check if it's an icon/badge (exclude)
                        const isIcon = excludePatterns.some(pattern => imgSrc.toLowerCase().includes(pattern.toLowerCase()));
                        if (isIcon) continue;
                        
                        // Check if it's a product image (prefer)
                        const isProductImage = productImagePatterns.some(pattern => imgSrc.toLowerCase().includes(pattern.toLowerCase()));
                        if (isProductImage) {
                            productImageUrl = imgSrc;
                            break; // Found a product image, use it
                        }
                    }
                    
                    // If no product image found, try to find any non-icon image
                    if (!productImageUrl) {
                        for (const img of allImages) {
                            const imgSrc = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '';
                            if (!imgSrc) continue;
                            
                            // Skip icons/badges
                            const isIcon = excludePatterns.some(pattern => imgSrc.toLowerCase().includes(pattern.toLowerCase()));
                            if (!isIcon && imgSrc.startsWith('http')) {
                                productImageUrl = imgSrc;
                                break;
                            }
                        }
                    }
                    
                    listing.imageUrl = productImageUrl;
                    
                    // Extract URL - prioritize links to item pages
                    const link = item.querySelector('a[href*="/item/"]') || item.querySelector('a[href*="mercari"]') || item.querySelector('a[href*="yahoo"]') || item.querySelector('a');
                    if (link) {
                        let href = link.getAttribute('href');
                        if (href && !href.startsWith('http')) {
                            href = 'https://buyee.jp' + href;
                        }
                        // Only use valid item links (skip homepage)
                        if (href && href !== 'https://buyee.jp/' && (href.includes('/item/') || href.includes('mercari') || href.includes('yahoo'))) {
                            listing.href = href;
                        }
                    }
                    
                    if (listing.title || listing.href) {
                        listings.push(listing);
                    }
                });
                
                return {
                    count: listings.length,
                    listings: listings,
                    debug: {
                        totalDivs: document.querySelectorAll('div').length,
                        totalLinks: document.querySelectorAll('a').length,
                        totalImages: document.querySelectorAll('img').length,
                        pageTitle: document.title,
                        pageUrl: window.location.href,
                        bodyText: document.body.textContent.substring(0, 500),
                        hasErrorText: document.body.textContent.toLowerCase().includes('error') || 
                                     document.body.textContent.toLowerCase().includes('not found'),
                        itemLinks: document.querySelectorAll('a[href*="/item/"]').length,
                        mercariLinks: document.querySelectorAll('a[href*="mercari"]').length,
                        yahooLinks: document.querySelectorAll('a[href*="yahoo"]').length
                    }
                };
            }
        ''')
        
        listings = listings_data.get('listings', [])
        count = listings_data.get('count', 0)
        
        log_info(f"  Found {count} listings")
        if listings_data.get('debug'):
            debug = listings_data['debug']
            log_debug("  Debug Info:")
            log_debug(f"    - Page Title: {debug.get('pageTitle', 'N/A')}")
            log_debug(f"    - Page URL: {debug.get('pageUrl', 'N/A')}")
            log_debug(f"    - Total divs: {debug.get('totalDivs', 0)}")
            log_debug(f"    - Total links: {debug.get('totalLinks', 0)}")
            log_debug(f"    - Total images: {debug.get('totalImages', 0)}")
            log_debug(f"    - Item links: {debug.get('itemLinks', 0)}")
            log_debug(f"    - Mercari links: {debug.get('mercariLinks', 0)}")
            log_debug(f"    - Yahoo links: {debug.get('yahooLinks', 0)}")
            log_debug(f"    - Has error text: {debug.get('hasErrorText', False)}")
            if debug.get('bodyText'):
                log_debug(f"    - Body text preview: {debug['bodyText'][:200]}...")
        
        # Convert to our format and validate
        all_listings = []
        invalid_count = 0
        for item in listings:
            href = item.get('href', '')
            if not href.startswith('http'):
                href = BASE_URL + href if href.startswith('/') else BASE_URL + '/' + href
            
            title = item.get('title', '')
            # Translate title to English if it contains Japanese (fallback if Buyee didn't translate)
            if title and contains_japanese(title):
                try:
                    title = translate_japanese(title)
                except Exception as e:
                    print(f"  Translation warning for title: {e}")
            
            shop_name = item.get('shopName', '')
            # Map shop names if needed (fallback in case JavaScript didn't map)
            if shop_name == 'JDirectItems Auction':
                shop_name = 'Yahoo Japan Auctions'
            elif shop_name == 'Rakuten Rakuma':
                shop_name = 'Rakuma'
            elif shop_name == 'JDirectItems Fleamarket':
                shop_name = 'Yahoo Japan Fleamarket'
            
            # Extract listing ID from URL
            listing_id = extract_listing_id(href)
            
            # Build listing data with shop-specific price fields
            listing_data = {
                'title': title,
                'image_url': item.get('imageUrl', ''),
                'listing_url': href,
                'listing_id': listing_id,
                'shop_name': shop_name if shop_name else None,
            }
            
            # Add price fields based on shop
            if shop_name == 'Yahoo Japan Auctions':
                listing_data['buyout_price'] = item.get('buyoutPrice', '')
                listing_data['current_price'] = item.get('currentPrice', '')
            else:
                listing_data['price'] = item.get('price', '')
            
            # Validate listing
            is_valid, errors = validate_search_result(listing_data)
            if is_valid:
                all_listings.append(listing_data)
            else:
                invalid_count += 1
                if errors:
                    log_warning(f"Invalid listing skipped: {errors[0]}")
        
        if invalid_count > 0:
            log_warning(f"Skipped {invalid_count} invalid listings")
        
        # Get HTML for inspection
        html_content = page.content()
        
        # Check for pagination (next page)
        has_next_page = False
        next_page_url = None
        
        if PAGINATION_ENABLED:
            # Try to find next page link/button
            # First, look for Buyee's pagination container: <div class="page_navi">
            try:
                # Use JavaScript to find next page link within page_navi
                current_url = page.url
                current_page = 1
                
                # Get current page number from URL
                if 'page=' in current_url:
                    try:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(current_url)
                        params = parse_qs(parsed.query)
                        if 'page' in params:
                            current_page = int(params['page'][0])
                    except:
                        pass
                
                navi_result = page.evaluate(f'''
                    (currentPage) => {{
                        const pageNavi = document.querySelector('div.page_navi, div[class*="page_navi"]');
                        if (!pageNavi) return null;
                        
                        // Look for next page link - check all links and find one with "next" text or class
                        const allLinks = Array.from(pageNavi.querySelectorAll('a'));
                        
                        // First, try to find a link with "next" text or class
                        for (const link of allLinks) {{
                            const text = link.textContent.trim().toLowerCase();
                            const className = link.className || '';
                            const href = link.getAttribute('href');
                            
                            if (!href) continue;
                            
                            // Check if it looks like a next page link
                            const isNextLink = text === '次へ' || 
                                             text === 'next' ||
                                             className.toLowerCase().includes('next') ||
                                             (link.getAttribute('aria-label') || '').toLowerCase().includes('next');
                            
                            if (isNextLink) {{
                                const isDisabled = link.hasAttribute('disabled') ||
                                                 link.classList.contains('disabled') ||
                                                 link.getAttribute('aria-disabled') === 'true';
                                
                                if (!isDisabled) {{
                                    return href;
                                }}
                            }}
                        }}
                        
                        // Fallback: find link that goes to current_page + 1
                        const nextPageNum = currentPage + 1;
                        for (const link of allLinks) {{
                            const href = link.getAttribute('href');
                            if (!href) continue;
                            
                            // Extract page number from href
                            const pageMatch = href.match(/[?&]page=(\\d+)/);
                            if (pageMatch) {{
                                const pageNum = parseInt(pageMatch[1]);
                                if (pageNum === nextPageNum) {{
                                    const isDisabled = link.hasAttribute('disabled') ||
                                                     link.classList.contains('disabled') ||
                                                     link.getAttribute('aria-disabled') === 'true';
                                    
                                    if (!isDisabled) {{
                                        return href;
                                    }}
                                }}
                            }}
                        }}
                        
                        return null;
                    }}
                ''', current_page)
                
                if navi_result:
                    href = navi_result
                    if not href.startswith('http'):
                        href = BASE_URL + href if href.startswith('/') else BASE_URL + '/' + href
                    next_page_url = href
                    has_next_page = True
                    log_info(f"  Found next page in page_navi: {next_page_url}")
            except Exception as e:
                log_warning(f"  Error checking page_navi: {e}")
            
            # Fallback: Try original selectors (outside page_navi)
            if not has_next_page:
                next_page_selectors = [
                    'a[class*="next"]',
                    'a[class*="pagination"]',
                    'button[class*="next"]',
                    'a:has-text("Next")',
                    'a:has-text("次へ")',
                    'a[aria-label*="next" i]',
                    'a[aria-label*="Next" i]',
                ]
                
                for selector in next_page_selectors:
                    try:
                        next_elem = page.query_selector(selector)
                        if next_elem:
                            # Check if it's enabled (not disabled)
                            is_disabled = next_elem.get_attribute('disabled') or \
                                         'disabled' in (next_elem.get_attribute('class') or '') or \
                                         'disabled' in (next_elem.get_attribute('aria-disabled') or '')
                            
                            if not is_disabled:
                                href = next_elem.get_attribute('href')
                                if href:
                                    if not href.startswith('http'):
                                        href = BASE_URL + href if href.startswith('/') else BASE_URL + '/' + href
                                    next_page_url = href
                                    has_next_page = True
                                    log_info(f"  Found next page: {next_page_url}")
                                    break
                    except:
                        continue
            
            # Don't use fallback URL construction - only use actual next page links from page_navi
            # This prevents blindly incrementing page numbers for pages that don't exist
        
        # Return all listings, HTML, count, and pagination info
        return all_listings, html_content, count, all_listings, has_next_page, next_page_url
        
    except Exception as e:
        log_error(f"Error extracting listing data: {e}")
        import traceback
        if LOG_ENABLED:
            logging.exception("Full traceback:")
        traceback.print_exc()
        return [], page.content(), 0, [], False, None

def scrape_listing_details(page, listing_url):
    """Phase 2: Scrape detailed information from a single listing's detail page
    
    Extracts additional fields not available in search results:
    
    Common fields (all shops):
    - Description (Item Explanation)
    - Seller Info
    - Shipping Info
    - Status (sold/available)
    - All product images
    
    Yahoo Japan Auctions-specific fields:
    - Buyout Price (more accurate than search results)
    - Current Price (more accurate than search results)
    - Item Condition
    - Number of Bids
    - Closing Time (JST)
    
    Note: Also re-extracts shop_name, listing_id, and title from detail page
    (these may be more complete/accurate than search results)
    """
    from bs4 import BeautifulSoup
    import re
    
    try:
        log_info(f"  Navigating to: {listing_url}")
        page.goto(listing_url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)  # Wait for page to fully load
        
        # Wait for itemDescription section to load (which contains the iframe)
        try:
            page.wait_for_selector('section#itemDescription, #itemDescription, [id="itemDescription"]', timeout=10000)
        except:
            # Try scrolling to trigger lazy loading
            try:
                page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
                time.sleep(2)
                page.wait_for_selector('section#itemDescription, #itemDescription, [id="itemDescription"]', timeout=5000)
            except:
                pass  # Continue if not found
        
        # Use JavaScript to extract images (more reliable for dynamic content)
        images_js = page.evaluate(r'''
            () => {
                const images = [];
                document.querySelectorAll('img').forEach(img => {
                    const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src');
                    if (src) {
                        // Filter for product images (exclude logos, icons, tracking pixels)
                        if (src.includes('auctions.yahoo.co.jp') || 
                            src.includes('cdnyauction.buyee.jp') ||
                            src.includes('mercdn.net') ||
                            (src.includes('buyee') && !src.includes('common/icon') && 
                             !src.includes('common/logo') && !src.includes('common/spacer'))) {
                            images.push(src);
                        }
                    }
                });
                return [...new Set(images)];
            }
        ''')
        
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style tags to get cleaner text
        for script in soup(['script', 'style', 'noscript']):
            script.decompose()
        
        detail = {}
        full_text = soup.get_text()
        
        # Extract Shop name from store-name div
        shop_name = None
        shop_selectors = [
            'div.store-name.yauc.store-name--jdiaution',
            'div.store-name.mercari',
            'div.store-name.rakuma',
            'div.store-name.jdifleamarket',
            'div[class*="store-name"]'
        ]
        
        for selector in shop_selectors:
            shop_elem = soup.select_one(selector)
            if shop_elem:
                classes = shop_elem.get('class', [])
                class_str = ' '.join(classes) if classes else ''
                
                # Map classes to shop names
                if 'yauc' in class_str and 'jdiaution' in class_str:
                    shop_name = 'Yahoo Japan Auctions'
                    break
                elif 'mercari' in class_str:
                    shop_name = 'Mercari'
                    break
                elif 'rakuma' in class_str:
                    shop_name = 'Rakuma'
                    break
                elif 'jdifleamarket' in class_str:
                    shop_name = 'Yahoo Japan Fleamarket'
                    break
        
        # Fallback: Try JavaScript extraction if not found in HTML
        if not shop_name:
            shop_result = page.evaluate(r'''
                () => {
                    const shopDiv = document.querySelector('div.store-name');
                    if (shopDiv) {
                        const classes = shopDiv.className;
                        if (classes.includes('yauc') && classes.includes('jdiaution')) {
                            return 'Yahoo Japan Auctions';
                        } else if (classes.includes('mercari')) {
                            return 'Mercari';
                        } else if (classes.includes('rakuma')) {
                            return 'Rakuma';
                        } else if (classes.includes('jdifleamarket')) {
                            return 'Yahoo Japan Fleamarket';
                        }
                    }
                    return null;
                }
            ''')
            if shop_result:
                shop_name = shop_result
        
        if shop_name:
            detail['shop_name'] = shop_name
            log_info(f"    Shop detected: {shop_name}")
        else:
            detail['shop_name'] = 'Unknown'
            log_warning("Could not detect shop name")
        
        # Extract listing ID from URL
        listing_id = extract_listing_id(listing_url)
        if listing_id:
            detail['listing_id'] = listing_id
            log_info(f"    Listing ID: {listing_id}")
        
        # Extract title (item name)
        title_text = None
        title_selectors = [
            'h1',
            '.item-title',
            '.itemTitle',
            '[class*="itemTitle"]',
            '[class*="item-title"]',
            'title'
        ]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                if title_text and len(title_text) > 5 and title_text != 'Buyee':
                    break
        # Also try regex patterns for Japanese titles
        if not title_text or len(title_text) < 5:
            title_patterns = [
                r'商品名[：:\s]+\n?([^\n]{10,200})',
                r'商品[：:\s]+\n?([^\n]{10,200})',
            ]
            for pattern in title_patterns:
                match = re.search(pattern, full_text)
                if match:
                    title_text = match.group(1).strip()
                    if len(title_text) > 5:
                        break
        
        if title_text and len(title_text) > 5:
            title_text = title_text[:500]  # Limit length
            detail['title'] = title_text
            # Translate to English if contains Japanese
            if contains_japanese(title_text):
                try:
                    detail['title'] = translate_japanese(title_text)
                except Exception as e:
                    log_warning(f"    Translation error for title: {e}")
                    detail['title'] = title_text
        
        # Extract description from section#item-description (Buyee's specific container)
        # Description is inside an iframe, which is inside section#itemDescription
        description_text = None
        
        # Find section#itemDescription first, then get its iframe
        try:
            # Wait for itemDescription section to load
            try:
                page.wait_for_selector('section#itemDescription, #itemDescription, [id="itemDescription"]', timeout=10000)
            except:
                pass
            
            # Try to find section#itemDescription and get its iframe
            item_desc_section = (page.query_selector('section#itemDescription') or 
                               page.query_selector('#itemDescription') or
                               page.query_selector('[id="itemDescription"]'))
            
            if item_desc_section:
                # Find iframe inside this section
                iframe = item_desc_section.query_selector('iframe')
                if iframe:
                    # Get the iframe frame object
                    iframe_frame = iframe.content_frame()
                    if iframe_frame:
                        # Wait a bit for iframe content to load
                        time.sleep(2)
                        
                        # Try to find section#item-description inside the iframe
                        try:
                            iframe_frame.wait_for_selector('section#item-description, #item-description', timeout=10000)
                        except:
                            pass
                        
                        # Extract description from iframe
                        desc_result = iframe_frame.evaluate('''
                            () => {
                                const selectors = [
                                    'section#item-description',
                                    '#item-description',
                                    'section[id="item-description"]',
                                    '[id="item-description"]'
                                ];
                                
                                for (const selector of selectors) {
                                    const desc_section = document.querySelector(selector);
                                    if (desc_section) {
                                        const clone = desc_section.cloneNode(true);
                                        clone.querySelectorAll('script, style, iframe').forEach(el => el.remove());
                                        const text = clone.textContent.trim();
                                        
                                        // Skip generic Buyee text
                                        if (text && 
                                            !text.includes('Buyee is an official partner') &&
                                            !text.includes('function') &&
                                            text.length > 50) {
                                            return text;
                                        }
                                    }
                                }
                                return null;
                            }
                        ''')
                        
                        if desc_result and len(desc_result) > 50:
                            description_text = ' '.join(desc_result.split())
            else:
                log_warning("No iframe found inside section#itemDescription")
        except Exception as e:
            log_warning(f"Could not access iframe for description: {e}")
        
        # Fallback: Try to find in main page if not found in iframe
        if not description_text:
            desc_result = page.evaluate(r'''
                () => {
                    const selectors = [
                        'section#item-description',
                        '#item-description',
                        'section[id="item-description"]',
                        '[id="item-description"]'
                    ];
                    
                    for (const selector of selectors) {
                        const desc_section = document.querySelector(selector);
                        if (desc_section) {
                            const clone = desc_section.cloneNode(true);
                            clone.querySelectorAll('script, style, iframe').forEach(el => el.remove());
                            const text = clone.textContent.trim();
                            
                            if (text && 
                                !text.includes('Buyee is an official partner') &&
                                !text.includes('function') &&
                                text.length > 50) {
                                return text;
                            }
                        }
                    }
                    return null;
                }
            ''')
            
            if desc_result and len(desc_result) > 50:
                description_text = ' '.join(desc_result.split())
        
        # Fallback: Try regex patterns on cleaned text
        if not description_text:
            desc_patterns = [
                r'Item Explanation[：:\s]+\n?([^\n]{50,2000})',  # Item Explanation (English)
                r'商品説明[：:\s]+\n?([^\n]{50,2000})',  # 商品説明 followed by text
                r'商品の説明[：:\s]+\n?([^\n]{50,2000})',  # 商品の説明
                r'説明[：:\s]+\n?([^\n]{50,2000})',  # 説明
                r'Description[：:\s]+\n?([^\n]{50,2000})',  # Description (English)
            ]
            
            for pattern in desc_patterns:
                match = re.search(pattern, full_text, re.DOTALL)
                if match:
                    candidate = match.group(1).strip()
                    # Filter out script-like content and generic Buyee text
                    if not re.search(r'(function|var |const |let |script|gtm\.|dataLayer|Buyee is an official partner)', candidate, re.I):
                        if len(candidate) > 50:  # Meaningful length
                            description_text = candidate
                            break
        
        # Strategy 3: Try to find description in structured elements
        if not description_text:
            desc_headings = soup.find_all(string=re.compile(r'Item Explanation|商品説明|商品の説明|Description', re.I))
            for heading in desc_headings[:2]:  # Check first 2
                parent = heading.find_parent()
                if parent:
                    # Look for next siblings or children with actual description
                    text_parts = []
                    current = parent
                    for i in range(5):
                        current = current.next_sibling if hasattr(current, 'next_sibling') else None
                        if current and hasattr(current, 'get_text'):
                            text = current.get_text(strip=True)
                            if text and len(text) > 50 and not text.startswith('Buyee is an official'):
                                if not re.search(r'(function|var |const |gtm\.)', text, re.I):
                                    text_parts.append(text)
                                    if len(' '.join(text_parts)) > 100:
                                        break
                    if text_parts:
                        description_text = ' '.join(text_parts)
                        break
        
        if description_text:
            # Clean up description
            description_text = ' '.join(description_text.split())
            if len(description_text) > 2000:
                description_text = description_text[:2000] + '...'
            # Translate to English if contains Japanese
            if contains_japanese(description_text):
                try:
                    detail['description'] = translate_japanese(description_text[:1500])  # Limit for translation
                except Exception as e:
                    log_warning(f"    Translation error for description: {e}")
                    detail['description'] = description_text
            else:
                detail['description'] = description_text
        
        # Extract shop-specific fields only for Yahoo Japan Auctions
        if shop_name == 'Yahoo Japan Auctions':
            # Extract Buyout Price (即決価格)
            buyout_price = None
            # Prioritize JPY (¥, 円) prices - try JPY patterns first
            jpy_patterns = [
                r'Buyout Price[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
                r'即決価格[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
                r'Buyout[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
            ]
            for pattern in jpy_patterns:
                match = re.search(pattern, full_text, re.I)
                if match:
                    buyout_price = match.group(1).strip()
                    if buyout_price and re.search(r'\d', buyout_price):
                        break
            
            # Fallback: try other currencies if JPY not found
            if not buyout_price:
                buyout_patterns = [
                    r'Buyout Price[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'即決価格[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'Buyout[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'Buyout Price[^\d]*([\d,]+\.?\d*)\s*(?:¥|円|YEN|BRL|USD)',
                    r'即決価格[^\d]*([\d,]+\.?\d*)\s*(?:¥|円|YEN|BRL|USD)',
                ]
                for pattern in buyout_patterns:
                    match = re.search(pattern, full_text, re.I)
                    if match:
                        buyout_price = match.group(1).strip()
                        if buyout_price and re.search(r'\d', buyout_price):
                            break
            
            # Extract Current Price (現在価格/入札価格)
            current_price = None
            # Prioritize JPY (¥, 円) prices - try JPY patterns first
            jpy_patterns = [
                r'Current Price[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
                r'現在価格[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
                r'入札価格[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
                r'Current[^\d]*((?:¥|円)\s*[\d,]+\.?\d*)',
            ]
            for pattern in jpy_patterns:
                match = re.search(pattern, full_text, re.I)
                if match:
                    current_price = match.group(1).strip()
                    if current_price and re.search(r'\d', current_price):
                        break
            
            # Fallback: try other currencies if JPY not found
            if not current_price:
                current_patterns = [
                    r'Current Price[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'現在価格[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'入札価格[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'Current[^\d]*((?:¥|円|YEN|BRL|USD)\s*[\d,]+\.?\d*)',
                    r'Current Price[^\d]*([\d,]+\.?\d*)\s*(?:¥|円|YEN|BRL|USD)',
                    r'現在価格[^\d]*([\d,]+\.?\d*)\s*(?:¥|円|YEN|BRL|USD)',
                ]
                for pattern in current_patterns:
                    match = re.search(pattern, full_text, re.I)
                    if match:
                        current_price = match.group(1).strip()
                        if current_price and re.search(r'\d', current_price):
                            break
            
            # Store prices separately
            if buyout_price:
                detail['buyout_price'] = buyout_price[:100]
            if current_price:
                detail['current_price'] = current_price[:100]
            
            # Extract condition, number of bids, and closing time from section#itemDetail_sec
            # They are in a table structure: itemDetail__listName (label) and itemDetail__listValue (value)
            condition_text = None
            bids_text = None
            closing_time = None
            
            # Use JavaScript to extract from itemDetail_sec section
            detail_info = page.evaluate(r'''
                () => {
                    const detail_sec = document.querySelector('section#itemDetail_sec') || 
                                      document.querySelector('#itemDetail_sec') ||
                                      document.querySelector('[id="itemDetail_sec"]');
                    
                    if (!detail_sec) {
                        return { found: false };
                    }
                    
                    const result = { found: true, condition: null, bids: null, closing_time: null };
                    
                    // Find all listName divs
                    const listNames = detail_sec.querySelectorAll('.itemDetail__listName, [class*="itemDetail__listName"]');
                    
                    for (const listName of listNames) {
                        const nameText = listName.textContent.trim();
                        
                        // Find the corresponding listValue (next sibling or parent's next sibling)
                        let listValue = listName.nextElementSibling;
                        if (!listValue || !listValue.classList.contains('itemDetail__listValue')) {
                            // Try parent's next sibling
                            const parent = listName.parentElement;
                            if (parent) {
                                listValue = parent.nextElementSibling;
                                if (listValue) {
                                    listValue = listValue.querySelector('.itemDetail__listValue, [class*="itemDetail__listValue"]');
                                }
                            }
                        }
                        
                        if (listValue && listValue.classList.contains('itemDetail__listValue')) {
                            const valueText = listValue.textContent.trim();
                            
                            // Check for Item Condition
                            if (nameText.includes('Item Condition') || nameText.includes('Condition') || 
                                nameText.includes('状態') || nameText.includes('コンディション')) {
                                result.condition = valueText;
                            }
                            // Check for Number of Bids
                            else if (nameText.includes('Number of Bids') || nameText.includes('Bids') || 
                                     nameText.includes('入札数')) {
                                result.bids = valueText;
                            }
                            // Check for Closing Time
                            else if (nameText.includes('Closing Time') || nameText.includes('End Time') || 
                                     nameText.includes('終了時刻') || nameText.includes('終了時間')) {
                                result.closing_time = valueText;
                            }
                        }
                    }
                    
                    return result;
                }
            ''')
            
            if detail_info.get('found'):
                condition_text = detail_info.get('condition')
                bids_text = detail_info.get('bids')
                closing_time = detail_info.get('closing_time')
            
            # Fallback: Try regex patterns if not found in structured format
            if not condition_text:
                condition_patterns = [
                    r'状態[：:]\s*([^\n]+)',
                    r'コンディション[：:]\s*([^\n]+)',
                    r'ランク[：:]\s*([^\n]+)',
                    r'condition[：:]\s*([^\n]+)',
                    r'Condition[：:]\s*([^\n]+)',
                ]
                for pattern in condition_patterns:
                    match = re.search(pattern, full_text, re.I)
                    if match:
                        condition_text = match.group(1).strip()
                        break
            
            if condition_text:
                condition_text = condition_text[:200]
                # Translate to English if contains Japanese
                if contains_japanese(condition_text):
                    try:
                        detail['condition'] = translate_japanese(condition_text)
                    except Exception as e:
                        log_warning(f"    Translation error for condition: {e}")
                        detail['condition'] = condition_text
                else:
                    detail['condition'] = condition_text
        
        # Check if sold/available
        if re.search(r'売り切れ|sold out|この商品は売り切れ|終了', full_text, re.I):
            detail['status'] = 'sold'
        elif re.search(r'販売中|available|在庫あり|入札中', full_text, re.I):
            detail['status'] = 'available'
        
        # Extract seller information
        seller_text = None
        seller_patterns = [
            r'出品者[：:]\s*([^\n]+)',
            r'seller[：:]\s*([^\n]+)',
            r'Seller[：:]\s*([^\n]+)',
        ]
        for pattern in seller_patterns:
            match = re.search(pattern, full_text, re.I)
            if match:
                seller_text = match.group(1).strip()[:200]
                break
        if seller_text:
            seller_text = seller_text[:200]
            # Translate to English if contains Japanese
            if contains_japanese(seller_text):
                try:
                    detail['seller_info'] = translate_japanese(seller_text)
                except Exception as e:
                    log_warning(f"    Translation error for seller_info: {e}")
                    detail['seller_info'] = seller_text
            else:
                detail['seller_info'] = seller_text
        
        # Extract shipping information
        shipping_text = None
        shipping_patterns = [
            r'送料[：:]\s*([^\n]+)',
            r'shipping[：:]\s*([^\n]+)',
            r'Shipping[：:]\s*([^\n]+)',
        ]
        for pattern in shipping_patterns:
            match = re.search(pattern, full_text, re.I)
            if match:
                shipping_text = match.group(1).strip()[:200]
                break
        if shipping_text:
            shipping_text = shipping_text[:200]
            # Translate to English if contains Japanese
            if contains_japanese(shipping_text):
                try:
                    detail['shipping_info'] = translate_japanese(shipping_text)
                except Exception as e:
                    log_warning(f"    Translation error for shipping_info: {e}")
                    detail['shipping_info'] = shipping_text
            else:
                detail['shipping_info'] = shipping_text
        
        # Extract ALL images using JavaScript result (filtered for product images)
        image_urls = []
        seen_urls = set()
        
        for src in images_js:
            if not src.startswith('http'):
                src = 'https:' + src if src.startswith('//') else BASE_URL + src
            url_key = src.split('?')[0]
            if url_key not in seen_urls:
                seen_urls.add(url_key)
                image_urls.append(src)
        
        # Fallback: Also check HTML for any missed product images
        for img in soup.find_all('img'):
            src = img.get('src', '') or img.get('data-src', '') or img.get('data-lazy-src', '')
            if src and ('auctions.yahoo.co.jp' in src or 'mercdn.net' in src or 
                       ('buyee' in src and 'common/icon' not in src and 'common/logo' not in src)):
                if not src.startswith('http'):
                    src = 'https:' + src if src.startswith('//') else BASE_URL + src
                url_key = src.split('?')[0]
                if url_key not in seen_urls:
                    seen_urls.add(url_key)
                    image_urls.append(src)
        
        if image_urls:
            detail['all_images'] = image_urls
        
            # Number of bids and closing time are already extracted above from itemDetail_sec
            # Just store them if found (only for Yahoo Japan Auctions)
            if bids_text:
                detail['number_of_bids'] = bids_text.strip()
            else:
                # Fallback: Try regex patterns
                bids_patterns = [
                    r'Number of Bids[：:\s]*(\d+)',
                    r'入札数[：:\s]*(\d+)',
                    r'Bids[：:\s]*(\d+)',
                    r'(\d+)\s*bids?',
                    r'(\d+)\s*入札',
                ]
                for pattern in bids_patterns:
                    match = re.search(pattern, full_text, re.I)
                    if match:
                        bids_text = match.group(1).strip()
                        detail['number_of_bids'] = bids_text
                        break
            
            if closing_time:
                # Clean up the time string
                closing_time = ' '.join(closing_time.split())
                detail['closing_time_jst'] = closing_time[:200]
            else:
                # Fallback: Try regex patterns
                closing_patterns = [
                    r'Closing Time[：:\s]*([^\n]+JST[^\n]*)',
                    r'End Time[：:\s]*([^\n]+JST[^\n]*)',
                    r'終了時刻[：:\s]*([^\n]+)',
                    r'Closing[：:\s]*([^\n]+)',
                    r'Ends[：:\s]*([^\n]+)',
                ]
                for pattern in closing_patterns:
                    match = re.search(pattern, full_text, re.I)
                    if match:
                        closing_time = match.group(1).strip()
                        closing_time = ' '.join(closing_time.split())
                        if closing_time:
                            detail['closing_time_jst'] = closing_time[:200]
                            break
        
        # Validate detail data
        shop_name = detail.get('shop_name', 'Unknown')
        is_valid, errors = validate_listing_details(detail, shop_name)
        if errors:
            log_warning(f"Validation warnings: {', '.join(errors[:2])}")  # Show first 2 warnings
        
        return detail
    except Exception as e:
        log_error(f"Error extracting detail: {e}")
        import traceback
        if LOG_ENABLED:
            logging.exception("Full traceback:")
        traceback.print_exc()
        return {}

def parse_arguments():
    """Parse command-line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Buyee Scraper - Scrape listings from Buyee.jp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default search term
  python test_buyee_playwright.py
  
  # Specify search term
  python test_buyee_playwright.py --search "Nikon FM2"
  
  # Short form
  python test_buyee_playwright.py -s "Canon AE-1"
  
  # For website integration, pass search_term as parameter to main()
        """
    )
    
    parser.add_argument(
        '-s', '--search',
        dest='search_term',
        type=str,
        default=DEFAULT_SEARCH_TERM,
        help=f'Search term to use (default: "{DEFAULT_SEARCH_TERM}")'
    )
    
    return parser.parse_args()

def main(search_term=None):
    """Main scraping function
    
    Args:
        search_term (str, optional): Search term to use. If None, uses DEFAULT_SEARCH_TERM.
                                     This allows the function to be called programmatically
                                     (e.g., from a website) or from command line.
    
    Returns:
        dict: Results dictionary with scraping results
    """
    # Use provided search_term, or default
    if search_term is None:
        search_term = DEFAULT_SEARCH_TERM
    
    # Setup logging first
    log_filepath = setup_logging()
    
    if not PLAYWRIGHT_AVAILABLE:
        log_error("Playwright is not available. Please install it first.")
        log_error("Install with: pip install playwright")
        log_error("Then run: playwright install chromium")
        return {'error': 'Playwright not available'}
    
    log_info("=" * 60)
    log_info("Buyee Scraping Test - Playwright Version")
    log_info("=" * 60)
    log_info(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_info(f"Search Term: {search_term}")
    if log_filepath:
        log_info(f"Log file: {log_filepath}")
    log_info("")
    
    results = {
        'test_date': datetime.now().isoformat(),
        'search_term': search_term,
        'access_test': False,
        'search_test': False,
        'extraction_test': False,
        'listings_found': 0,
        'challenges': [],
        'notes': [],
        'sample_data': []
    }
    
    search_url = f"{BASE_URL}/item/crosssearch/query/{quote_plus(search_term)}?conversionType=top_page_search&suggest=1"
    
    with sync_playwright() as p:
        log_info("Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='ja-JP',  # Japanese locale to try to get JPY prices
            timezone_id='Asia/Tokyo',
            extra_http_headers={
                'Accept-Language': 'ja,ja-JP;q=0.9,en;q=0.8'  # Japanese language preference
            }
        )
        page = context.new_page()
        
        try:
            # Test 1: Navigate to homepage first
            log_info(f"Navigating to homepage: {BASE_URL}")
            page.goto(BASE_URL, wait_until='domcontentloaded', timeout=60000)
            time.sleep(2)  # Wait for page to fully load
            results['access_test'] = True
            log_success("Homepage loaded successfully")
            
            # Check if we can find a search form
            log_info("\nLooking for search form...")
            search_form_found = False
            search_input = None
            
            # Try multiple search input selectors
            search_selectors = [
                'input[name="keyword"]',
                'input[type="search"]',
                'input[placeholder*="search" i]',
                'input[id*="search" i]',
                'input[class*="search" i]',
                '#search-keyword',
                '.search-keyword',
                'input[type="text"]'
            ]
            
            for selector in search_selectors:
                try:
                    search_input = page.query_selector(selector)
                    if search_input:
                        log_info(f"  Found search input with selector: {selector}")
                        search_form_found = True
                        break
                except:
                    continue
            
            if search_form_found and search_input:
                # Try to interact with search form
                log_info(f"  Entering search term: {search_term}")
                search_input.fill(search_term)
                time.sleep(1)
                
                # Try to find and click search button
                search_button_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Search")',
                    'button:has-text("検索")',
                    '.search-button',
                    '#search-button'
                ]
                
                search_clicked = False
                for btn_selector in search_button_selectors:
                    try:
                        search_btn = page.query_selector(btn_selector)
                        if search_btn:
                            log_info(f"  Found search button with selector: {btn_selector}")
                            search_btn.click()
                            search_clicked = True
                            break
                    except:
                        continue
                
                if not search_clicked:
                    # Try pressing Enter
                    log_info("  Pressing Enter to submit search...")
                    search_input.press('Enter')
                
                # Wait for navigation
                page.wait_for_load_state('networkidle', timeout=30000)
                time.sleep(3)
                log_success("Search submitted")
            else:
                # Fallback: Try direct URL
                log_info(f"\nSearch form not found, trying direct URL: {search_url}")
                page.goto(search_url, wait_until='domcontentloaded', timeout=60000)
                time.sleep(3)
            
            # Check if we're on an error page
            page_title = page.title()
            page_url = page.url
            log_info(f"\nCurrent page title: {page_title}")
            log_info(f"Current page URL: {page_url}")
            
            if 'error' in page_title.lower() or '/errors' in page_url:
                results['challenges'].append("Search URL redirects to error page")
                results['notes'].append(f"Page title: {page_title}")
                results['notes'].append(f"Page URL: {page_url}")
                log_warning("Page appears to be an error page")
                # Still try to extract data in case there's content
            
            results['search_test'] = True
            
            # Phase 1: Scrape search results with pagination
            log_info("\nPhase 1: Scraping search results...")
            all_listings_combined = []
            page_number = 1
            total_count_all_pages = 0
            
            while True:
                log_info(f"\n--- Page {page_number} ---")
                listings, html_content, total_count, all_listings, has_next_page, next_page_url = scrape_search_results(page)
                
                log_info(f"  Found {total_count} listings on page {page_number}")
                all_listings_combined.extend(all_listings)
                total_count_all_pages += total_count
                
                # Check if we should continue pagination
                if not PAGINATION_ENABLED:
                    break
                
                if not has_next_page or not next_page_url:
                    log_info("  No more pages available")
                    break
                
                if PAGINATION_MAX_PAGES and page_number >= PAGINATION_MAX_PAGES:
                    log_info(f"  Reached maximum page limit ({PAGINATION_MAX_PAGES})")
                    break
                
                # Navigate to next page
                log_info("  Navigating to next page...")
                time.sleep(PAGINATION_DELAY_BETWEEN_PAGES)
                try:
                    page.goto(next_page_url, wait_until='domcontentloaded', timeout=60000)
                    time.sleep(3)  # Wait for page to load
                    page_number += 1
                except Exception as e:
                    log_warning(f"Error navigating to next page: {e}")
                    break
            
            log_info(f"\n{'='*60}")
            log_info(f"TOTAL LISTINGS FOUND (all pages): {len(all_listings_combined)}")
            log_info(f"Pages scraped: {page_number}")
            log_info(f"{'='*60}\n")
            
            results['total_listings_count'] = total_count_all_pages
            results['pages_scraped'] = page_number
            results['all_listings_basic'] = all_listings_combined
            
            # FUTURE FEATURE: Filter new listings only (if enabled)
            # ======================================================
            # When FILTER_NEW_LISTINGS_ONLY is True, this will filter out
            # listings that already exist in the database
            if FILTER_NEW_LISTINGS_ONLY:
                log_info("\n🔍 Filtering for new listings only...")
                all_listings_combined = filter_new_listings(all_listings_combined)
                log_info(f"  After filtering: {len(all_listings_combined)} new listings")
            
            # FUTURE FEATURE: Separate listings for status updates vs full scrape
            # ===================================================================
            # When STATUS_UPDATE_MODE is True, this separates listings into:
            # - status_updates: Existing listings that only need status update
            # - new_listings: New listings that need full Phase 2 scraping
            status_updates, new_listings = process_status_updates(all_listings_combined)
            
            # Use combined listings for Phase 2 (or new_listings if status update mode)
            if STATUS_UPDATE_MODE:
                all_listings = new_listings
                results['status_updates_count'] = len(status_updates)
                results['new_listings_count'] = len(new_listings)
            else:
                all_listings = all_listings_combined
            
            listings = all_listings  # For compatibility with Phase 2 code
            
            # FUTURE FEATURE: Process status updates (lightweight Phase 2)
            # =============================================================
            if STATUS_UPDATE_MODE and status_updates:
                log_info(f"\n🔄 Phase 2a: Processing status updates for {len(status_updates)} existing listings...")
                for listing in status_updates:
                    listing_id = listing.get('listing_id')
                    try:
                        if STATUS_UPDATE_SKIP_PHASE2:
                            # TODO: Extract status from Phase 1 data or do lightweight check
                            # For now, we still do Phase 2 but could optimize this
                            log_warning("Status-only mode: Still doing full Phase 2 (optimization TODO)")
                            detail = scrape_listing_details(page, listing['listing_url'])
                            new_status = detail.get('status')
                            if new_status and is_listing_status_changed(listing_id, new_status):
                                update_listing_status(listing_id, new_status)
                                log_success(f"Updated status for {listing_id}: {new_status}")
                        else:
                            # Full Phase 2 but only update status field
                            detail = scrape_listing_details(page, listing['listing_url'])
                            new_status = detail.get('status')
                            if new_status:
                                update_listing_status(listing_id, new_status)
                                listing.update(detail)  # Update local copy too
                    except Exception as e:
                        log_error(f"Error updating status for {listing_id}: {e}")
                        continue
            
            if all_listings and len(all_listings) > 0:
                # Phase 2: Scrape detail pages for ALL listings (or new listings only if status update mode)
                listings_to_process = all_listings
                log_info(f"\nPhase 2: Scraping detail pages for {len(listings_to_process)} listings...")
                
                if PHASE2_PARALLEL and len(listings_to_process) > 1:
                    # Parallel processing with rate limiting detection and automatic fallback
                    log_info(f"  Using parallel processing with {PHASE2_MAX_WORKERS} workers")
                    log_info(f"  Delay between requests: {PHASE2_DELAY_BETWEEN_REQUESTS}s")
                    log_info(f"  Rate limit threshold: {PHASE2_RATE_LIMIT_THRESHOLD} errors before fallback")
                    
                    # Create a new browser context for each worker
                    contexts = []
                    pages = []
                    for i in range(PHASE2_MAX_WORKERS):
                        ctx = browser.new_context(
                            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            locale='ja-JP',  # Japanese locale to try to get JPY prices
                            timezone_id='Asia/Tokyo',
                            extra_http_headers={
                                'Accept-Language': 'ja,ja-JP;q=0.9,en;q=0.8'  # Japanese language preference
                            }
                        )
                        contexts.append(ctx)
                        pages.append(ctx.new_page())
                    
                    # Thread-safe counters and rate limit tracking
                    completed_lock = Lock()
                    completed_count = [0]
                    failed_count = [0]
                    rate_limit_count = [0]
                    is_rate_limited = [False]
                    
                    def scrape_with_retry(listing_data, page_instance, listing_index):
                        """Scrape a single listing with retry logic and rate limit detection"""
                        listing_url = listing_data['listing_url']
                        listing_title = listing_data.get('title', 'N/A')[:50]
                        
                        for attempt in range(1, PHASE2_RETRY_ATTEMPTS + 1):
                            try:
                                # Add delay to avoid rate limiting
                                if attempt > 1:
                                    time.sleep(2 * attempt)  # Exponential backoff on retry
                                else:
                                    time.sleep(PHASE2_DELAY_BETWEEN_REQUESTS)
                                
                                detail = scrape_listing_details(page_instance, listing_url)
                                listing_data.update(detail)
                                
                                with completed_lock:
                                    completed_count[0] += 1
                                    log_success(f"  [{completed_count[0]}/{len(listings_to_process)}] {listing_title}")
                                
                                return True
                            except Exception as e:
                                error_str = str(e).lower()
                                is_rate_limit_error = (
                                    '429' in error_str or 
                                    'rate limit' in error_str or 
                                    'too many requests' in error_str or
                                    'timeout' in error_str
                                )
                                
                                if is_rate_limit_error:
                                    with completed_lock:
                                        rate_limit_count[0] += 1
                                        if rate_limit_count[0] >= PHASE2_RATE_LIMIT_THRESHOLD:
                                            is_rate_limited[0] = True
                                            log_warning(f"\nRate limiting detected ({rate_limit_count[0]} errors)")
                                            log_info("Switching to sequential processing with increased delays...")
                                
                                if attempt < PHASE2_RETRY_ATTEMPTS and not is_rate_limited[0]:
                                    if is_rate_limit_error:
                                        log_warning(f"Rate limit error on attempt {attempt} for {listing_title}, waiting longer...")
                                        time.sleep(5 * attempt)  # Longer wait for rate limits
                                    else:
                                        log_warning(f"Attempt {attempt} failed for {listing_title}, retrying...")
                                    continue
                                else:
                                    with completed_lock:
                                        failed_count[0] += 1
                                        completed_count[0] += 1
                                    
                                    if is_rate_limited[0]:
                                        # Don't log individual errors if we're rate limited
                                        return False
                                    else:
                                        log_error(f"[{completed_count[0]}/{len(listings_to_process)}] Failed after {PHASE2_RETRY_ATTEMPTS} attempts: {listing_title}")
                                        log_error(f"     Error: {str(e)[:100]}")
                                    return False
                        return False
                    
                    # Distribute listings across workers
                    with ThreadPoolExecutor(max_workers=PHASE2_MAX_WORKERS) as executor:
                        futures = []
                        for idx, listing in enumerate(listings_to_process):
                            # Check if we should stop parallel processing
                            if is_rate_limited[0]:
                                break
                            
                            # Round-robin assignment of listings to pages
                            page_idx = idx % PHASE2_MAX_WORKERS
                            future = executor.submit(scrape_with_retry, listing, pages[page_idx], idx)
                            futures.append(future)
                        
                        # Wait for all to complete
                        for future in as_completed(futures):
                            if is_rate_limited[0]:
                                # Cancel remaining futures if rate limited
                                for f in futures:
                                    f.cancel()
                                break
                            future.result()  # This will raise if there was an exception, but we handle it in the function
                    
                    # Close worker contexts
                    for ctx in contexts:
                        ctx.close()
                    
                    # If rate limited or too many failures, fall back to sequential
                    failure_rate = failed_count[0] / len(listings_to_process) if listings_to_process else 0
                    remaining_listings = [l for l in listings_to_process if 'description' not in l or not l.get('description')]
                    
                    if is_rate_limited[0] or (failure_rate > PHASE2_FAILURE_THRESHOLD and remaining_listings):
                        log_warning(f"\nParallel processing issues detected:")
                        if is_rate_limited[0]:
                            log_warning(f"     - Rate limiting: {rate_limit_count[0]} errors")
                        if failure_rate > PHASE2_FAILURE_THRESHOLD:
                            log_warning(f"     - High failure rate: {failed_count[0]}/{len(listings_to_process)} ({failure_rate*100:.1f}%)")
                        
                        if remaining_listings:
                            log_info(f"\nProcessing {len(remaining_listings)} remaining listings sequentially with increased delays...")
                            increased_delay = PHASE2_DELAY_BETWEEN_REQUESTS * 3  # Triple the delay
                            
                            for i, listing in enumerate(remaining_listings, 1):
                                if 'description' in listing and listing.get('description'):
                                    continue  # Skip if already has description
                                
                                log_info(f"  [{i}/{len(remaining_listings)}] Sequential: {listing.get('title', 'N/A')[:50]}")
                                try:
                                    time.sleep(increased_delay)
                                    detail = scrape_listing_details(page, listing['listing_url'])
                                    listing.update(detail)
                                except Exception as e:
                                    log_error(f"    Error: {str(e)[:100]}")
                                    continue
                    
                    if failed_count[0] > 0:
                        log_warning(f"\n{failed_count[0]} listing(s) failed to scrape")
                    
                else:
                    # Sequential processing (safer, slower)
                    if not PHASE2_PARALLEL:
                        log_info("  Using sequential processing (parallel disabled)")
                    else:
                        log_info("  Using sequential processing (only 1 listing)")
                    
                    for i, listing in enumerate(listings_to_process, 1):
                        log_info(f"\n[{i}/{len(listings_to_process)}] Scraping details for: {listing.get('title', 'N/A')[:50]}")
                        try:
                            detail = scrape_listing_details(page, listing['listing_url'])
                            listing.update(detail)
                            time.sleep(PHASE2_DELAY_BETWEEN_REQUESTS)  # Rate limiting
                        except Exception as e:
                            log_error(f"Error scraping {listing.get('listing_url')}: {e}")
                            continue
                
                results['extraction_test'] = True
                results['listings_found'] = len(listings_to_process)
                results['sample_data'] = listings_to_process
                log_success(f"\nPhase 2 complete: Processed {len(listings_to_process)} listings")
                
                # FUTURE FEATURE: Mark listings as scraped in database
                # =====================================================
                if FILTER_NEW_LISTINGS_ONLY:
                    log_info("\n💾 Marking listings as scraped in database...")
                    for listing in listings_to_process:
                        listing_id = listing.get('listing_id')
                        if listing_id:
                            mark_listing_as_scraped(listing_id)
                    log_success(f"Marked {len(listings_to_process)} listings as scraped")
            else:
                results['notes'].append("No listings found - HTML structure needs inspection")
                log_warning("No listings found - HTML structure needs inspection")
            
            # Save HTML for inspection
            html_file = 'validation/results/buyee_playwright_html.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            log_info(f"\nHTML saved to: {html_file}")
            
        except Exception as e:
            results['challenges'].append(f"Error during scraping: {str(e)}")
            log_error(f"Error: {e}")
            import traceback
            if LOG_ENABLED:
                logging.exception("Full traceback:")
            traceback.print_exc()
        finally:
            browser.close()
    
    # Download ALL images for each listing
    if results.get('sample_data'):
        images_dir = 'validation/results/buyee_playwright_images'
        os.makedirs(images_dir, exist_ok=True)
        log_info("\nDownloading ALL images for listings...")
        for idx, listing in enumerate(results['sample_data']):
            local_images = []
            
            # Download all images from all_images array
            all_images = listing.get('all_images', [])
            if all_images:
                log_info(f"  Listing {idx+1}: Downloading {len(all_images)} images...")
                for img_idx, image_url in enumerate(all_images):
                    # Filter out tracking pixels, icons, and non-product images
                    if not any(excluded in image_url.lower() for excluded in [
                        'spacer.gif', 'icon_', 'logo_', 'step/', 'common/icon',
                        'twitter.com', 't.co', 'analytics.twitter.com', 'bat.bing.com',
                        'adsct', 'adsct?'
                    ]):
                        image_filename = download_image(image_url, images_dir, idx, img_idx)
                        if image_filename:
                            local_images.append(f"buyee_playwright_images/{image_filename}")
            
            # Fallback: Download primary image if no all_images or if all_images is empty
            if not local_images:
                image_url = listing.get('image_url')
                if image_url:
                    image_filename = download_image(image_url, images_dir, idx, 0)
                    if image_filename:
                        local_images.append(f"buyee_playwright_images/{image_filename}")
            
            if local_images:
                listing['local_images'] = local_images
                listing['local_image_path'] = local_images[0]  # Keep first image for backwards compatibility
    
    
    # Save results
    md_file = 'validation/results/buyee_playwright_results.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Buyee Scraping Test Results - Playwright Version\n\n")
        f.write(f"**Date Tested:** {results['test_date']}\n")
        f.write(f"**Search Term:** {results['search_term']}\n\n")
        
        f.write("## Test Results\n\n")
        f.write(f"- **Access Test:** {'✅ PASS' if results['access_test'] else '❌ FAIL'}\n")
        f.write(f"- **Search Test:** {'✅ PASS' if results['search_test'] else '❌ FAIL'}\n")
        f.write(f"- **Extraction Test:** {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}\n")
        f.write(f"- **Listings Found:** {results['listings_found']}\n")
        if 'total_listings_count' in results:
            f.write(f"- **Total Listings Count:** {results['total_listings_count']}\n")
        f.write("\n")
        
        if results.get('challenges'):
            f.write("## Challenges Encountered\n\n")
            for challenge in results['challenges']:
                f.write(f"- {challenge}\n")
            f.write("\n")
        
        if results.get('notes'):
            f.write("## Notes\n\n")
            for note in results['notes']:
                f.write(f"- {note}\n")
            f.write("\n")
        
        if results.get('sample_data'):
            f.write("## Sample Data Extracted\n\n")
            for i, listing in enumerate(results['sample_data'], 1):
                f.write(f"### Listing {i}: {listing.get('title', 'N/A')[:80]}\n\n")
                
                # Write structured fields
                shop_name = listing.get('shop_name', 'N/A')
                f.write(f"**Shop:** {shop_name}\n\n")
                
                f.write(f"**Title:** {listing.get('title', 'N/A')}\n\n")
                
                # Only show shop-specific fields for Yahoo Japan Auctions
                if shop_name == 'Yahoo Japan Auctions':
                    buyout_price = listing.get('buyout_price', '')
                    f.write(f"**Buyout Price:** {buyout_price if buyout_price else 'N/A'}\n\n")
                    
                    current_price = listing.get('current_price', listing.get('price', 'N/A'))
                    f.write(f"**Current Price:** {current_price}\n\n")
                
                description = listing.get('description', '')
                f.write(f"**Description (Item Explanation):** {description if description else 'N/A'}\n\n")
                
                # Only show shop-specific fields for Yahoo Japan Auctions
                if shop_name == 'Yahoo Japan Auctions':
                    condition = listing.get('condition', '')
                    f.write(f"**Item Condition:** {condition if condition else 'N/A'}\n\n")
                    
                    bids = listing.get('number_of_bids', '')
                    f.write(f"**Number of Bids:** {bids if bids else 'N/A'}\n\n")
                    
                    closing_time = listing.get('closing_time_jst', '')
                    f.write(f"**Closing Time (JST):** {closing_time if closing_time else 'N/A'}\n\n")
                
                listing_url = listing.get('listing_url', '')
                f.write(f"**Listing URL:** [{listing_url}]({listing_url})\n\n")
                
                # Write all images - prefer local images if available, otherwise use URLs
                local_images = listing.get('local_images', [])
                all_images = listing.get('all_images', [])
                
                if local_images:
                    f.write("**Images (Downloaded):**\n\n")
                    for img_idx, img_path in enumerate(local_images, 1):
                        f.write(f"{img_idx}. ![Image {img_idx}]({img_path})\n\n")
                elif all_images:
                    f.write("**Images:**\n\n")
                    for img_idx, img_url in enumerate(all_images, 1):
                        f.write(f"{img_idx}. ![Image {img_idx}]({img_url})\n\n")
                
                f.write("---\n\n")
    
    json_file = 'validation/results/buyee_playwright_results.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    log_info("\n" + "=" * 60)
    log_info("Test Results Summary:")
    log_info("=" * 60)
    log_info(f"Access Test: {'✅ PASS' if results['access_test'] else '❌ FAIL'}")
    log_info(f"Search Test: {'✅ PASS' if results['search_test'] else '❌ FAIL'}")
    log_info(f"Extraction Test: {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}")
    log_info(f"Listings Found: {results['listings_found']}")
    if 'total_listings_count' in results:
        log_info(f"Total Listings Count: {results['total_listings_count']}")
    if 'pages_scraped' in results:
        log_info(f"Pages Scraped: {results['pages_scraped']}")
    log_info(f"\nResults saved to:")
    log_info(f"  - Markdown: {md_file}")
    log_info(f"  - JSON: {json_file}")
    if log_filepath:
        log_info(f"  - Log file: {log_filepath}")
    
    # Final log entry
    if LOG_ENABLED:
        logging.info("=" * 60)
        logging.info("Scraping session completed")
        logging.info("=" * 60)
    
    return results

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()
    
    # Run main function with search term from arguments
    results = main(search_term=args.search_term)
    
    # Exit with appropriate code
    if results.get('error'):
        sys.exit(1)
    elif not results.get('extraction_test'):
        sys.exit(1)
    else:
        sys.exit(0)
