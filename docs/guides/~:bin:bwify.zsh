Here’s a **Zsh script** that converts **all images in a folder** to **black & white**, saving results into a `bw/` subfolder (keeps originals). It prefers **ImageMagick** (best quality/control) and falls back to **macOS `sips`** if ImageMagick isn’t installed.

```zsh
#!/usr/bin/env zsh
set -euo pipefail
setopt extendedglob nullglob

# Usage:
#   ./bwify.zsh /path/to/folder
#   ./bwify.zsh /path/to/folder /path/to/output_folder
#
# Output defaults to: <input>/bw

in_dir="${1:-.}"
out_dir="${2:-$in_dir/bw}"

# Normalize paths
in_dir="${in_dir:A}"
out_dir="${out_dir:A}"

mkdir -p "$out_dir"

# Detect tool
use_magick=0
if command -v magick >/dev/null 2>&1; then
  use_magick=1
elif command -v convert >/dev/null 2>&1; then
  use_magick=2
fi

# macOS Generic Gray profile (fallback)
gray_profile="/System/Library/ColorSync/Profiles/Generic Gray Profile.icc"

# Files to process (non-recursive)
types=(jpg jpeg png tif tiff webp heic heif bmp gif)
files=()
for ext in $types; do
  files+=("$in_dir"/*.${ext}(N))
  files+=("$in_dir"/*.${(U)ext}(N))
done

if (( ${#files[@]} == 0 )); then
  echo "No images found in: $in_dir"
  exit 0
fi

echo "Input : $in_dir"
echo "Output: $out_dir"
if (( use_magick == 1 )); then
  echo "Using : ImageMagick (magick)"
elif (( use_magick == 2 )); then
  echo "Using : ImageMagick (convert)"
else
  echo "Using : macOS sips (fallback)"
fi

for f in "${files[@]}"; do
  base="${f:t}"
  out="$out_dir/$base"

  # Avoid overwriting if input already in out_dir
  if [[ "$f" == "$out" ]]; then
    echo "Skipping (same path): $f"
    continue
  fi

  if (( use_magick == 1 )); then
    magick "$f" -colorspace Gray -type Grayscale -strip "$out"
  elif (( use_magick == 2 )); then
    convert "$f" -colorspace Gray -type Grayscale -strip "$out"
  else
    # Best-effort grayscale via ColorSync profile
    if [[ -f "$gray_profile" ]]; then
      sips --matchTo "$gray_profile" "$f" --out "$out" >/dev/null
    else
      echo "ERROR: Gray profile not found at: $gray_profile"
      echo "Install ImageMagick for reliable grayscale conversion."
      exit 1
    fi
  fi

  echo "BW  -> ${out:t}"
done

echo "Done. Converted ${#files[@]} file(s)."
```

**Run it:**

```sh
chmod +x bwify.zsh
./bwify.zsh /path/to/images
```

If you want a **recursive** version (includes subfolders), tell me and I’ll give a `find`-based one (still Zsh-safe with spaces in filenames).
