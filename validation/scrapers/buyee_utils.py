#!/usr/bin/env python3
"""
Buyee Scraper Utilities

Shared utilities for Buyee scraping scripts.
This module contains:
- Configuration constants
- Logging functions
- Helper functions
- Database placeholder functions

Used by:
- buyee_search.py (Phase 1: Search results scraping)
- buyee_details.py (Phase 2: Detail page scraping)
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
PHASE2_PARALLEL = False  # Set to False to process sequentially (True causes thread errors with Playwright sync API)
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
