#!/usr/bin/env python3
"""Update website to also check for mood images"""

with open('/Users/matt/Desktop/home-and-verse/preview.html') as f:
    content = f.read()

old_code = '''// Load extra images - try common patterns and show what works
  React.useEffect(() => {
    if (!sku) return;
    
    // Try loading variants _2 through _6 directly
    const possibleExtras = [];
    for (let i = 2; i <= 6; i++) {
      possibleExtras.push(`/images/${sku}_${i}.jpg`);
    }'''

new_code = '''// Load extra images - try common patterns and show what works
  React.useEffect(() => {
    if (!sku) return;
    
    // Try loading variants _2 through _6 AND mood images
    const possibleExtras = [];
    for (let i = 2; i <= 6; i++) {
      possibleExtras.push(`/images/${sku}_${i}.jpg`);
    }
    // Also check for mood images
    for (let i = 1; i <= 4; i++) {
      possibleExtras.push(`/images/${sku}_mood${i}.jpg`);
    }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Updated to check for mood images too!")
else:
    print("Pattern not found")

with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w') as f:
    f.write(content)
