from PIL import Image

# Load original 4K logo
original = Image.open('/home/ubuntu/shutterzilla_v1_all_gray_4k.png')
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
