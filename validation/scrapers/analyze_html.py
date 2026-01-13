#!/usr/bin/env python3
"""Quick script to analyze the HTML structure and find items"""

import json
import re
from html.parser import HTMLParser

# Read the HTML from stdin or file
html_content = input() if True else open('validation/results/mercari_playwright_html.html').read()

# Find __NEXT_DATA__ script tag
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_content, re.DOTALL)
if next_data_match:
    try:
        next_data = json.loads(next_data_match.group(1))
        print("✅ Found __NEXT_DATA__ script tag")
        
        # Search for item URLs in the JSON
        data_str = json.dumps(next_data)
        item_matches = re.findall(r'/item/m\d+', data_str)
        unique_items = set(item_matches)
        print(f"Found {len(unique_items)} unique item URLs in __NEXT_DATA__")
        
        if len(unique_items) > 0:
            print(f"\nFirst 10 item IDs:")
            for item in list(unique_items)[:10]:
                print(f"  - {item}")
        
        # Try to find the actual items array
        def find_items(obj, path=""):
            """Recursively search for items array"""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if 'item' in key.lower() or 'product' in key.lower() or 'listing' in key.lower():
                        if isinstance(value, list) and len(value) > 0:
                            print(f"\nFound potential items array at: {path}.{key} (length: {len(value)})")
                            if len(value) > 0:
                                print(f"  First item keys: {list(value[0].keys()) if isinstance(value[0], dict) else 'not a dict'}")
                    find_items(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_items(item, f"{path}[{i}]")
        
        print("\nSearching for items array in __NEXT_DATA__...")
        find_items(next_data)
        
    except json.JSONDecodeError as e:
        print(f"❌ Could not parse __NEXT_DATA__: {e}")
else:
    print("❌ Could not find __NEXT_DATA__ script tag")

# Also check for item links in the HTML
item_links = re.findall(r'href=["\']([^"\']*?/item/m\d+[^"\']*?)["\']', html_content)
unique_links = set(item_links)
print(f"\nFound {len(unique_links)} unique item links in HTML")
if len(unique_links) > 0:
    print(f"\nFirst 10 links:")
    for link in list(unique_links)[:10]:
        print(f"  - {link}")
