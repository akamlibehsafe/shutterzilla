#!/usr/bin/env python3
"""
Generate a profile picture for Caren Sturka.
This script can be used with Lovable or run standalone.
"""

import requests
import os
import sys

def generate_profile_pic_from_randomuser(name="Caren Sturka", output_path=None):
    """
    Generate a profile picture using Random User API (real photos).
    """
    if output_path is None:
        output_path = "docs/mockups/current/assets/profile-pic.jpg"
    
    try:
        # Get a random user photo
        response = requests.get("https://randomuser.me/api/?gender=female&nat=us")
        response.raise_for_status()
        data = response.json()
        photo_url = data['results'][0]['picture']['large']
        
        # Download the image
        img_response = requests.get(photo_url)
        img_response.raise_for_status()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the image
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        print(f"✓ Profile picture saved to: {output_path}")
        print(f"✓ Photo URL: {photo_url}")
        return output_path
        
    except Exception as e:
        print(f"Error generating profile picture: {e}")
        return None

def generate_with_lovable_prompt():
    """
    Print a prompt you can use in Lovable's AI interface.
    """
    prompt = """
Generate a professional profile picture for Caren Sturka.

Requirements:
- Realistic, professional headshot style
- Circular/circular-croppable format  
- High quality, suitable for web use (at least 512x512px)
- Professional appearance, friendly expression
- Neutral or transparent background
- Adult professional (30-40s), female
- Professional business casual appearance
- Well-lit, clear features
- Suitable for web application topbar (will be displayed at 44x44px)

Save as: docs/mockups/current/assets/profile-pic.jpg
"""
    print("=" * 60)
    print("LOVABLE PROMPT:")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
    print("\nCopy the prompt above and paste it into Lovable's AI chat.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--lovable":
        generate_with_lovable_prompt()
    else:
        print("Generating profile picture using Random User API...")
        result = generate_profile_pic_from_randomuser()
        if result:
            print(f"\nTo use this image, update the HTML to:")
            print(f'<img src="../../assets/profile-pic.jpg" alt="Caren Sturka profile" />')
