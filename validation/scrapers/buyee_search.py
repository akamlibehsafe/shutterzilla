#!/usr/bin/env python3
"""
Buyee Search Scraper - Phase 1

Scrapes search results from Buyee.jp and outputs JSON.
This is Phase 1 of the scraping process.
Output can be used as input for buyee_details.py (Phase 2).
"""

import json
import time
import sys
import argparse
import os
from datetime import datetime
from urllib.parse import quote_plus

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")

# Import shared utilities
from buyee_utils import (
    BASE_URL, DEFAULT_SEARCH_TERM,
    PAGINATION_ENABLED, PAGINATION_MAX_PAGES, PAGINATION_DELAY_BETWEEN_PAGES,
    FILTER_NEW_LISTINGS_ONLY, filter_new_listings,
    LOG_ENABLED,
    setup_logging, log_info, log_warning, log_error, log_debug, log_success,
    translate_japanese, contains_japanese, extract_listing_id,
    validate_search_result
)

import logging

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
                                listing.shopName = 'Yahoo';
                            } else if (storeNameText === 'Mercari') {
                                listing.shopName = 'Mercari';
                            } else if (storeNameText === 'Rakuten Rakuma') {
                                listing.shopName = 'Rakuma';
                            } else if (storeNameText === 'JDirectItems Fleamarket') {
                                listing.shopName = 'Yahoo Shopping';
                            } else {
                                listing.shopName = storeNameText; // Fallback: use as-is
                            }
                        } else {
                            // Fallback: get text directly from storeName element
                            const storeNameText = storeNameElem.textContent.trim();
                            if (storeNameText === 'JDirectItems Auction') {
                                listing.shopName = 'Yahoo';
                            } else if (storeNameText === 'Mercari') {
                                listing.shopName = 'Mercari';
                            } else if (storeNameText === 'Rakuten Rakuma') {
                                listing.shopName = 'Rakuma';
                            } else if (storeNameText === 'JDirectItems Fleamarket') {
                                listing.shopName = 'Yahoo Shopping';
                            } else if (storeNameText) {
                                listing.shopName = storeNameText;
                            }
                        }
                    }
                    
                    // Extract price - different logic for Yahoo vs other shops
                    if (listing.shopName === 'Yahoo') {
                        // For Yahoo (Auction), try to extract Buyout Price and Current Price separately
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
                shop_name = 'Yahoo'
            elif shop_name == 'Rakuten Rakuma':
                shop_name = 'Rakuma'
            elif shop_name == 'JDirectItems Fleamarket':
                shop_name = 'Yahoo Shopping'
            
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
            if shop_name == 'Yahoo':
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


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Buyee Search Scraper - Phase 1 (Search Results)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-s', '--search',
        dest='search_term',
        type=str,
        default=DEFAULT_SEARCH_TERM,
        help=f'Search term to use (default: "{DEFAULT_SEARCH_TERM}")'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        type=str,
        default='validation/results/buyee_search_results.json',
        help='Output JSON file path'
    )
    return parser.parse_args()


def main(search_term=None, output_file=None):
    """Main scraping function - Phase 1 only
    
    Args:
        search_term (str, optional): Search term to use. If None, uses DEFAULT_SEARCH_TERM.
        output_file (str, optional): Output JSON file path. If None, uses default.
    
    Returns:
        dict: Results dictionary with scraping results
    """
    # Use provided search_term, or default
    if search_term is None:
        search_term = DEFAULT_SEARCH_TERM
    
    if output_file is None:
        output_file = 'validation/results/buyee_search_results.json'
    
    # Setup logging first
    log_filepath = setup_logging()
    
    if not PLAYWRIGHT_AVAILABLE:
        log_error("Playwright is not available. Please install it first.")
        log_error("Install with: pip install playwright")
        log_error("Then run: playwright install chromium")
        return {'error': 'Playwright not available'}
    
    log_info("=" * 60)
    log_info("Buyee Search Scraper - Phase 1 (Search Results)")
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
        'listings_found': 0,
        'challenges': [],
        'notes': [],
        'all_listings_basic': []
    }
    
    search_url = f"{BASE_URL}/item/crosssearch/query/{quote_plus(search_term)}?conversionType=top_page_search&suggest=1"
    
    with sync_playwright() as p:
        log_info("Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='ja-JP',
            timezone_id='Asia/Tokyo',
            extra_http_headers={
                'Accept-Language': 'ja,ja-JP;q=0.9,en;q=0.8'
            }
        )
        page = context.new_page()
        
        try:
            # Navigate to homepage first
            log_info(f"Navigating to homepage: {BASE_URL}")
            page.goto(BASE_URL, wait_until='domcontentloaded', timeout=60000)
            time.sleep(2)
            results['access_test'] = True
            log_success("Homepage loaded successfully")
            
            # Check if we can find a search form
            log_info("\nLooking for search form...")
            search_form_found = False
            search_input = None
            
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
                log_info(f"  Entering search term: {search_term}")
                search_input.fill(search_term)
                time.sleep(1)
                
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
                    log_info("  Pressing Enter to submit search...")
                    search_input.press('Enter')
                
                page.wait_for_load_state('networkidle', timeout=30000)
                time.sleep(3)
                log_success("Search submitted")
            else:
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
                    time.sleep(3)
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
            results['listings_found'] = len(all_listings_combined)
            
            # Filter new listings only (if enabled)
            if FILTER_NEW_LISTINGS_ONLY:
                log_info("\n🔍 Filtering for new listings only...")
                all_listings_combined = filter_new_listings(all_listings_combined)
                log_info(f"  After filtering: {len(all_listings_combined)} new listings")
                results['all_listings_basic'] = all_listings_combined
                results['listings_found'] = len(all_listings_combined)
            
        except Exception as e:
            results['challenges'].append(f"Error during scraping: {str(e)}")
            log_error(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save results to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    log_info(f"\n{'='*60}")
    log_info("Phase 1 Complete")
    log_info(f"{'='*60}")
    log_info(f"Listings Found: {results['listings_found']}")
    if 'total_listings_count' in results:
        log_info(f"Total Listings Count: {results['total_listings_count']}")
    if 'pages_scraped' in results:
        log_info(f"Pages Scraped: {results['pages_scraped']}")
    log_info(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()
    
    # Run main function
    results = main(search_term=args.search_term, output_file=args.output_file)
    
    # Exit with appropriate code
    if results.get('error'):
        sys.exit(1)
    elif not results.get('search_test'):
        sys.exit(1)
    else:
        sys.exit(0)

