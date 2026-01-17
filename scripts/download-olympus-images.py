#!/usr/bin/env python3
"""
Download Olympus OM-1N images from Buyee listing
Uses the existing Buyee scrapers to find a listing and extract images
"""

import sys
import os
import json
import time
from pathlib import Path

# Add parent directory to path to import scrapers
sys.path.insert(0, str(Path(__file__).parent.parent / 'validation' / 'scrapers'))

try:
    from buyee_search import main as search_main
    from buyee_details import scrape_listing_details
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError as e:
    print(f"Error importing scrapers: {e}")
    print("Make sure you're running from the project root")
    PLAYWRIGHT_AVAILABLE = False
    sys.exit(1)

import urllib.request
from urllib.parse import urlparse

def download_image(url, output_path):
    """Download an image from URL to output path"""
    try:
        print(f"  Downloading: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"  ✓ Saved: {output_path}")
        return True
    except Exception as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return False

def process_image(input_path, output_path, size="800x600"):
    """Resize and format image using ImageMagick"""
    try:
        from PIL import Image
        img = Image.open(input_path)
        # Resize maintaining aspect ratio, then crop to exact size
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        # Create new image with white background
        new_img = Image.new('RGB', (800, 600), 'white')
        # Paste centered
        x = (800 - img.width) // 2
        y = (600 - img.height) // 2
        new_img.paste(img, (x, y))
        new_img.save(output_path, 'PNG', quality=95)
        print(f"  ✓ Processed: {output_path}")
        return True
    except ImportError:
        # Fallback to ImageMagick command line
        try:
            import subprocess
            cmd = ['magick', 'convert', input_path, '-resize', f'{size}^', 
                   '-gravity', 'center', '-extent', size, 
                   '-background', 'white', '-quality', '90', output_path]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ Processed: {output_path}")
            return True
        except Exception as e:
            print(f"  ✗ Error processing image: {e}")
            # Just copy the file if processing fails
            import shutil
            shutil.copy(input_path, output_path)
            return False
    except Exception as e:
        print(f"  ✗ Error processing image: {e}")
        return False

def main():
    """Main function to find and download Olympus OM-1N images"""
    search_term = "Olympus OM-1N"
    target_dir = Path("docs/mockups/current/assets/cameras")
    temp_dir = target_dir / "temp_downloads"
    
    # Create directories
    target_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Olympus OM-1N Image Downloader")
    print("=" * 60)
    print(f"Search term: {search_term}")
    print(f"Target directory: {target_dir}")
    print("")
    
    if not PLAYWRIGHT_AVAILABLE:
        print("Error: Playwright not available")
        sys.exit(1)
    
    # Step 1: Search for listings
    print("Step 1: Searching for Olympus OM-1N listings on Buyee...")
    print("")
    
    results = search_main(search_term=search_term, output_file=str(temp_dir / "search_results.json"))
    
    if not results or 'all_listings_basic' not in results or not results['all_listings_basic']:
        print("Error: No listings found")
        sys.exit(1)
    
    listings = results['all_listings_basic']
    print(f"\nFound {len(listings)} listing(s)")
    
    # Find the first relevant listing
    om1n_listing = None
    for listing in listings:
        title = listing.get('title', '').lower()
        if 'om-1n' in title or 'om1n' in title or ('olympus' in title and 'om-1' in title):
            om1n_listing = listing
            break
    
    if not om1n_listing:
        # Use first listing if no specific match
        om1n_listing = listings[0]
        print(f"Using first listing: {om1n_listing.get('title', 'N/A')}")
    else:
        print(f"Found matching listing: {om1n_listing.get('title', 'N/A')}")
    
    listing_url = om1n_listing.get('listing_url')
    if not listing_url:
        print("Error: No listing URL found")
        sys.exit(1)
    
    print(f"Listing URL: {listing_url}")
    print("")
    
    # Step 2: Scrape details to get all images
    print("Step 2: Scraping listing details to extract all images...")
    print("")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            locale='ja-JP',
            timezone_id='Asia/Tokyo'
        )
        page = context.new_page()
        
        try:
            detail = scrape_listing_details(page, listing_url)
            all_images = detail.get('all_images', [])
            
            if not all_images:
                print("Warning: No images found in listing details")
                # Try to use thumbnail from search results
                thumbnail_url = om1n_listing.get('image_url')
                if thumbnail_url:
                    all_images = [thumbnail_url]
                    print(f"Using thumbnail from search results")
            
            print(f"Found {len(all_images)} image(s)")
            print("")
        finally:
            browser.close()
    
    if not all_images:
        print("Error: No images available to download")
        sys.exit(1)
    
    # Step 3: Download images
    print("Step 3: Downloading and processing images...")
    print("")
    
    # We need 4 images: main, and 3 more for thumbnails
    # Download first 4 images (or use first image 4 times if only 1 available)
    images_to_download = all_images[:4] if len(all_images) >= 4 else [all_images[0]] * 4
    
    image_files = []
    for i, img_url in enumerate(images_to_download, 1):
        if i == 1:
            filename = "olympus-om1n.png"
        else:
            filename = f"olympus-om1n-{i-1}.png"
        
        temp_file = temp_dir / f"temp_{filename}"
        final_file = target_dir / filename
        
        # Download
        if download_image(img_url, temp_file):
            # Process (resize and format)
            if process_image(temp_file, final_file):
                image_files.append(final_file)
                # Clean up temp file
                temp_file.unlink()
    
    print("")
    print("=" * 60)
    print("Download Complete!")
    print("=" * 60)
    print(f"Downloaded {len(image_files)} image(s):")
    for img_file in image_files:
        print(f"  - {img_file}")
    print("")
    print("Images are ready to use in the mockups!")

if __name__ == "__main__":
    main()
