#!/usr/bin/env python3
"""
Debug script to inspect a single Mercari listing
"""

from playwright.sync_api import sync_playwright
import time
import json
from bs4 import BeautifulSoup
import re

LISTING_URL = "https://www.mercari.com/jp/item/m26068059510"

def debug_listing(url):
    """Debug a single listing to understand its structure"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        print(f"Visiting: {url}")
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        time.sleep(5)  # Wait for page to load
        
        # Check if we got blocked
        page_title = page.title()
        print(f"\nPage Title: {page_title}")
        
        if "Just a moment" in page_title or "Cloudflare" in page_title:
            print("⚠️ WARNING: Page appears to be blocked by Cloudflare")
            print("This is a common anti-bot protection. We may need to:")
            print("  - Wait longer for the page to load")
            print("  - Use different browser settings")
            print("  - Handle Cloudflare challenges")
        
        # Save HTML for inspection
        html = page.content()
        with open('/tmp/mercari_listing.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\nHTML saved to /tmp/mercari_listing.html")
        
        # Try JavaScript extraction
        print("\n=== Trying JavaScript extraction ===")
        data = page.evaluate('''
            () => {
                const result = {
                    title: document.title,
                    url: window.location.href,
                    images: [],
                    textSnippets: []
                };
                
                // Get all images
                document.querySelectorAll('img').forEach(img => {
                    const src = img.src || img.getAttribute('data-src') || '';
                    if (src) {
                        result.images.push({
                            src: src.substring(0, 150),
                            alt: (img.alt || '').substring(0, 50)
                        });
                    }
                });
                
                // Get text content (first 1000 chars)
                result.textSnippets = document.body.innerText.substring(0, 1000);
                
                return result;
            }
        ''')
        
        print(f"\nFound {len(data['images'])} images total")
        print("\nFirst 15 images found:")
        for i, img in enumerate(data['images'][:15], 1):
            print(f"{i:2d}. {img['src'][:100]}")
            if img['alt']:
                print(f"    alt: {img['alt']}")
        
        # Look for product images specifically
        print("\n=== Product images (containing 'item' in URL) ===")
        product_images = [img for img in data['images'] if '/item/' in img['src'] or 'item' in img['src'].lower()]
        print(f"Found {len(product_images)} potential product images")
        for img in product_images:
            print(f"  {img['src']}")
        
        # Try to find images with static.mercdn.net
        print("\n=== Images from static.mercdn.net ===")
        mercdn_images = [img for img in data['images'] if 'static.mercdn.net' in img['src']]
        print(f"Found {len(mercdn_images)} images from mercdn.net")
        for img in mercdn_images[:10]:
            print(f"  {img['src']}")
        
        # Show some text to see what's on the page
        print(f"\n=== Page text (first 500 chars) ===")
        print(data['textSnippets'][:500])
        
        browser.close()
        
        return data

if __name__ == "__main__":
    debug_listing(LISTING_URL)
