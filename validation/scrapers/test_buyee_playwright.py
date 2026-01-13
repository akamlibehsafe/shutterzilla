#!/usr/bin/env python3
"""
Buyee Scraping Test - Playwright Version

This script tests Buyee scraping using Playwright for JavaScript rendering.
Buyee is a proxy service for Japanese marketplaces (Mercari, Yahoo Auctions, etc.)
"""

import json
import time
import os
import requests
from datetime import datetime
from urllib.parse import urlparse, quote

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")

# Test configuration
SEARCH_TERM = "Nikon FM2"
BASE_URL = "https://buyee.jp"

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

def extract_listing_data_playwright(page):
    """Extract listing data from rendered Buyee page using Playwright"""
    try:
        # Wait for page to load
        print("Waiting for page to load...")
        page.wait_for_load_state('networkidle', timeout=30000)
        time.sleep(3)  # Additional wait for content to render
        
        # Extract listings using JavaScript
        print("Extracting listings from page...")
        listings_data = page.evaluate('''
            () => {
                const listings = [];
                
                // Try multiple selector patterns for Buyee listings
                const selectors = [
                    'div.item-card',
                    'div.product-item',
                    'div.search-result-item',
                    'div[class*="item"]',
                    'div[class*="product"]',
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
                    const allLinks = Array.from(document.querySelectorAll('a[href*="/item/"]'));
                    if (allLinks.length > 0) {
                        console.log(`Found ${allLinks.length} item links`);
                        items = allLinks.map(link => link.closest('div') || link.parentElement || link);
                    }
                }
                
                items.forEach((item, index) => {
                    const listing = {};
                    
                    // Extract title
                    const titleSelectors = ['h2', 'h3', '.title', '.item-title', '[class*="title"]'];
                    for (const sel of titleSelectors) {
                        const titleElem = item.querySelector(sel);
                        if (titleElem) {
                            listing.title = titleElem.textContent.trim();
                            break;
                        }
                    }
                    if (!listing.title) {
                        const link = item.querySelector('a');
                        if (link) listing.title = link.textContent.trim();
                    }
                    
                    // Extract price
                    const priceSelectors = ['.price', '.item-price', '[class*="price"]'];
                    for (const sel of priceSelectors) {
                        const priceElem = item.querySelector(sel);
                        if (priceElem) {
                            listing.price = priceElem.textContent.trim();
                            break;
                        }
                    }
                    
                    // Extract image
                    const img = item.querySelector('img');
                    if (img) {
                        listing.imageUrl = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '';
                    }
                    
                    // Extract URL
                    const link = item.querySelector('a[href*="/item/"]') || item.querySelector('a');
                    if (link) {
                        let href = link.getAttribute('href');
                        if (href && !href.startsWith('http')) {
                            href = 'https://buyee.jp' + href;
                        }
                        listing.href = href || '';
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
                        bodyText: document.body.textContent.substring(0, 200)
                    }
                };
            }
        ''')
        
        listings = listings_data.get('listings', [])
        count = listings_data.get('count', 0)
        
        print(f"  Found {count} listings")
        if listings_data.get('debug'):
            print(f"  Debug: {listings_data['debug']}")
        
        # Convert to our format
        all_listings = []
        for item in listings:
            href = item.get('href', '')
            if not href.startswith('http'):
                href = BASE_URL + href if href.startswith('/') else BASE_URL + '/' + href
            
            all_listings.append({
                'title': item.get('title', ''),
                'price': item.get('price', ''),
                'image_url': item.get('imageUrl', ''),
                'listing_url': href,
            })
        
        # Get HTML for inspection
        html_content = page.content()
        
        # Return first 5 for detailed extraction, plus all listings
        return all_listings[:5], html_content, count, all_listings
        
    except Exception as e:
        print(f"Error extracting listing data: {e}")
        import traceback
        traceback.print_exc()
        return [], page.content(), 0, []

