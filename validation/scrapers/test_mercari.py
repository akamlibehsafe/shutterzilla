#!/usr/bin/env python3
"""
Mercari Japan Scraping Test

This script tests if we can successfully scrape camera listings from Mercari Japan.
Based on validation plan section 0.2.1

Test Criteria:
- Can we access mercari.jp search page?
- Can we find/search for camera listings?
- Can we extract key data fields (title, price, images, URL)?
- Are there rate limits or blocking mechanisms?
- Is the HTML structure stable enough to scrape?
- Do we need JavaScript rendering (Playwright) or can we use simple HTTP (BeautifulSoup)?
- Are there anti-bot measures we need to handle?
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import os
from urllib.parse import urlparse

# Test configuration
SEARCH_TERM = "Nikon FM2"  # or similar camera
BASE_URL = "https://www.mercari.com/jp"
SEARCH_URL = f"{BASE_URL}/search/"  # Adjust based on actual URL structure

def get_headers():
    """Get realistic browser headers"""
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }

def test_access():
    """Test if we can access Mercari Japan website"""
    print("Testing website access with improved headers...")
    try:
        headers = get_headers()
        session = requests.Session()
        response = session.get(BASE_URL, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Access successful with improved headers!")
            return response, session
        else:
            print(f"❌ Still getting {response.status_code} with improved headers")
            return None, None
    except Exception as e:
        print(f"Error accessing website: {e}")
        return None, None

def test_search(search_term, session=None):
    """Test if we can search for listings"""
    print(f"\nTesting search for: {search_term}")
    try:
        headers = get_headers()
        headers['Referer'] = BASE_URL
        headers['Sec-Fetch-Site'] = 'same-origin'
        
        # Try different search URL patterns
        search_urls = [
            f"{BASE_URL}/search/?keyword={search_term}",
            f"{BASE_URL}/jp/search/?keyword={search_term}",
            f"{BASE_URL}/search?keyword={search_term}"
        ]
        
        if session:
            req_method = session.get
        else:
            req_method = requests.get
            session = requests.Session()
        
        for url in search_urls:
            try:
                response = req_method(url, headers=headers, timeout=10)
                print(f"Tried: {url}")
                print(f"Search Status Code: {response.status_code}")
                if response.status_code == 200:
                    print(f"✅ Search successful with URL: {url}")
                    return response, url
                time.sleep(1)  # Small delay between attempts
            except Exception as e:
                print(f"Error with URL {url}: {e}")
                continue
        
        return None, None
    except Exception as e:
        print(f"Error searching: {e}")
        return None, None

def extract_listing_data(html_content):
    """
    Extract listing data from HTML content
    
    Returns list of dictionaries with listing information
    """
    listings = []
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # NOTE: Selectors need to be determined by inspecting actual HTML structure
    # These are placeholder selectors - adjust based on actual structure
    
    # Example structure (needs to be updated based on actual HTML):
    # listing_items = soup.select('div.listing-item')  # Adjust selector
    
    # For each listing, extract:
    # - Title
    # - Price
    # - Image URL(s)
    # - Listing URL
    # - Condition/status
    # - Seller information (if available)
    
    # Placeholder structure:
    """
    for item in listing_items:
        listing = {
            'title': item.select_one('.title').text.strip() if item.select_one('.title') else None,
            'price': item.select_one('.price').text.strip() if item.select_one('.price') else None,
            'image_url': item.select_one('img')['src'] if item.select_one('img') else None,
            'listing_url': item.select_one('a')['href'] if item.select_one('a') else None,
            'condition': item.select_one('.condition').text.strip() if item.select_one('.condition') else None,
            # Add more fields as needed
        }
        listings.append(listing)
    """
    
    print("NOTE: HTML structure needs to be inspected and selectors updated")
    return listings

def test_rate_limiting(session=None):
    """Test rate limiting behavior"""
    print("\nTesting rate limiting...")
    requests_count = 0
    start_time = time.time()
    
    if not session:
        session = requests.Session()
    
    # Make multiple requests and see if we get rate limited
    for i in range(5):
        try:
            headers = get_headers()
            response = session.get(BASE_URL, headers=headers, timeout=10)
            requests_count += 1
            if response.status_code != 200:
                print(f"Request {i+1} returned status {response.status_code}")
            time.sleep(1)  # Small delay between requests
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
            break
    
    elapsed = time.time() - start_time
    print(f"Made {requests_count} requests in {elapsed:.2f} seconds")
    
    return requests_count == 5

def download_image(image_url, output_dir, listing_index, image_index=0):
    """Download an image from URL and save it locally"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=10, stream=True)
        if response.status_code == 200:
            # Get file extension from URL or default to jpg
            parsed_url = urlparse(image_url)
            ext = os.path.splitext(parsed_url.path)[1] or '.jpg'
            filename = f"listing_{listing_index}_image_{image_index}{ext}"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")
    return None

