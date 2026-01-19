#!/usr/bin/env python3
"""
Update all cards to have a two-line price structure.
For Yahoo Japan Auctions: "Current Price" + "Buyout Price"
For other cards: "Price" + "Price" (same value)
"""

import re
from pathlib import Path

def update_card_prices(html_file):
    """Update price structure in a single HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: Yahoo Japan Auctions cards with two prices in card__prices div
    # Match the structure: <div class="card__prices">...two prices...</div>
    pattern_yahoo_two = re.compile(
        r'(<div class="card__prices">)\s*'
        r'<span class="card__price">([^<]+)</span>\s*'
        r'<span class="card__price card__price--buyout">([^<]+)</span>\s*'
        r'</div>',
        re.MULTILINE
    )
    
    def replace_yahoo_two(match):
        current_price = match.group(2).strip()
        buyout_price = match.group(3).strip()
        return f'''<div class="card__prices">
                <div class="card__price-row">
                  <span class="card__price-label">Current Price</span>
                  <span class="card__price">{current_price}</span>
                </div>
                <div class="card__price-row">
                  <span class="card__price-label">Buyout Price</span>
                  <span class="card__price card__price--buyout">{buyout_price}</span>
                </div>
              </div>'''
    
    content = pattern_yahoo_two.sub(replace_yahoo_two, content)
    
    # Pattern 2: Single price (either <span class="card__price"> or already in card__prices but single)
    # We need to be careful - only replace if it's NOT already handled by pattern 1
    # Match: <span class="card__price">¥89,850</span> followed by <div class="card__actions">
    pattern_single = re.compile(
        r'(<div class="card__meta">)\s*'
        r'<span class="card__price">([^<]+)</span>\s*'
        r'(<div class="card__actions">)',
        re.MULTILINE
    )
    
    def replace_single(match):
        price = match.group(2).strip()
        return f'''<div class="card__meta">
              <div class="card__prices">
                <div class="card__price-row">
                  <span class="card__price-label">Price</span>
                  <span class="card__price">{price}</span>
                </div>
                <div class="card__price-row">
                  <span class="card__price-label">Price</span>
                  <span class="card__price">{price}</span>
                </div>
              </div>
              <div class="card__actions">'''
    
    content = pattern_single.sub(replace_single, content)
    
    # Pattern 3: Fix Yahoo Japan Auctions cards that got "Price" labels but should have "Current Price" and "Buyout Price"
    # Find cards with data-shop="yahoo-japan-auctions" that have "Price" labels
    # We need to check if the card-link has yahoo-japan-auctions attribute
    def fix_yahoo_labels(match_content):
        # Find all card sections
        card_sections = re.finditer(
            r'(<a[^>]*data-shop="yahoo-japan-auctions"[^>]*>.*?</a>)',
            match_content,
            re.DOTALL
        )
        
        for card_match in card_sections:
            card_html = card_match.group(1)
            # Check if it has "Price" labels (not "Current Price")
            if 'card__price-label">Price</span>' in card_html:
                # Extract the price value
                price_match = re.search(r'<span class="card__price">([^<]+)</span>', card_html)
                if price_match:
                    price = price_match.group(1).strip()
                    # Replace with Current Price and Buyout Price
                    # We need to find the card__prices section in this card
                    new_card_html = re.sub(
                        r'(<div class="card__prices">.*?<div class="card__price-row">.*?<span class="card__price-label">)Price(</span>.*?<span class="card__price">)([^<]+)(</span>.*?</div>.*?<div class="card__price-row">.*?<span class="card__price-label">)Price(</span>.*?<span class="card__price">)([^<]+)(</span>.*?</div>.*?</div>)',
                        rf'\1Current Price\2{price}\3\4Buyout Price\5{price}\6\7',
                        card_html,
                        flags=re.DOTALL
                    )
                    match_content = match_content.replace(card_html, new_card_html)
        
        return match_content
    
    content = fix_yahoo_labels(content)
    
    # Actually, let's use a simpler approach: after all replacements, find yahoo-japan-auctions cards
    # and fix their labels
    def fix_yahoo_after_replace(full_content):
        # Split by card-link sections
        parts = re.split(r'(<a[^>]*class="card-link"[^>]*>)', full_content)
        result_parts = []
        
        i = 0
        while i < len(parts):
            result_parts.append(parts[i])
            if i + 1 < len(parts) and 'data-shop="yahoo-japan-auctions"' in parts[i]:
                # This is a yahoo-japan-auctions card
                # Find the next closing </a> tag
                card_content = parts[i + 1] if i + 1 < len(parts) else ''
                # Check if it has "Price" labels that need to be changed
                if 'card__price-label">Price</span>' in card_content:
                    # Replace first "Price" with "Current Price"
                    card_content = re.sub(
                        r'(<span class="card__price-label">)Price(</span>.*?<span class="card__price">)([^<]+)(</span>.*?</div>.*?<div class="card__price-row">.*?<span class="card__price-label">)Price(</span>.*?<span class="card__price">)([^<]+)(</span>)',
                        r'\1Current Price\2\3\4Buyout Price\5\6\7',
                        card_content,
                        count=1
                    )
                    result_parts.append(card_content)
                    i += 2
                    continue
            if i + 1 < len(parts):
                result_parts.append(parts[i + 1])
            i += 1
        
        return ''.join(result_parts)
    
    # Simpler: just do a direct replacement for yahoo cards
    yahoo_fix_pattern = re.compile(
        r'(<a[^>]*data-shop="yahoo-japan-auctions"[^>]*>.*?<div class="card__prices">.*?<div class="card__price-row">.*?<span class="card__price-label">)Price(</span>.*?<span class="card__price">)([^<]+)(</span>.*?</div>.*?<div class="card__price-row">.*?<span class="card__price-label">)Price(</span>.*?<span class="card__price">)([^<]+)(</span>.*?</div>.*?</div>)',
        re.DOTALL
    )
    
    def fix_yahoo(match):
        price1 = match.group(3).strip()
        price2 = match.group(6).strip()
        return f'{match.group(1)}Current Price{match.group(2)}{price1}{match.group(4)}Buyout Price{match.group(5)}{price2}{match.group(7)}'
    
    content = yahoo_fix_pattern.sub(fix_yahoo, content)
    
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
        if update_card_prices(html_file):
            print(f"Updated: {html_file.name}")
            updated_count += 1
    
    print(f"\nUpdated {updated_count} file(s)")

if __name__ == '__main__':
    main()
