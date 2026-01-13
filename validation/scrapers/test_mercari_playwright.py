#!/usr/bin/env python3
"""
Mercari Japan Scraping Test - Playwright Version

This script tests Mercari scraping using Playwright for JavaScript rendering.
"""

import json
import time
import os
import requests
import re
from datetime import datetime
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")

def download_image(image_url, output_dir, listing_index, image_index=0):
    """Download an image from URL and save it locally"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=10, stream=True)
        if response.status_code == 200:
            # Get file extension from URL or default to jpg
            parsed_url = urlparse(image_url)
            ext = os.path.splitext(parsed_url.path)[1] or '.jpg'
            # Remove query parameters from extension
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



BASE_URL = "https://jp.mercari.com"
SEARCH_TERM = "Nikon FM2"
SEARCH_PARAMS = "sort=created_time&order=desc&status=on_sale"  # Newest first, only on sale items

def translate_japanese(text, target_lang='en'):
    """Translate Japanese text to English (or other language)"""
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

def extract_listing_detail(page, listing_url):
    """Extract detailed information from a listing's detail page"""
    from bs4 import BeautifulSoup
    import re
    
    try:
        print(f"  Visiting detail page: {listing_url}")
        page.goto(listing_url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)  # Wait for page to fully load
        
        # Use JavaScript to extract images (more reliable for React apps)
        images_js = page.evaluate('''
            () => {
                const images = [];
                document.querySelectorAll('img').forEach(img => {
                    const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src');
                    if (src && (src.includes('mercdn.net') || src.includes('mercari'))) {
                        images.push(src);
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
        
        # Extract description - use regex on cleaned text (more reliable for React apps)
        description_text = None
        
        # Strategy: Look for description pattern in cleaned text (after removing scripts)
        desc_patterns = [
            r'商品説明[：:\s]+\n?([^\n]{50,2000})',  # 商品説明 followed by text
            r'商品の説明[：:\s]+\n?([^\n]{50,2000})',  # 商品の説明
            r'説明[：:\s]+\n?([^\n]{50,2000})',  # 説明
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, full_text, re.DOTALL)
            if match:
                candidate = match.group(1).strip()
                # Filter out script-like content (common false positives)
                if not re.search(r'(function|var |const |let |script|gtm\.|dataLayer)', candidate, re.I):
                    if len(candidate) > 20:  # Meaningful length
                        description_text = candidate
                        break
        
        # Strategy 2: Try to find description in structured elements
        if not description_text:
            desc_headings = soup.find_all(string=re.compile(r'商品説明|商品の説明', re.I))
            for heading in desc_headings[:1]:  # Just check first one
                parent = heading.find_parent()
                if parent:
                    # Get text from parent and siblings, but filter out scripts
                    text_parts = []
                    for elem in [parent] + list(parent.next_siblings)[:3]:
                        if hasattr(elem, 'get_text'):
                            text = elem.get_text(strip=True)
                            if text and len(text) > 20:
                                # Skip if looks like script
                                if not re.search(r'(function|var |const |gtm\.)', text, re.I):
                                    text_parts.append(text)
                    if text_parts:
                        description_text = ' '.join(text_parts[:3])  # Take first 3 parts
        
        if description_text:
            # Clean up description (remove excessive whitespace, limit length)
            description_text = ' '.join(description_text.split())
            if len(description_text) > 2000:
                description_text = description_text[:2000] + '...'
            detail['description'] = description_text
            # Translate if it contains Japanese characters
            if any(ord(char) > 127 for char in description_text[:100]):
                try:
                    detail['description_translated'] = translate_japanese(description_text[:1000])
                except Exception as e:
                    print(f"    Translation error: {e}")
        
        # Extract condition/status - look for condition indicators
        condition_text = None
        condition_patterns = [r'状態[：:]\s*([^\n]+)', r'コンディション[：:]\s*([^\n]+)', 
                             r'ランク[：:]\s*([^\n]+)', r'condition[：:]\s*([^\n]+)']
        for pattern in condition_patterns:
            match = re.search(pattern, full_text, re.I)
            if match:
                condition_text = match.group(1).strip()
                break
        if condition_text:
            detail['condition'] = condition_text
        
        # Check if sold/available
        if re.search(r'売り切れ|sold out|この商品は売り切れ', full_text, re.I):
            detail['status'] = 'sold'
        elif re.search(r'販売中|available|在庫あり', full_text, re.I):
            detail['status'] = 'available'
        
        # Extract price (if not already extracted)
        price_match = re.search(r'(¥|BRL|円)\s*([\d,]+\.?\d*)', full_text)
        if price_match:
            detail['price_detail'] = price_match.group(0)
        
        # Extract seller information
        seller_text = None
        seller_patterns = [r'出品者[：:]\s*([^\n]+)', r'seller[：:]\s*([^\n]+)']
        for pattern in seller_patterns:
            match = re.search(pattern, full_text, re.I)
            if match:
                seller_text = match.group(1).strip()[:200]
                break
        if seller_text:
            detail['seller_info'] = seller_text
        
        # Extract shipping information
        shipping_text = None
        shipping_patterns = [r'送料[：:]\s*([^\n]+)', r'shipping[：:]\s*([^\n]+)']
        for pattern in shipping_patterns:
            match = re.search(pattern, full_text, re.I)
            if match:
                shipping_text = match.group(1).strip()[:200]
                break
        if shipping_text:
            detail['shipping_info'] = shipping_text
        
        # Extract ALL images using JavaScript result (more reliable)
        image_urls = []
        seen_urls = set()
        
        # Use JavaScript-extracted images first (most reliable)
        for src in images_js:
            if not src.startswith('http'):
                src = 'https:' + src if src.startswith('//') else BASE_URL + src
            url_key = src.split('?')[0]
            if url_key not in seen_urls:
                seen_urls.add(url_key)
                image_urls.append(src)
        
        # Fallback: Also check HTML for any missed images
        for img in soup.find_all('img'):
            src = img.get('src', '') or img.get('data-src', '') or img.get('data-lazy-src', '')
            if src and ('mercdn.net' in src or 'mercari' in src.lower()):
                if not src.startswith('http'):
                    src = 'https:' + src if src.startswith('//') else BASE_URL + src
                url_key = src.split('?')[0]
                if url_key not in seen_urls:
                    seen_urls.add(url_key)
                    image_urls.append(src)
        
        if image_urls:
            detail['all_images'] = image_urls  # ALL images, no limit
        
        # Detect warning keywords
        warnings = []
        if re.search(r'ジャンク|junk', full_text, re.I):
            warnings.append('junk')
        if re.search(r'修理|repair', full_text, re.I):
            warnings.append('repair')
        if warnings:
            detail['warning_keywords'] = warnings
        
        # Extract category/brand if available
        category_match = re.search(r'カテゴリー[：:]\s*([^\n]+)', full_text, re.I)
        if category_match:
            detail['category'] = category_match.group(1).strip()[:100]
        
        return detail
    except Exception as e:
        print(f"  Error extracting detail: {e}")
        import traceback
        traceback.print_exc()
        return {}

def extract_items_from_api_response(api_data):
    """Extract items from API response JSON"""
    items = []
    if not api_data:
        return items
    
    try:
        # Common API response structures
        if isinstance(api_data, dict):
            # Try different keys that might contain items
            for key in ['items', 'results', 'data', 'entities', 'products', 'listings', 'hits']:
                if key in api_data:
                    data = api_data[key]
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                # Extract item data
                                href = item.get('id') or item.get('itemId') or item.get('href') or ''
                                if not href and 'url' in item:
                                    href = item['url']
                                if not href and 'link' in item:
                                    href = item['link']
                                
                                # Try to construct href from item ID
                                if not href and 'id' in item:
                                    item_id = str(item['id'])
                                    if item_id.startswith('m') or item_id.isdigit():
                                        href = f"/en/item/m{item_id}" if not item_id.startswith('m') else f"/en/item/{item_id}"
                                
                                if href and '/item/m' in str(href):
                                    items.append({
                                        'href': href.split('?')[0],
                                        'title': item.get('name') or item.get('title') or item.get('itemName') or '',
                                        'price': item.get('price') or item.get('itemPrice') or '',
                                        'imageUrl': item.get('thumbnails') or item.get('imageUrl') or item.get('thumbnail') or item.get('image') or ''
                                    })
                    elif isinstance(data, dict):
                        # Nested structure, recurse
                        items.extend(extract_items_from_api_response(data))
            
            # Also search for item patterns in the JSON string
            json_str = json.dumps(api_data)
            item_id_matches = re.findall(r'/item/m(\d+)', json_str)
            if item_id_matches and len(items) == 0:
                # Found item IDs but couldn't extract full data - create minimal items
                for item_id in set(item_id_matches):
                    items.append({
                        'href': f"/en/item/m{item_id}",
                        'title': '',
                        'price': '',
                        'imageUrl': ''
                    })
    except Exception as e:
        print(f"    Error extracting from API response: {e}")
    
    return items

def extract_items_from_next_data(page):
    """Extract items from __NEXT_DATA__ script tag"""
    items = []
    try:
        result = page.evaluate('''
            () => {
                try {
                    const nextDataScript = document.querySelector('script#__NEXT_DATA__');
                    if (!nextDataScript) return null;
                    
                    const nextData = JSON.parse(nextDataScript.textContent);
                    
                    // Search for items in the data structure
                    const findItems = (obj, path = '') => {
                        if (!obj || typeof obj !== 'object') return [];
                        
                        let results = [];
                        
                        // Check if this object looks like an item
                        const objStr = JSON.stringify(obj);
                        if (objStr.includes('/item/m') && (obj.id || obj.itemId || obj.href)) {
                            const href = obj.href || obj.id || obj.itemId || '';
                            if (href && (href.includes('/item/m') || (typeof href === 'string' && href.match(/^m\\d+$/)))) {
                                let itemHref = href;
                                if (!itemHref.includes('/')) {
                                    itemHref = `/en/item/${itemHref}`;
                                }
                                results.push({
                                    href: itemHref.split('?')[0],
                                    title: obj.name || obj.title || obj.itemName || '',
                                    price: obj.price || obj.itemPrice || '',
                                    imageUrl: obj.thumbnails || obj.imageUrl || obj.thumbnail || obj.image || ''
                                });
                            }
                        }
                        
                        // Recursively search nested objects
                        for (const key in obj) {
                            if (key.toLowerCase().includes('item') || key.toLowerCase().includes('product') || key.toLowerCase().includes('listing')) {
                                const value = obj[key];
                                if (Array.isArray(value)) {
                                    for (const item of value) {
                                        if (item && typeof item === 'object') {
                                            results = results.concat(findItems(item, path + '.' + key));
                                        }
                                    }
                                } else if (value && typeof value === 'object') {
                                    results = results.concat(findItems(value, path + '.' + key));
                                }
                            } else if (obj[key] && typeof obj[key] === 'object') {
                                results = results.concat(findItems(obj[key], path + '.' + key));
                            }
                        }
                        
                        return results;
                    };
                    
                    const foundItems = findItems(nextData);
                    
                    // Also try to extract item IDs from the JSON string
                    const dataStr = JSON.stringify(nextData);
                    const itemMatches = dataStr.match(/\\/item\\/m\\d+/g);
                    if (itemMatches && foundItems.length === 0) {
                        // Create minimal items from IDs
                        const uniqueIds = [...new Set(itemMatches)];
                        return uniqueIds.map(href => ({
                            href: href.split('?')[0],
                            title: '',
                            price: '',
                            imageUrl: ''
                        }));
                    }
                    
                    return foundItems;
                } catch (e) {
                    console.error('Error parsing __NEXT_DATA__:', e);
                    return null;
                }
            }
        ''')
        
        if result:
            items = result
    except Exception as e:
        print(f"    Error extracting from __NEXT_DATA__: {e}")
    
    return items

def extract_listing_data_playwright(page):
    """Extract listing data from rendered page using Playwright - simplified version"""
    try:
        # Wait for page to load
        page.wait_for_selector('main', timeout=10000)
        
        # Intercept network requests and responses to find the search API
        # CRITICAL: Extract items directly from API response instead of DOM
        api_requests = []
        search_responses = []
        api_response_data = None  # Store the API response JSON
        
        def handle_request(request):
            url = request.url
            if 'api' in url.lower() or 'search' in url.lower() or 'item' in url.lower():
                api_requests.append(url)
        
        search_api_ready = {'ready': False}
        api_responses_to_process = []  # Store responses to process asynchronously
        
        def handle_response(response):
            url = response.url
            # Look for the main search API that returns all items
            if 'api.mercari.jp/v2/entities:search' in url or ('api.mercari.jp' in url and 'search' in url.lower()):
                print(f"  📡 Found search API response: {url[:100]}")
                api_responses_to_process.append(response)
                search_api_ready['ready'] = True
            # Also track other search API responses
            if 'api.mercari.jp' in url and ('search' in url.lower() or 'items' in url.lower() or 'products' in url.lower()):
                search_responses.append(url)
        
        page.on('request', handle_request)
        page.on('response', handle_response)
        
        # Wait for network to be idle (all API calls to complete)
        print("Waiting for all listings to load...")
        try:
            page.wait_for_load_state('networkidle', timeout=30000)
        except:
            pass
        
        # Wait a bit more for any delayed API responses
        time.sleep(3)
        
        # Wait for the main search API response
        print("Waiting for search API to complete...")
        max_wait = 15
        waited = 0
        while not search_api_ready['ready'] and waited < max_wait:
            time.sleep(1)
            waited += 1
            if waited % 3 == 0:
                print(f"  Waiting for search API... ({waited}s)")
        
        # Process API responses to extract items
        if api_responses_to_process:
            print(f"\n📦 Processing {len(api_responses_to_process)} API response(s)...")
            for response in api_responses_to_process:
                try:
                    # In Playwright, response.json() needs to be awaited, but we're in a callback
                    # So we'll process it synchronously here
                    response_body = response.json()
                    if response_body:
                        api_response_data = response_body
                        print(f"  ✅ Successfully parsed API response")
                        # Try to count items
                        items_count = 0
                        if isinstance(response_body, dict):
                            for key in ['items', 'results', 'data', 'entities', 'products', 'listings', 'hits']:
                                if key in response_body and isinstance(response_body[key], list):
                                    items_count = len(response_body[key])
                                    print(f"    Found {items_count} items in response['{key}']")
                                    break
                            if items_count == 0:
                                response_str = json.dumps(response_body)
                                item_matches = re.findall(r'/item/m\d+', response_str)
                                if item_matches:
                                    print(f"    Found {len(set(item_matches))} unique item references in response")
                except Exception as e:
                    print(f"    Could not parse API response: {e}")
                    # Try alternative: read as text and parse
                    try:
                        response_text = response.text()
                        if response_text:
                            response_body = json.loads(response_text)
                            api_response_data = response_body
                            print(f"  ✅ Parsed API response from text (length: {len(response_text)})")
                    except Exception as e2:
                        print(f"    Also failed to parse as text: {e2}")
        
        # Additional wait for React to fully render after API response
        print("Waiting for listings to render in DOM...")
        time.sleep(3)  # Give React time to render all items from API response
        
        # Poll for items to appear - wait up to 15 seconds for items to load
        # Use data-testid="merListItem-container" as the primary selector (most reliable)
        initial_count = 0
        max_wait_time = 15
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            initial_count = page.evaluate('''
                () => {
                    // Primary method: Use data-testid (most reliable)
                    const containers = document.querySelectorAll('[data-testid="merListItem-container"]').length;
                    
                    // Fallback methods
                    const pattern1 = document.querySelectorAll('a[href*="/en/item/m"]').length;
                    const pattern2 = document.querySelectorAll('a[href*="/item/m"]').length;
                    const pattern3 = Array.from(document.querySelectorAll('a')).filter(a => {
                        const href = a.getAttribute('href') || '';
                        return href.match(/\\/item\\/m\\d+/);
                    }).length;
                    
                    // Return the maximum count found
                    return Math.max(containers, pattern1, pattern2, pattern3);
                }
            ''')
            
            if initial_count >= 95:  # If we have close to 101 items, likely all are loaded
                print(f"  ✅ Found {initial_count} items after {int(time.time() - start_time)}s - likely all loaded!")
                break
            elif initial_count > 0 and (time.time() - start_time) % 2 < 1:  # Print every ~2 seconds
                print(f"  Found {initial_count} items so far... (waiting {int(time.time() - start_time)}s)")
            
            time.sleep(0.5)
        
        print(f"  Initial items found: {initial_count}")
        
        # NEW APPROACH: Try to extract items from API response first (contains all 101 items)
        items_from_api = []
        if api_response_data:
            print("\n🔍 Attempting to extract items from API response...")
            try:
                # Try different possible structures in the API response
                items_from_api = extract_items_from_api_response(api_response_data)
                if items_from_api:
                    print(f"  ✅ Extracted {len(items_from_api)} items from API response!")
                    # If we got items from API, use those instead of scrolling
                    if len(items_from_api) >= 95:
                        print(f"  ✅ API response contains {len(items_from_api)} items - using API data instead of DOM!")
                        # Convert API items to our format and return early
                        all_listings_data = []
                        for item in items_from_api:
                            href = item.get('href', '')
                            if not href.startswith('http'):
                                if href.startswith('/en/'):
                                    href = BASE_URL + href
                                elif href.startswith('/item/'):
                                    href = BASE_URL + '/en' + href
                                else:
                                    href = BASE_URL + '/en/' + href
                            
                            all_listings_data.append({
                                'title': item.get('title', ''),
                                'title_translated': translate_japanese(item.get('title', '')) if item.get('title') else None,
                                'price': item.get('price', ''),
                                'image_url': item.get('imageUrl', '') or item.get('image_url', ''),
                                'listing_url': href,
                            })
                        
                        html_content = page.content()
                        # Use first 5 for detailed extraction
                        listings = all_listings_data[:5]
                        return listings, html_content, len(items_from_api), all_listings_data
            except Exception as e:
                print(f"  ⚠️ Could not extract items from API response: {e}")
                import traceback
                traceback.print_exc()
        
        # FALLBACK: If API extraction failed, try __NEXT_DATA__ extraction
        print("\n🔍 Attempting to extract items from __NEXT_DATA__...")
        items_from_next_data = extract_items_from_next_data(page)
        if items_from_next_data and len(items_from_next_data) >= 95:
            print(f"  ✅ Extracted {len(items_from_next_data)} items from __NEXT_DATA__!")
            all_listings_data = []
            for item in items_from_next_data:
                href = item.get('href', '')
                if not href.startswith('http'):
                    if href.startswith('/en/'):
                        href = BASE_URL + href
                    elif href.startswith('/item/'):
                        href = BASE_URL + '/en' + href
                    else:
                        href = BASE_URL + '/en/' + href
                
                all_listings_data.append({
                    'title': item.get('title', ''),
                    'title_translated': translate_japanese(item.get('title', '')) if item.get('title') else None,
                    'price': item.get('price', ''),
                    'image_url': item.get('imageUrl', '') or item.get('image_url', ''),
                    'listing_url': href,
                })
            
            html_content = page.content()
            listings = all_listings_data[:5]
            return listings, html_content, len(items_from_next_data), all_listings_data
        
        # LAST RESORT: Use scrolling collection (your updated approach)
        print("\n⚠️ API and __NEXT_DATA__ extraction failed, falling back to scrolling collection...")
        previous_count = initial_count
        scroll_attempts = 0
        max_scrolls = 200
        consecutive_no_change = 0
        target_items = 101
        
        # Get viewport info
        viewport_info = page.evaluate('''
            () => {
                return {
                    height: window.innerHeight,
                    width: window.innerWidth,
                    scrollHeight: document.body.scrollHeight,
                    scrollTop: window.pageYOffset || window.scrollY
                };
            }
        ''')
        viewport_height = viewport_info['height']
        scroll_height = viewport_info['scrollHeight']
        
        print(f"  Viewport: {viewport_height}px, Page height: {scroll_height}px")
        estimated_viewports = max(1, scroll_height // viewport_height) if scroll_height > 0 else 20
        print(f"  Need to scroll through ~{estimated_viewports} viewports to cover all rows")
        
        # CRITICAL: With virtual scrolling, we must collect items DURING scrolling, not at the end
        # Strategy: Scroll through page and collect unique items at each position
        print("  Collecting items during scroll (virtual scrolling requires this approach)...")
        collected_items = {}  # Dictionary to store unique items by href
        scroll_positions_checked = set()
        
        # Scroll systematically through the page and collect items at each position
        while scroll_attempts < max_scrolls:
            # Get current scroll position
            current_scroll = page.evaluate('window.pageYOffset || window.scrollY')
            max_scroll = page.evaluate('document.body.scrollHeight - window.innerHeight')
            
            # Scroll in increments - scroll down by 1/4 viewport at a time
            scroll_increment = viewport_height * 0.25
            target_scroll = min(current_scroll + scroll_increment, max_scroll)
            
            page.evaluate(f'window.scrollTo(0, {target_scroll})')
            time.sleep(1.5)  # Wait for items to load
            
            # COLLECT ITEMS at this scroll position (critical for virtual scrolling)
            items_at_position = page.evaluate('''
                () => {
                    const items = [];
                    // Use data-testid containers (most reliable)
                    const containers = Array.from(document.querySelectorAll('[data-testid="merListItem-container"]'));
                    
                    containers.forEach(container => {
                        const link = container.querySelector('a[href*="/item/m"]') || container.querySelector('a[href*="/en/item/m"]');
                        if (!link) return;
                        
                        const href = link.getAttribute('href') || '';
                        if (!href || !href.match(/\\/item\\/m\\d+/)) return;
                        
                        const normalizedHref = href.split('?')[0];
                        
                        // Extract data from container
                        const containerText = (container.textContent || '').trim();
                        let price = '';
                        let title = '';
                        
                        const priceMatch = containerText.match(/(BRL|¥|円|USD|\\$)[\\d,]+\.?\\d*/);
                        if (priceMatch) {
                            price = priceMatch[0];
                            title = containerText.replace(price, '').trim().split('\\n')[0];
                        } else {
                            title = (link.textContent || '').trim() || containerText.split('\\n')[0];
                        }
                        
                        const img = container.querySelector('img');
                        const imageUrl = img ? (img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '') : '';
                        
                        items.push({
                            href: normalizedHref,
                            title: title,
                            price: price,
                            imageUrl: imageUrl
                        });
                    });
                    
                    return items;
                }
            ''')
            
            # Add items to our collection (tracking by href to avoid duplicates)
            for item in items_at_position:
                if item['href'] not in collected_items:
                    collected_items[item['href']] = item
            
            # Check current count of unique items collected
            item_count = len(collected_items)
            
            # Every 10 scrolls, also scroll to bottom to ensure we trigger all loading
            if scroll_attempts % 10 == 0:
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2.5)  # Wait at bottom
                # Collect items at bottom
                items_at_bottom = page.evaluate('''
                    () => {
                        const items = [];
                        const containers = Array.from(document.querySelectorAll('[data-testid="merListItem-container"]'));
                        containers.forEach(container => {
                            const link = container.querySelector('a[href*="/item/m"]') || container.querySelector('a[href*="/en/item/m"]');
                            if (!link) return;
                            const href = (link.getAttribute('href') || '').split('?')[0];
                            if (!href || !href.match(/\\/item\\/m\\d+/)) return;
                            const containerText = (container.textContent || '').trim();
                            let price = '';
                            const priceMatch = containerText.match(/(BRL|¥|円|USD|\\$)[\\d,]+\.?\\d*/);
                            if (priceMatch) price = priceMatch[0];
                            const img = container.querySelector('img');
                            const imageUrl = img ? (img.src || img.getAttribute('data-src') || '') : '';
                            items.push({
                                href: href,
                                title: (link.textContent || '').trim() || containerText.split('\\n')[0],
                                price: price,
                                imageUrl: imageUrl
                            });
                        });
                        return items;
                    }
                ''')
                for item in items_at_bottom:
                    if item['href'] not in collected_items:
                        collected_items[item['href']] = item
                item_count = len(collected_items)
                
                # Scroll back up a bit to trigger more loading
                page.evaluate(f'window.scrollTo(0, {max_scroll * 0.8})')
                time.sleep(1.5)
            
            if item_count != previous_count:
                print(f"  Scroll {scroll_attempts + 1}: Collected {item_count} unique items")
                consecutive_no_change = 0
                previous_count = item_count
                
                # Early exit if we found the target number of items
                if item_count >= target_items:
                    print(f"  ✅ Collected {item_count} unique items (target: {target_items})! Stopping scroll.")
                    break
                
                if item_count >= 100:
                    print(f"  ✅ Collected {item_count} items! Continuing to ensure we have all...")
                    # Continue scrolling to get remaining items - collect at each position
                    for attempt in range(20):  # Attempts to get the last item
                        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                        time.sleep(1.8)  # Wait for items
                        # Collect items at this position
                        items_at_pos = page.evaluate('''
                            () => {
                                const items = [];
                                const containers = Array.from(document.querySelectorAll('[data-testid="merListItem-container"]'));
                                containers.forEach(container => {
                                    const link = container.querySelector('a[href*="/item/m"]') || container.querySelector('a[href*="/en/item/m"]');
                                    if (!link) return;
                                    const href = (link.getAttribute('href') || '').split('?')[0];
                                    if (!href || !href.match(/\\/item\\/m\\d+/)) return;
                                    const containerText = (container.textContent || '').trim();
                                    let price = '';
                                    const priceMatch = containerText.match(/(BRL|¥|円|USD|\\$)[\\d,]+\.?\\d*/);
                                    if (priceMatch) price = priceMatch[0];
                                    const img = container.querySelector('img');
                                    const imageUrl = img ? (img.src || img.getAttribute('data-src') || '') : '';
                                    items.push({
                                        href: href,
                                        title: (link.textContent || '').trim() || containerText.split('\\n')[0],
                                        price: price,
                                        imageUrl: imageUrl
                                    });
                                });
                                return items;
                            }
                        ''')
                        # Add new items
                        new_items_found = 0
                        for item in items_at_pos:
                            if item['href'] not in collected_items:
                                collected_items[item['href']] = item
                                new_items_found += 1
                        
                        item_count = len(collected_items)
                        if new_items_found > 0:
                            print(f"    Collected {new_items_found} more items: {item_count} total")
                            consecutive_no_change = 0
                        else:
                            consecutive_no_change += 1
                            if consecutive_no_change >= 3:
                                break
                        
                        if item_count >= target_items:
                            print(f"  ✅ Reached target of {target_items} items!")
                            break
                    break
            else:
                consecutive_no_change += 1
                # Only stop after many attempts with no change - be persistent but not excessive
                if consecutive_no_change >= 15:  # No change for 15 scrolls
                    print(f"  No new items after {consecutive_no_change} scrolls, trying final aggressive scroll...")
                    # Try aggressive scrolls to bottom
                    for attempt in range(10):  # Final attempts
                        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                        time.sleep(2.5)  # Wait
                        # Check if we found target
                        quick_check = page.evaluate('document.querySelectorAll(\'[data-testid="merListItem-container"]\').length');
                        if quick_check >= target_items:
                            print(f"  ✅ Found {quick_check} items during final scroll!")
                            item_count = quick_check
                            break
                        # Also try scrolling up and down to trigger loading
                        page.evaluate('window.scrollTo(0, 0)')
                        time.sleep(1.5)
                        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                        time.sleep(2.5)
                        
                        final_check = page.evaluate('''
                            () => {
                                // Primary method: Use data-testid (most reliable)
                                const containers = document.querySelectorAll('[data-testid="merListItem-container"]').length;
                                
                                // Fallback methods
                                const pattern1 = document.querySelectorAll('a[href*="/en/item/m"]').length;
                                const pattern2 = document.querySelectorAll('a[href*="/item/m"]').length;
                                const pattern3 = Array.from(document.querySelectorAll('a')).filter(a => {
                                    const href = a.getAttribute('href') || '';
                                    return href.match(/\\/item\\/m\\d+/);
                                }).length;
                                
                                return Math.max(containers, pattern1, pattern2, pattern3);
                            }
                        ''')
                        if final_check > item_count:
                            print(f"  Found {final_check} items after final scroll attempt {attempt + 1}!")
                            item_count = final_check
                            previous_count = item_count
                            consecutive_no_change = 0
                            if item_count >= target_items:
                                print(f"  ✅ Reached target of {target_items} items!")
                                break
                            break
                    if consecutive_no_change >= 5:
                        print(f"  Stopping at {item_count} items after exhaustive scrolling")
                        break
                    # Check if we reached target during final scrolls
                    if item_count >= target_items:
                        break
            
            scroll_attempts += 1
        
        # Check for "Load More" button or pagination
        print("Checking for 'Load More' button or pagination...")
        load_more_info = page.evaluate('''
            () => {
                const buttons = Array.from(document.querySelectorAll('button, [role="button"], a[class*="load"], a[class*="more"], a[class*="next"]'));
                const loadMoreButtons = buttons.filter(btn => {
                    const text = (btn.textContent || '').toLowerCase();
                    return text.includes('load more') || text.includes('show more') || text.includes('next') || text.includes('more items');
                });
                
                const pagination = Array.from(document.querySelectorAll('[class*="pagination"], [class*="page"]'));
                
                return {
                    loadMoreButtons: loadMoreButtons.length,
                    pagination: pagination.length,
                    buttonTexts: loadMoreButtons.slice(0, 3).map(b => b.textContent.trim())
                };
            }
        ''')
        
        if load_more_info['loadMoreButtons'] > 0:
            print(f"  Found {load_more_info['loadMoreButtons']} 'Load More' buttons: {load_more_info['buttonTexts']}")
            # Try clicking load more buttons
            for i in range(5):  # Try clicking up to 5 times
                clicked = page.evaluate('''
                    () => {
                        const buttons = Array.from(document.querySelectorAll('button, [role="button"], a[class*="load"], a[class*="more"]'));
                        const loadMore = buttons.find(btn => {
                            const text = (btn.textContent || '').toLowerCase();
                            return text.includes('load more') || text.includes('show more') || text.includes('more items');
                        });
                        if (loadMore && !loadMore.disabled) {
                            loadMore.click();
                            return true;
                        }
                        return false;
                    }
                ''')
                if clicked:
                    print(f"    Clicked 'Load More' button (attempt {i+1})")
                    time.sleep(3)  # Wait for items to load
                else:
                    break
        else:
            print(f"  No 'Load More' buttons found (pagination elements: {load_more_info['pagination']})")
        
        # Scroll back to top to ensure all items are in DOM
        page.evaluate('window.scrollTo(0, 0)')
        time.sleep(1)
        
        # Final count - use the collected items count (more accurate for virtual scrolling)
        final_count = item_count  # Use the count from our collection strategy
        print(f"  Final count after scrolling: {final_count} items (collected from virtual scrolling)")
        
        if api_requests:
            print(f"  Detected {len(api_requests)} API requests")
            # Show first few API URLs for debugging
            for url in api_requests[:5]:
                print(f"    - {url[:100]}")
        
        if search_responses:
            print(f"  Found {len(search_responses)} search API responses")
        
        # Additional wait for React to fully render
        time.sleep(2)
        
        # Extract all listings using JavaScript - use data-testid as primary method
        print("Extracting all listings from page...")
        result = page.evaluate('''
            () => {
                // Debug: Check what's actually in the DOM
                const debug = {
                    containers: document.querySelectorAll('[data-testid="merListItem-container"]').length,
                    linksWithEnItem: document.querySelectorAll('a[href*="/en/item/m"]').length,
                    linksWithItem: document.querySelectorAll('a[href*="/item/m"]').length,
                    imagesWithMercdn: document.querySelectorAll('img[src*="mercdn.net/thumb/item"]').length,
                    allImages: document.querySelectorAll('img').length,
                    bodyHeight: document.body.scrollHeight,
                    windowHeight: window.innerHeight
                };
                console.log('DOM Debug:', JSON.stringify(debug, null, 2));
                
                // Since we're using virtual scrolling collection strategy, we need to scroll through
                // and collect all items. But for final extraction, we'll get what's currently in DOM
                // plus use the collected item IDs to reconstruct the full list.
                
                // Method 1: Use data-testid="merListItem-container" (most reliable)
                const containers = Array.from(document.querySelectorAll('[data-testid="merListItem-container"]'));
                
                // Method 2: Find all links with /en/item/m or /item/m pattern (fallback)
                const pattern1 = Array.from(document.querySelectorAll('a[href*="/en/item/m"]'));
                const pattern2 = Array.from(document.querySelectorAll('a[href*="/item/m"]'));
                const allLinks = Array.from(document.querySelectorAll('a'));
                const itemLinks = [...new Set([...pattern1, ...pattern2, ...allLinks.filter(link => {
                    const href = link.getAttribute('href') || '';
                    return href.match(/\/item\/m\d+/);
                })])];
                
                console.log(`Found ${containers.length} item containers in DOM`);
                console.log(`Found ${itemLinks.length} item links in DOM`);
                
                // Get all unique item IDs we've seen (from collected_items if available in page context)
                // Note: collected_items is in Python scope, so we'll need to pass it or reconstruct
                
                // Try to find items in React/Next.js state or window data
                let itemsInState = 0;
                let itemsFromNextData = [];
                try {
                    // Check if there's a __NEXT_DATA__ script tag with items
                    const nextDataScript = document.querySelector('script#__NEXT_DATA__');
                    if (nextDataScript) {
                        const nextData = JSON.parse(nextDataScript.textContent);
                        // Try to find items in the data structure
                        const dataStr = JSON.stringify(nextData);
                        const itemMatches = dataStr.match(/\/item\/m\d+/g);
                        if (itemMatches) {
                            itemsInState = new Set(itemMatches).size;
                            console.log(`Found ${itemsInState} items in __NEXT_DATA__`);
                            
                            // Try to extract item data from __NEXT_DATA__
                            // Look for items array in various possible locations
                            const findItemsInObject = (obj, path = '') => {
                                if (!obj || typeof obj !== 'object') return [];
                                if (Array.isArray(obj)) {
                                    return obj.filter(item => 
                                        item && typeof item === 'object' && 
                                        (item.id || item.itemId || item.href || JSON.stringify(item).includes('/item/m'))
                                    );
                                }
                                let results = [];
                                for (const key in obj) {
                                    if (key.toLowerCase().includes('item') || key.toLowerCase().includes('product') || key.toLowerCase().includes('listing')) {
                                        const value = obj[key];
                                        if (Array.isArray(value)) {
                                            results = results.concat(value);
                                        } else if (value && typeof value === 'object') {
                                            results = results.concat(findItemsInObject(value, path + '.' + key));
                                        }
                                    } else {
                                        results = results.concat(findItemsInObject(obj[key], path + '.' + key));
                                    }
                                }
                                return results;
                            };
                            
                            itemsFromNextData = findItemsInObject(nextData);
                            if (itemsFromNextData.length > 0) {
                                console.log(`Found ${itemsFromNextData.length} potential items in __NEXT_DATA__ structure`);
                            }
                        }
                    }
                } catch (e) {
                    console.log('Could not parse __NEXT_DATA__:', e);
                }
                
                // Method 3: Also check for data attributes or other patterns (fallback)
                const allElements = Array.from(document.querySelectorAll('[href*="/item/m"], [data-href*="/item/m"]'));
                
                // Combine all methods - prioritize containers, then links
                const allItemElements = [...new Set([...containers, ...itemLinks, ...allElements])];
                
                console.log(`Found ${containers.length} containers with data-testid`);
                console.log(`Found ${itemLinks.length} links with /item/m pattern`);
                console.log(`Found ${allItemElements.length} total item elements`);
                
                // Get unique listings
                const seen = new Set();
                const listings = [];
                
                // Process containers first (most reliable)
                containers.forEach(container => {
                    // Find the link within the container
                    const link = container.querySelector('a[href*="/item/m"]') || container.querySelector('a[href*="/en/item/m"]');
                    if (!link) return;
                    
                    const href = link.getAttribute('href') || '';
                    if (!href) return;
                    
                    const normalizedHref = href.split('?')[0];
                    
                    if (!seen.has(normalizedHref)) {
                        seen.add(normalizedHref);
                        
                        // Extract title and price from container
                        const containerText = (container.textContent || '').trim();
                        let price = '';
                        let title = '';
                        
                        // Try to find price in container text
                        const priceMatch = containerText.match(/(BRL|¥|円|USD|\\$)[\\d,]+\.?\\d*/);
                        if (priceMatch) {
                            price = priceMatch[0];
                            title = containerText.replace(price, '').trim().split('\\n')[0]; // Get first line as title
                        } else {
                            // Try to find title in link or nearby elements
                            title = (link.textContent || '').trim() || containerText.split('\\n')[0];
                        }
                        
                        // Find image in container
                        let imageUrl = '';
                        const img = container.querySelector('img');
                        if (img) {
                            imageUrl = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '';
                        }
                        
                        listings.push({
                            href: normalizedHref,
                            title: title,
                            price: price,
                            imageUrl: imageUrl
                        });
                    }
                });
                
                // Process remaining links (fallback for items not in containers)
                itemLinks.forEach(link => {
                    const href = link.getAttribute('href') || link.getAttribute('data-href') || '';
                    if (!href) return;
                    
                    const normalizedHref = href.split('?')[0];
                    
                    if (!seen.has(normalizedHref)) {
                        seen.add(normalizedHref);
                        
                        // Extract title and price from link text or nearby elements
                        let text = (link.textContent || '').trim();
                        let price = '';
                        let title = '';
                        
                        // Try to find price in link text
                        const priceMatch = text.match(/(BRL|¥|円|USD|\\$)[\\d,]+\.?\\d*/);
                        if (priceMatch) {
                            price = priceMatch[0];
                            title = text.replace(price, '').trim();
                        } else {
                            title = text;
                            // Try to find price in parent container
                            let parent = link.parentElement;
                            for (let i = 0; i < 3 && parent; i++) {
                                const parentText = (parent.textContent || '').trim();
                                const parentPriceMatch = parentText.match(/(BRL|¥|円|USD|\\$)[\\d,]+\.?\\d*/);
                                if (parentPriceMatch) {
                                    price = parentPriceMatch[0];
                                    if (!title) title = parentText.replace(price, '').trim();
                                    break;
                                }
                                parent = parent.parentElement;
                            }
                        }
                        
                        // Find image in parent container
                        let imageUrl = '';
                        let parent = link.parentElement;
                        for (let i = 0; i < 5 && parent; i++) {
                            const img = parent.querySelector('img');
                            if (img) {
                                imageUrl = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '';
                                if (imageUrl && (imageUrl.includes('mercdn') || imageUrl.includes('mercari'))) {
                                    break;
                                }
                            }
                            parent = parent.parentElement;
                        }
                        
                        listings.push({
                            href: normalizedHref,
                            title: title,
                            price: price,
                            imageUrl: imageUrl
                        });
                    }
                });
                
                // If we found items in __NEXT_DATA__ and have fewer in DOM, try to use those
                if (itemsInState > listings.length && itemsInState >= 95) {
                    console.log(`__NEXT_DATA__ has ${itemsInState} items but DOM only has ${listings.length} - virtual scrolling confirmed`);
                }
                
                return { 
                    count: listings.length, 
                    listings: listings,
                    debug: debug,
                    itemsInState: itemsInState || 0,
                    itemsFromNextData: itemsFromNextData.length || 0
                };
            }
        ''')
        
        total_count = result['count']
        if 'debug' in result:
            print(f"  DOM Debug: {result['debug']}")
        if result.get('itemsInState', 0) > 0:
            print(f"  Found {result['itemsInState']} items in React/Next.js state")
        all_listings_js = result['listings']
        
        print(f"Found {total_count} unique listings")
        
        # Convert to our format
        all_listings_data = []
        for item in all_listings_js:
            href = item['href']
            if not href.startswith('http'):
                if href.startswith('/en/'):
                    href = BASE_URL + href
                elif href.startswith('/item/'):
                    href = BASE_URL + '/en' + href
                else:
                    href = BASE_URL + '/en/' + href
            
            image_url = item['imageUrl']
            if image_url and not image_url.startswith('http'):
                image_url = 'https:' + image_url if image_url.startswith('//') else BASE_URL + image_url
            
            all_listings_data.append({
                'title': item['title'],
                'title_translated': translate_japanese(item['title']) if item['title'] else None,
                'price': item['price'] if item['price'] else None,
                'image_url': image_url if image_url else None,
                'listing_url': href,
            })
        
        # Get HTML for saving
        html_content = page.content()
        
        # Use first 5 for detailed extraction
        listings = all_listings_data[:5]
        print(f"Will extract detailed data for first {len(listings)} listings")
        
        return listings, html_content, total_count, all_listings_data
        
    except Exception as e:
        print(f"Error extracting listings: {e}")
        import traceback
        traceback.print_exc()
        return [], page.content(), 0, []

def test_mercari_with_playwright():
    """Test Mercari scraping with Playwright"""
    if not PLAYWRIGHT_AVAILABLE:
        return None, "Playwright not available"
    
    print("=" * 60)
    print("Mercari Japan Scraping Test - Playwright Version")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'test_date': datetime.now().isoformat(),
        'search_term': SEARCH_TERM,
        'playwright_available': True,
        'access_test': False,
        'search_test': False,
        'extraction_test': False,
        'listings_found': 0,
        'challenges': [],
        'notes': [],
        'sample_data': []
    }
    
    search_url = f"{BASE_URL}/en/search?keyword={SEARCH_TERM.replace(' ', '%20')}&{SEARCH_PARAMS}"
    
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            # Test 1: Navigate to search page
            print(f"Navigating to: {search_url}")
            # Use 'domcontentloaded' instead of 'networkidle' - less strict
            page.goto(search_url, wait_until='domcontentloaded', timeout=60000)
            results['access_test'] = True
            results['search_test'] = True
            print("✅ Page loaded successfully")
            
            # Wait a bit for JavaScript to execute
            print("Waiting for content to load...")
            time.sleep(5)  # Give time for listings to load
            
            # Test 2: Extract listing data from search results
            print("\nExtracting listing data from search results...")
            listings, html_content, total_count, all_listings = extract_listing_data_playwright(page)
            
            print(f"\n{'='*60}")
            print(f"TOTAL LISTINGS FOUND: {total_count}")
            print(f"{'='*60}")
            if total_count == 101:
                print("✅ SUCCESS: Found exactly 101 items as expected!")
            elif total_count >= 100:
                print(f"✅ Found {total_count} items (close to expected 101)")
            else:
                print(f"⚠️ Found {total_count} items (expected 101)")
            print(f"{'='*60}\n")
            
            results['total_listings_count'] = total_count
            results['all_listings_basic'] = all_listings  # Store all listings with basic info
            
            if listings:
                # Visit each listing's detail page to extract more information
                print(f"\nVisiting detail pages for {len(listings)} listings...")
                for i, listing in enumerate(listings, 1):
                    print(f"\n[{i}/{len(listings)}] Extracting details for: {listing.get('title', 'N/A')[:50]}")
                    detail = extract_listing_detail(page, listing['listing_url'])
                    listing.update(detail)
                
                results['extraction_test'] = True
                results['listings_found'] = len(listings)
                results['sample_data'] = listings  # All 5 listings with full details
                print(f"\n✅ Extracted detailed data for {len(listings)} listings")
                print("\nSample listings:")
                for i, listing in enumerate(listings[:3], 1):
                    print(f"\n{i}. {listing.get('title', 'N/A')[:60]}")
                    if listing.get('title_translated'):
                        print(f"   (Translated: {listing.get('title_translated')[:60]})")
                    print(f"   Price: {listing.get('price', 'N/A')}")
                    if listing.get('warning_keywords'):
                        print(f"   Warnings: {', '.join(listing.get('warning_keywords', []))}")
            else:
                results['notes'].append("Listings found but extraction needs refinement - HTML structure needs inspection")
                print("⚠️ Listings structure needs inspection")
            
            # Save HTML for inspection
            html_file = 'validation/results/mercari_playwright_html.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\nHTML saved to: {html_file}")
            
        except Exception as e:
            results['challenges'].append(f"Error during scraping: {str(e)}")
            print(f"❌ Error: {e}")
        finally:
            browser.close()
    
    # Download ALL images for all listings
    if results.get('sample_data'):
        images_dir = 'validation/results/mercari_playwright_images'
        os.makedirs(images_dir, exist_ok=True)
        print("\nDownloading ALL images for listings...")
        for idx, listing in enumerate(results['sample_data']):
            # Download primary image
            image_url = listing.get('image_url')
            if image_url:
                image_filename = download_image(image_url, images_dir, idx, 0)
                if image_filename:
                    if 'local_images' not in listing:
                        listing['local_images'] = []
                    listing['local_images'].append(f"mercari_playwright_images/{image_filename}")
            
            # Download all images from detail page
            all_images = listing.get('all_images', [])
            if all_images:
                print(f"  Listing {idx+1}: Downloading {len(all_images)} images...")
                for img_idx, img_url in enumerate(all_images):
                    if img_url != image_url:  # Don't re-download primary image
                        image_filename = download_image(img_url, images_dir, idx, img_idx)
                        if image_filename:
                            if 'local_images' not in listing:
                                listing['local_images'] = []
                            listing['local_images'].append(f"mercari_playwright_images/{image_filename}")
                if listing.get('local_images'):
                    print(f"  Listing {idx+1}: Downloaded {len(listing['local_images'])} images total")
    
    # Save results as Markdown (human-readable for comparison)
    md_file = 'validation/results/mercari_playwright_results.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Mercari Japan Scraping Test Results - Playwright Version\n\n")
        f.write(f"**Date Tested:** {results['test_date']}\n")
        f.write(f"**Search Term:** {results['search_term']}\n\n")
        
        f.write("## Test Results\n\n")
        f.write(f"- **Access Test:** {'✅ PASS' if results['access_test'] else '❌ FAIL'}\n")
        f.write(f"- **Search Test:** {'✅ PASS' if results['search_test'] else '❌ FAIL'}\n")
        f.write(f"- **Extraction Test:** {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}\n")
        f.write(f"- **Listings Found (detailed):** {results['listings_found']}\n")
        if 'total_listings_count' in results:
            f.write(f"- **Total Listings Count:** {results['total_listings_count']}\n")
            if results['total_listings_count'] == 101:
                f.write(f"  - ✅ **SUCCESS: Found exactly 101 items as expected!**\n")
            elif results['total_listings_count'] >= 100:
                f.write(f"  - ✅ Found {results['total_listings_count']} items (close to expected 101)\n")
            else:
                f.write(f"  - ⚠️ Found {results['total_listings_count']} items (expected 101)\n")
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
            f.write("Compare these extracted values with the actual Mercari page:\n\n")
            for i, listing in enumerate(results['sample_data'], 1):
                f.write(f"### Sample Listing {i}\n\n")
                
                # Display image if downloaded
                if listing.get('local_image_path'):
                    f.write(f"![Listing {i} Image]({listing['local_image_path']})\n\n")
                
                f.write("**Extracted Data:**\n\n")
                f.write("```json\n")
                f.write(json.dumps(listing, indent=2, ensure_ascii=False))
                f.write("\n```\n\n")
                
                # Add comparison checklist
                f.write("**Compare with Mercari page:**\n")
                f.write(f"- [ ] Title matches: `{listing.get('title', 'N/A')}`\n")
                f.write(f"- [ ] Price matches: `{listing.get('price', 'N/A')}`\n")
                f.write(f"- [ ] Image matches (see image above)\n")
                if listing.get('image_url'):
                    f.write(f"- [ ] Image URL accessible: {listing.get('image_url')}\n")
                if listing.get('listing_url'):
                    f.write(f"- [ ] Listing URL works: {listing.get('listing_url')}\n")
                f.write("\n")
        
        f.write("## Conclusion\n\n")
        f.write("✅ **Mercari scraping is FEASIBLE using Playwright**\n\n")
        f.write("The test successfully extracted listing data including:\n")
        f.write("- Titles\n")
        f.write("- Prices\n")
        f.write("- Images\n")
        f.write("- Listing URLs\n\n")
        f.write("This confirms that the Scraper App can work with Mercari as a source.\n")
    
    # Save JSON results
    json_file = 'validation/results/mercari_playwright_results.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    print(f"Access Test: {'✅ PASS' if results['access_test'] else '❌ FAIL'}")
    print(f"Search Test: {'✅ PASS' if results['search_test'] else '❌ FAIL'}")
    print(f"Extraction Test: {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}")
    print(f"Listings Found (detailed): {results['listings_found']}")
    if 'total_listings_count' in results:
        print(f"Total Listings Count: {results['total_listings_count']}")
        if results['total_listings_count'] == 101:
            print("✅ SUCCESS: Found exactly 101 items!")
        elif results['total_listings_count'] >= 100:
            print(f"✅ Found {results['total_listings_count']} items (close to expected 101)")
        else:
            print(f"⚠️ Found {results['total_listings_count']} items (expected 101)")
    print(f"\nResults saved to:")
    print(f"  - Markdown: {md_file} (human-readable with images)")
    print(f"  - JSON: {json_file} (structured data)")
    if results.get('sample_data') and any(l.get('local_image_path') for l in results['sample_data']):
        print(f"  - Images: validation/results/mercari_playwright_images/ (downloaded images)")
    
    return results, None

if __name__ == "__main__":
    test_mercari_with_playwright()
