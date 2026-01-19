from PIL import Image
import sys
import os

# Get input file path from command line argument or use default
if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    # Try to find the logo in common locations
    possible_paths = [
        'shutterzilla_v1_all_gray_4k.png',
        '../branding/Logo/02 Manus Generated Logos/v1_all_gray/shutterzilla_v1_4k.png',
        'branding/Logo/02 Manus Generated Logos/v1_all_gray/shutterzilla_v1_4k.png',
    ]
    
    input_path = None
    for path in possible_paths:
        if os.path.exists(path):
            input_path = path
            break
    
    if not input_path:
        print("Error: Logo file not found.")
        print("Usage: python resize_logo.py [path_to_4k_logo.png]")
        print("Or place the logo file in one of these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        sys.exit(1)

# Load original 4K logo
original = Image.open(input_path)
print(f'Loading logo from: {input_path}')
print(f'Original size: {original.size}')

# Content bounds from analysis
rmin, rmax = 450, 1085
cmin, cmax = 205, 2546

# Add small padding
padding = 20
rmin = max(0, rmin - padding)
rmax = min(original.height, rmax + padding)
cmin = max(0, cmin - padding)
cmax = min(original.width, cmax + padding)

# Crop to actual content
cropped = original.crop((cmin, rmin, cmax, rmax))
print(f'Cropped size: {cropped.size}')

# Save cropped high-res version
cropped.save('logo-cropped-original.png')

# For top bar - 50px height
topbar_height = 50
ratio = topbar_height / cropped.height
topbar_logo = cropped.resize((int(cropped.width * ratio), topbar_height), Image.LANCZOS)
topbar_logo.save('logo-topbar.png')
print(f'Top bar logo: {topbar_logo.size}')

# For landing page - 100px height  
landing_height = 100
ratio = landing_height / cropped.height
landing_logo = cropped.resize((int(cropped.width * ratio), landing_height), Image.LANCZOS)
landing_logo.save('logo-landing.png')
print(f'Landing logo: {landing_logo.size}')

# Default logo - 60px height
default_height = 60
ratio = default_height / cropped.height
default_logo = cropped.resize((int(cropped.width * ratio), default_height), Image.LANCZOS)
default_logo.save('logo.png')
print(f'Default logo: {default_logo.size}')

print('Done!')
