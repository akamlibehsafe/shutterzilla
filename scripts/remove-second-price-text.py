#!/usr/bin/env python3
"""
Remove text from the second price row for non-Yahoo Japan Auctions cards,
while keeping the structure for consistent spacing.
"""

import re
from pathlib import Path

def remove_second_price_text(html_file):
    """Remove text from second price row for non-Yahoo Japan Auctions cards."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match a card that is NOT yahoo-japan-auctions
    # We'll match cards and check if they have yahoo-japan-auctions, if not, process them
    # Match the entire card structure from opening <a> to closing </a>
    card_pattern = re.compile(
        r'(<a[^>]*class="card-link"[^>]*>.*?</a>)',
        re.DOTALL
    )
    
    def process_card(match):
        card_html = match.group(1)
        
        # Check if this is a Yahoo Japan Auctions card
        if 'data-shop="yahoo-japan-auctions"' in card_html:
            # Don't modify Yahoo Japan Auctions cards
            return card_html
        
        # For non-Yahoo cards, find and replace the second price row
        # Pattern to match the second card__price-row (the one after the first one)
        # We need to match: first row, then second row with Price label
        second_price_pattern = re.compile(
            r'(<div class="card__price-row">\s*<span class="card__price-label">Price</span>\s*<span class="card__price">[^<]+</span>\s*</div>\s*<div class="card__price-row">)\s*<span class="card__price-label">Price</span>\s*<span class="card__price">([^<]+)</span>\s*</div>',
            re.MULTILINE
        )
        
        def replace_second_price(m):
            # Keep the structure but remove the text
            return f'{m.group(1)}\n                  <span class="card__price-label"></span>\n                  <span class="card__price"></span>\n                </div>'
        
        card_html = second_price_pattern.sub(replace_second_price, card_html)
        
        return card_html
    
    # Process all cards
    content = card_pattern.sub(process_card, content)
    
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all HTML files in the mockups directory."""
    base_dir = Path(__file__).parent.parent / 'docs' / 'mockups' / 'current' / 'topbar-options-comparison' / 'option3'
    
    html_files = list(base_dir.glob('*.html'))
    
    updated_count = 0
    for html_file in html_files:
        if remove_second_price_text(html_file):
            print(f"Updated: {html_file.name}")
            updated_count += 1
    
    print(f"\nUpdated {updated_count} file(s)")

if __name__ == '__main__':
    main()
