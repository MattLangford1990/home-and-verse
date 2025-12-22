#!/usr/bin/env python3
"""
Rebuild image manifest by checking what's actually in Cloudinary
"""
import json
import urllib.request
from pathlib import Path

# Load all products to get SKUs
with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json') as f:
    data = json.load(f)

all_skus = [p['sku'] for p in data['products']]
print(f'Total products: {len(all_skus)}')

# Check each SKU for extra images
extras = {}
checked = 0

for sku in all_skus:
    checked += 1
    if checked % 200 == 0:
        print(f'Checked {checked}/{len(all_skus)}...')
    
    sku_extras = []
    
    # Check for _2, _3, _4, _5 variants
    for i in range(2, 8):
        url = f'https://res.cloudinary.com/dcfbgveei/image/upload/w_10/products/{sku}_{i}.jpg'
        try:
            req = urllib.request.Request(url, method='HEAD')
            urllib.request.urlopen(req, timeout=2)
            sku_extras.append(f'{sku}_{i}')
        except:
            pass
    
    # Also check for mood images
    for i in range(1, 4):
        url = f'https://res.cloudinary.com/dcfbgveei/image/upload/w_10/products/{sku}_mood{i}.jpg'
        try:
            req = urllib.request.Request(url, method='HEAD')
            urllib.request.urlopen(req, timeout=2)
            sku_extras.append(f'{sku}_mood{i}')
        except:
            pass
    
    if sku_extras:
        extras[sku] = sku_extras

print(f'\nProducts with extra images: {len(extras)}')

# Save
with open('/Users/matt/Desktop/home-and-verse/backend/data/image_extras.json', 'w') as f:
    json.dump(extras, f)

print('Saved to image_extras.json')

# Show sample
print('\nSample:')
for sku in list(extras.keys())[:10]:
    print(f'  {sku}: {extras[sku]}')
