#!/usr/bin/env python3
"""
Buyee Details Scraper - Phase 2

Scrapes detailed information from Buyee.jp listing pages.
This is Phase 2 of the scraping process.
Takes JSON input from buyee_search.py (Phase 1) and outputs detailed results.
"""

import json
import time
import sys
import argparse
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")

# Import shared utilities
from buyee_utils import (
    BASE_URL,
    PHASE2_PARALLEL, PHASE2_MAX_WORKERS, PHASE2_RETRY_ATTEMPTS,
    PHASE2_DELAY_BETWEEN_REQUESTS, PHASE2_RATE_LIMIT_THRESHOLD, PHASE2_FAILURE_THRESHOLD,
    FILTER_NEW_LISTINGS_ONLY,
    LOG_ENABLED,
    setup_logging, log_info, log_warning, log_error, log_success,
    translate_japanese, contains_japanese, extract_listing_id,
    validate_listing_details, download_image, mark_listing_as_scraped
)

import logging

def scrape_listing_details(page, listing_url):
    """Phase 2: Scrape detailed information from a single listing's detail page
    
    Extracts additional fields not available in search results:
    
    Common fields (all shops):
    - Description (Item Explanation)
    - Seller Info
    - Shipping Info
    - Status (sold/available)
    - All product images
    
    Yahoo-specific fields:
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
                    shop_name = 'Yahoo'
                    break
                elif 'mercari' in class_str:
                    shop_name = 'Mercari'
                    break
                elif 'rakuma' in class_str:
                    shop_name = 'Rakuma'
                    break
                elif 'jdifleamarket' in class_str:
                    shop_name = 'Yahoo Shopping'
                    break
        
        # Fallback: Try JavaScript extraction if not found in HTML
        if not shop_name:
            shop_result = page.evaluate(r'''
                () => {
                    const shopDiv = document.querySelector('div.store-name');
                    if (shopDiv) {
                        const classes = shopDiv.className;
                        if (classes.includes('yauc') && classes.includes('jdiaution')) {
                            return 'Yahoo';
                        } else if (classes.includes('mercari')) {
                            return 'Mercari';
                        } else if (classes.includes('rakuma')) {
                            return 'Rakuma';
                        } else if (classes.includes('jdifleamarket')) {
                            return 'Yahoo Shopping';
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
        
        # Extract shop-specific fields only for Yahoo (Auction)
        if shop_name == 'Yahoo':
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
            
            # Number of bids and closing time are already extracted above from itemDetail_sec
            # Just store them if found (only for Yahoo)
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
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Buyee Details Scraper - Phase 2 (Detail Pages)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        dest='input_file',
        type=str,
        default='validation/results/buyee_search_results.json',
        help='Input JSON file from buyee_search.py (Phase 1)'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        type=str,
        default='validation/results/buyee_details_results.json',
        help='Output JSON file path'
    )
    return parser.parse_args()


def main(input_file=None, output_file=None):
    """Main scraping function - Phase 2 only
    
    Args:
        input_file (str, optional): Input JSON file from buyee_search.py. If None, uses default.
        output_file (str, optional): Output JSON file path. If None, uses default.
    
    Returns:
        dict: Results dictionary with scraping results
    """
    if input_file is None:
        input_file = 'validation/results/buyee_search_results.json'
    if output_file is None:
        output_file = 'validation/results/buyee_details_results.json'
    
    # Setup logging first
    log_filepath = setup_logging()
    
    if not PLAYWRIGHT_AVAILABLE:
        log_error("Playwright is not available. Please install it first.")
        log_error("Install with: pip install playwright")
        log_error("Then run: playwright install chromium")
        return {'error': 'Playwright not available'}
    
    log_info("=" * 60)
    log_info("Buyee Details Scraper - Phase 2 (Detail Pages)")
    log_info("=" * 60)
    log_info(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_info(f"Input file: {input_file}")
    if log_filepath:
        log_info(f"Log file: {log_filepath}")
    log_info("")
    
    # Read input JSON from Phase 1
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            phase1_results = json.load(f)
    except FileNotFoundError:
        log_error(f"Input file not found: {input_file}")
        log_error("Please run buyee_search.py first to generate the input file.")
        return {'error': f'Input file not found: {input_file}'}
    except json.JSONDecodeError as e:
        log_error(f"Error parsing JSON file: {e}")
        return {'error': f'Invalid JSON file: {input_file}'}
    
    # Extract listings from Phase 1 results
    listings_to_process = phase1_results.get('all_listings_basic', [])
    if not listings_to_process:
        log_warning("No listings found in input file")
        return {'error': 'No listings found in input file'}
    
    log_info(f"Found {len(listings_to_process)} listings from Phase 1")
    
    results = {
        'test_date': datetime.now().isoformat(),
        'input_file': input_file,
        'listings_found': len(listings_to_process),
        'challenges': [],
        'notes': [],
        'sample_data': []
    }
    
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
                        locale='ja-JP',
                        timezone_id='Asia/Tokyo',
                        extra_http_headers={
                            'Accept-Language': 'ja,ja-JP;q=0.9,en;q=0.8'
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
                        if is_rate_limited[0]:
                            break
                        
                        # Round-robin assignment of listings to pages
                        page_idx = idx % PHASE2_MAX_WORKERS
                        future = executor.submit(scrape_with_retry, listing, pages[page_idx], idx)
                        futures.append(future)
                    
                    # Wait for all to complete
                    for future in as_completed(futures):
                        if is_rate_limited[0]:
                            for f in futures:
                                f.cancel()
                            break
                        future.result()
                
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
                        increased_delay = PHASE2_DELAY_BETWEEN_REQUESTS * 3
                        
                        for i, listing in enumerate(remaining_listings, 1):
                            if 'description' in listing and listing.get('description'):
                                continue
                            
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
                        time.sleep(PHASE2_DELAY_BETWEEN_REQUESTS)
                    except Exception as e:
                        log_error(f"Error scraping {listing.get('listing_url')}: {e}")
                        continue
            
            results['listings_found'] = len(listings_to_process)
            results['sample_data'] = listings_to_process
            log_success(f"\nPhase 2 complete: Processed {len(listings_to_process)} listings")
            
            # Mark listings as scraped in database (if enabled)
            if FILTER_NEW_LISTINGS_ONLY:
                log_info("\n💾 Marking listings as scraped in database...")
                for listing in listings_to_process:
                    listing_id = listing.get('listing_id')
                    if listing_id:
                        mark_listing_as_scraped(listing_id)
                log_success(f"Marked {len(listings_to_process)} listings as scraped")
        
        except Exception as e:
            results['challenges'].append(f"Error during scraping: {str(e)}")
            log_error(f"Error: {e}")
            import traceback
            if LOG_ENABLED:
                logging.exception("Full traceback:")
            traceback.print_exc()
        finally:
            browser.close()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save results to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    log_info(f"\n{'='*60}")
    log_info("Phase 2 Complete")
    log_info(f"{'='*60}")
    log_info(f"Listings Processed: {results['listings_found']}")
    log_info(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()
    
    # Run main function
    results = main(input_file=args.input_file, output_file=args.output_file)
    
    # Exit with appropriate code
    if results.get('error'):
        sys.exit(1)
    elif results.get('listings_found', 0) == 0:
        sys.exit(1)
    else:
        sys.exit(0)

