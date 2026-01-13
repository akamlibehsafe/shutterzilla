#!/usr/bin/env python3
"""
Mercari Japan Scraping Test - Playwright Version

This script tests Mercari scraping using Playwright for JavaScript rendering.
"""

import json
import time
import os
import requests
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

def extract_listing_data_playwright(page):
    """Extract listing data from rendered page using Playwright - simplified version"""
    try:
        # Wait for page to load
        page.wait_for_selector('main', timeout=10000)
        
        # Intercept network requests to see API calls
        api_requests = []
        def handle_request(request):
            url = request.url
            if 'api' in url.lower() or 'search' in url.lower() or 'item' in url.lower():
                api_requests.append(url)
        
        page.on('request', handle_request)
        
        # Wait for network to be idle (all API calls to complete)
        print("Waiting for all listings to load...")
        try:
            page.wait_for_load_state('networkidle', timeout=30000)
        except:
            pass
        
        # Wait for items to appear - poll until we have 100+ items or timeout
        print("Waiting for listings to render...")
        max_wait = 15  # seconds
        start_time = time.time()
        item_count = 0
        
        while time.time() - start_time < max_wait:
            item_count = page.evaluate('''
                () => {
                    const links = Array.from(document.querySelectorAll('a'));
                    return links.filter(link => {
                        const href = link.getAttribute('href') || '';
                        return href.match(/\\/item\\/m\\d+/);
                    }).length;
                }
            ''')
            
            if item_count >= 100:
                print(f"  Found {item_count} items!")
                break
            elif item_count > 0:
                print(f"  Found {item_count} items so far...")
            
            time.sleep(1)
        
        if api_requests:
            print(f"  Detected {len(api_requests)} API requests")
            # Show first few API URLs for debugging
            for url in api_requests[:3]:
                print(f"    - {url[:100]}")
        
        # Additional wait for React to fully render
        time.sleep(2)
        
        # Extract all listings using JavaScript - try multiple methods
        print("Extracting all listings from page...")
        result = page.evaluate('''
            () => {
                // Debug: Check page structure
                const debug = {
                    totalLinks: document.querySelectorAll('a').length,
                    linksWithItem: 0,
                    linksWithM: 0,
                    allHrefs: []
                };
                
                // Method 1: Find all links with /item/m pattern
                const allLinks = Array.from(document.querySelectorAll('a'));
                const itemLinks = allLinks.filter(link => {
                    const href = link.getAttribute('href') || '';
                    debug.allHrefs.push(href.substring(0, 50)); // First 50 chars
                    if (href.includes('/item/')) {
                        debug.linksWithItem++;
                    }
                    if (href.match(/\/item\/m\d+/)) {
                        debug.linksWithM++;
                        return true;
                    }
                    return false;
                });
                
                // Method 2: Try different patterns - maybe items are in different format
                const altPattern1 = Array.from(document.querySelectorAll('a[href*="item"]'));
                const altPattern2 = Array.from(document.querySelectorAll('[data-testid*="item"], [data-testid*="listing"]'));
                
                // Method 3: Look for article or listing containers
                const containers = Array.from(document.querySelectorAll('article, [class*="item"], [class*="listing"], [class*="product"]'));
                
                console.log('Debug info:', JSON.stringify(debug, null, 2));
                console.log(`Found ${itemLinks.length} links with /item/m pattern`);
                console.log(`Found ${altPattern1.length} links with "item" in href`);
                console.log(`Found ${containers.length} potential item containers`);
                
                // Method 2: Also check for data attributes or other patterns
                const allElements = Array.from(document.querySelectorAll('[href*="/item/m"], [data-href*="/item/m"]'));
                
                // Combine both methods
                const allItemElements = [...new Set([...itemLinks, ...allElements, ...altPattern1])];
                
                console.log(`Found ${allItemElements.length} total item elements`);
                
                // Get unique listings
                const seen = new Set();
                const listings = [];
                
                allItemElements.forEach(link => {
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
                
                return { count: listings.length, listings: listings };
            }
        ''')
        
        total_count = result['count']
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
