# Generate Profile Picture Script for Lovable

## Prompt for Lovable AI:

```
Generate a professional profile picture for a person named Brandon Sturka. 

Requirements:
- Realistic, professional headshot style
- Circular/circular-croppable format
- High quality, suitable for web use (at least 512x512px)
- Professional appearance, friendly expression
- Neutral background or transparent background
- Age: Adult professional (30-40s)
- Gender: Female
- Professional business casual appearance
- Well-lit, clear features
- Suitable for use in a web application topbar (44x44px display size, but generate larger for quality)

The image should be saved as a PNG or JPG file that can be used in the profile icon.
```

## Alternative: Using Image Generation APIs

If Lovable supports API calls, here's a script you can use:

```python
# generate_profile_pic.py
import requests
import os

def generate_profile_pic(name="Caren Sturka", output_path="docs/mockups/current/assets/profile-pic.jpg"):
    """
    Generate a profile picture using an image generation service.
    Note: This is a template - you'll need to replace with actual API endpoints
    that Lovable supports or integrate with services like:
    - DALL-E API
    - Midjourney API
    - Stable Diffusion API
    - Or use a placeholder service like randomuser.me
    """
    
    # Option 1: Use Random User API (real photos)
    response = requests.get("https://randomuser.me/api/?gender=female&nat=us")
    data = response.json()
    photo_url = data['results'][0]['picture']['large']
    
    img_response = requests.get(photo_url)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        f.write(img_response.content)
    
    print(f"Profile picture saved to {output_path}")
    return output_path

if __name__ == "__main__":
    generate_profile_pic()
```

## Quick Solution: Use Random User API

If you just need a real photo quickly, you can use this URL directly:

```
https://randomuser.me/api/portraits/women/44.jpg
```

Or generate a random one:
```python
import requests
import json

response = requests.get("https://randomuser.me/api/?gender=female")
data = response.json()
photo_url = data['results'][0]['picture']['large']
print(f"Photo URL: {photo_url}")
```

## For Lovable Specifically:

In Lovable, you can try:
1. Use the chat interface and paste the prompt above
2. Or use Lovable's image generation features if available
3. Or integrate with an external API using the Python script above
