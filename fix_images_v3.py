#!/usr/bin/env python3
"""Update preview.html to use a better image loading approach"""

with open('/Users/matt/Desktop/home-and-verse/preview.html') as f:
    content = f.read()

# Find and replace the useEffect for extra images
old_code = '''// Instant lookup from pre-loaded manifest - no network requests!
  React.useEffect(() => {
    if (!sku) return;
    const extras = IMAGE_EXTRAS[sku] || [];
    if (extras.length > 0) {
      setExtraImages(extras.map(id => `/images/${id}.jpg`));
    } else {
      setExtraImages([]);
    }
  }, [sku]);'''

new_code = '''// Load extra images - try common patterns and show what works
  React.useEffect(() => {
    if (!sku) return;
    
    // Try loading variants _2 through _6 directly
    const possibleExtras = [];
    for (let i = 2; i <= 6; i++) {
      possibleExtras.push(`/images/${sku}_${i}.jpg`);
    }
    
    // Test each one with an Image object (faster than fetch)
    const validExtras = [];
    let completed = 0;
    
    possibleExtras.forEach((path, idx) => {
      const img = new Image();
      img.onload = () => {
        validExtras[idx] = path;
        completed++;
        if (completed === possibleExtras.length) {
          setExtraImages(validExtras.filter(Boolean));
        }
      };
      img.onerror = () => {
        completed++;
        if (completed === possibleExtras.length) {
          setExtraImages(validExtras.filter(Boolean));
        }
      };
      img.src = getImageUrl(path, 'thumb');
    });
  }, [sku]);'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print('Replaced manifest lookup with Image preload approach')
else:
    print('Pattern not found - checking for alternatives...')
    # Try to find what's there
    import re
    match = re.search(r'// (Instant|Lazy).*?setExtraImages.*?\}, \[sku\]\);', content, re.DOTALL)
    if match:
        print(f'Found: {match.group()[:100]}...')

with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w') as f:
    f.write(content)

print('Done')
