#!/usr/bin/env python3
"""Update preview.html to use image manifest instead of network requests"""

import json
import re

# Load the manifest
with open('/Users/matt/Desktop/home-and-verse/backend/data/image_extras.json') as f:
    extras = json.load(f)

# Load the HTML
with open('/Users/matt/Desktop/home-and-verse/preview.html') as f:
    content = f.read()

# 1. Add the manifest after CLOUDINARY_BASE
manifest_js = 'const IMAGE_EXTRAS = ' + json.dumps(extras) + ';'

if 'IMAGE_EXTRAS' not in content:
    old_line = "const CLOUDINARY_BASE = 'https://res.cloudinary.com/dcfbgveei/image/upload';"
    new_lines = old_line + '\n\n// Pre-loaded image manifest - no network requests needed\n' + manifest_js
    content = content.replace(old_line, new_lines)
    print("Added IMAGE_EXTRAS manifest")

# 2. Replace the useEffect that checks for extra images
# Find the pattern and replace with instant lookup

old_pattern = r'''// Lazy-load extra images in background.*?const timer = setTimeout\(checkExtraImages, \d+\);
    return \(\) => clearTimeout\(timer\);
  \}, \[sku\]\);'''

new_code = '''// Instant lookup from pre-loaded manifest - no network requests!
  React.useEffect(() => {
    if (!sku) return;
    const extras = IMAGE_EXTRAS[sku] || [];
    if (extras.length > 0) {
      setExtraImages(extras.map(id => `/images/${id}.jpg`));
    } else {
      setExtraImages([]);
    }
  }, [sku]);'''

content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w') as f:
    f.write(content)

print("Done! Updated to use instant manifest lookup")