def extract_listing_detail(page, listing_url):
    """Extract detailed information from a single listing page"""
    try:
        print(f"  Navigating to: {listing_url}")
        page.goto(listing_url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(2)
        
        detail = page.evaluate('''
            () => {
                const detail = {};
                
                // Extract all images
                const images = Array.from(document.querySelectorAll('img[src*="buyee"]'))
                    .map(img => img.src || img.getAttribute('data-src') || '')
                    .filter(src => src && src.includes('buyee'));
                detail.all_images = images;
                
                // Extract description
                const descSelectors = ['.description', '.item-description', '[class*="description"]'];
                for (const sel of descSelectors) {
                    const desc = document.querySelector(sel);
                    if (desc) {
                        detail.description = desc.textContent.trim();
                        break;
                    }
                }
                
                return detail;
            }
        ''')
        
        return detail
    except Exception as e:
        print(f"  Error extracting detail: {e}")
        return {}

if __name__ == "__main__":
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright is not available. Please install it first.")
        exit(1)
    
    print("=" * 60)
    print("Buyee Scraping Test - Playwright Version")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'test_date': datetime.now().isoformat(),
        'search_term': SEARCH_TERM,
        'access_test': False,
        'search_test': False,
        'extraction_test': False,
        'listings_found': 0,
        'challenges': [],
        'notes': [],
        'sample_data': []
    }
    
    search_url = f"{BASE_URL}/item/search?keyword={quote(SEARCH_TERM)}"
    
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
            page.goto(search_url, wait_until='domcontentloaded', timeout=60000)
            results['access_test'] = True
            results['search_test'] = True
            print("✅ Page loaded successfully")
            
            # Test 2: Extract listing data
            print("\nExtracting listing data from search results...")
            listings, html_content, total_count, all_listings = extract_listing_data_playwright(page)
            
            print(f"\n{'='*60}")
            print(f"TOTAL LISTINGS FOUND: {total_count}")
            print(f"{'='*60}\n")
            
            results['total_listings_count'] = total_count
            results['all_listings_basic'] = all_listings
            
            if listings:
                # Visit detail pages for first few listings
                print(f"\nVisiting detail pages for {len(listings)} listings...")
                for i, listing in enumerate(listings, 1):
                    print(f"\n[{i}/{len(listings)}] Extracting details for: {listing.get('title', 'N/A')[:50]}")
                    detail = extract_listing_detail(page, listing['listing_url'])
                    listing.update(detail)
                
                results['extraction_test'] = True
                results['listings_found'] = len(listings)
                results['sample_data'] = listings
                print(f"\n✅ Extracted detailed data for {len(listings)} listings")
            else:
                results['notes'].append("No listings found - HTML structure needs inspection")
                print("⚠️ No listings found - HTML structure needs inspection")
            
            # Save HTML for inspection
            html_file = 'validation/results/buyee_playwright_html.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\nHTML saved to: {html_file}")
            
        except Exception as e:
            results['challenges'].append(f"Error during scraping: {str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()
    
    # Download images
    if results.get('sample_data'):
        images_dir = 'validation/results/buyee_playwright_images'
        os.makedirs(images_dir, exist_ok=True)
        print("\nDownloading images for listings...")
        for idx, listing in enumerate(results['sample_data']):
            image_url = listing.get('image_url')
            if image_url:
                image_filename = download_image(image_url, images_dir, idx, 0)
                if image_filename:
                    listing['local_image_path'] = f"buyee_playwright_images/{image_filename}"
    
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
                f.write(f"### Sample Listing {i}\n\n")
                if listing.get('local_image_path'):
                    f.write(f"![Listing {i} Image]({listing['local_image_path']})\n\n")
                f.write("```json\n")
                f.write(json.dumps(listing, indent=2, ensure_ascii=False))
                f.write("\n```\n\n")
    
    json_file = 'validation/results/buyee_playwright_results.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    print(f"Access Test: {'✅ PASS' if results['access_test'] else '❌ FAIL'}")
    print(f"Search Test: {'✅ PASS' if results['search_test'] else '❌ FAIL'}")
    print(f"Extraction Test: {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}")
    print(f"Listings Found: {results['listings_found']}")
    if 'total_listings_count' in results:
        print(f"Total Listings Count: {results['total_listings_count']}")
    print(f"\nResults saved to:")
    print(f"  - Markdown: {md_file}")
    print(f"  - JSON: {json_file}")