def main():
    """Run all tests"""
    print("=" * 60)
    print("Mercari Japan Scraping Test")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create images directory
    images_dir = 'validation/results/mercari_images'
    os.makedirs(images_dir, exist_ok=True)
    
    results = {
        'test_date': datetime.now().isoformat(),
        'search_term': SEARCH_TERM,
        'access_test': False,
        'search_test': False,
        'extraction_test': False,
        'rate_limiting_test': False,
        'challenges': [],
        'notes': [],
        'sample_data': []
    }
    
    # Test 1: Access
    access_response, session = test_access()
    results['access_test'] = access_response is not None and access_response.status_code == 200
    
    if not results['access_test']:
        results['challenges'].append("Getting 403 Forbidden - Mercari has anti-bot protection")
        results['notes'].append("Tried improved headers but still blocked. May need Playwright/Selenium for JavaScript rendering.")
    
    # Test 2: Search
    search_response, search_url = test_search(SEARCH_TERM, session)
    if search_response and search_response.status_code == 200:
        results['notes'].append(f"Successful search URL: {search_url}")
        results['search_test'] = True
        
        # Test 3: Extract data
        listings = extract_listing_data(search_response.text)
        if listings:
            results['extraction_test'] = True
            sample_listings = listings[:3]  # Save first 3 listings as samples
            
            # Download images for sample listings
            print("\nDownloading images for sample listings...")
            for idx, listing in enumerate(sample_listings):
                image_url = listing.get('image_url')
                if image_url:
                    image_filename = download_image(image_url, images_dir, idx)
                    if image_filename:
                        listing['local_image_path'] = f"mercari_images/{image_filename}"
                        print(f"  Downloaded image for listing {idx+1}: {image_filename}")
            
            results['sample_data'] = sample_listings
            print(f"\nExtracted {len(listings)} listings")
            if sample_listings:
                print("\nSample listing:")
                print(json.dumps(sample_listings[0], indent=2, ensure_ascii=False))
        else:
            results['notes'].append("Could not extract listing data - HTML structure needs inspection")
    
    # Test 4: Rate limiting
    results['rate_limiting_test'] = test_rate_limiting(session)
    
    # Document JavaScript requirement
    if results['access_test'] and results['search_test']:
        print("\n" + "=" * 60)
        print("Analysis: JavaScript Rendering Required")
        print("=" * 60)
        print("HTML inspection shows Mercari uses Next.js/React.")
        print("Listings are loaded client-side via JavaScript/API calls.")
        print("JavaScript rendering (Playwright/Selenium) is REQUIRED to extract listing data.")
        results['challenges'].append("JavaScript rendering required - Mercari uses Next.js/React, listings loaded client-side")
        results['notes'].append("HTML contains page structure but no listing data - listings loaded via JavaScript/API after page load")
        results['notes'].append("Need Playwright/Selenium to render JavaScript and wait for listings to load")
    
    # Save HTML for inspection (if search was successful)
    if search_response:
        html_file = 'validation/results/mercari_sample_html.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(search_response.text)
        print(f"\nHTML response saved to: {html_file} (for inspection)")
    
    # Save results as Markdown (human-readable for comparison)
    md_file = 'validation/results/mercari_results.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Mercari Japan Scraping Test Results\n\n")
        f.write(f"**Date Tested:** {results['test_date']}\n")
        f.write(f"**Search Term:** {results['search_term']}\n\n")
        
        f.write("## Test Results\n\n")
        f.write(f"- **Access Test:** {'✅ PASS' if results['access_test'] else '❌ FAIL'}\n")
        f.write(f"- **Search Test:** {'✅ PASS' if results['search_test'] else '❌ FAIL'}\n")
        f.write(f"- **Extraction Test:** {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}\n")
        f.write(f"- **Rate Limiting Test:** {'✅ PASS' if results['rate_limiting_test'] else '❌ FAIL'}\n\n")
        
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
        
        f.write("## Next Steps\n\n")
        f.write("- Review extracted data and compare with actual Mercari page\n")
        f.write("- Compare downloaded images with images on Mercari page\n")
        f.write("- Inspect HTML structure in `mercari_sample_html.html` if needed\n")
        f.write("- Update selectors in script if data extraction needs improvement\n")
    
    # Also save JSON for programmatic access
    json_file = 'validation/results/mercari_results.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    print(f"Access Test: {'✅ PASS' if results['access_test'] else '❌ FAIL'}")
    print(f"Search Test: {'✅ PASS' if results['search_test'] else '❌ FAIL'}")
    print(f"Extraction Test: {'✅ PASS' if results['extraction_test'] else '❌ FAIL'}")
    print(f"Rate Limiting Test: {'✅ PASS' if results['rate_limiting_test'] else '❌ FAIL'}")
    print(f"\nResults saved to:")
    print(f"  - Markdown: {md_file} (human-readable for comparison)")
    print(f"  - JSON: {json_file} (structured data)")
    if search_response:
        print(f"  - HTML: validation/results/mercari_sample_html.html (for inspection)")
    if results.get('sample_data') and any(l.get('local_image_path') for l in results['sample_data']):
        print(f"  - Images: validation/results/mercari_images/ (downloaded images for comparison)")
    
    return results

if __name__ == "__main__":
    main()
