#!/usr/bin/env python3
"""Build manifest of extra images per SKU for instant loading"""

import json
import re
from pathlib import Path
from collections import defaultdict

image_counts = defaultdict(list)

# From Remember uploads
remember_file = Path('/Users/matt/Desktop/home-and-verse/processed-images/upload_progress.json')
if remember_file.exists():
    with open(remember_file) as f:
        data = json.load(f)
    for filename in data.get('uploaded', []):
        name = Path(filename).stem
        parts = name.split('_')
        sku = parts[0]
        if len(parts) > 1 and parts[1].startswith('mood'):
            image_counts[sku].append(f'{sku}_{parts[1]}')
        elif len(parts) > 1 and parts[1].isdigit():
            image_counts[sku].append(f'{sku}_{parts[1]}')

# From Räder round 1
rader1_file = Path('/Users/matt/Desktop/home-and-verse/processed-rader-images/upload_progress.json')
if rader1_file.exists():
    with open(rader1_file) as f:
        data = json.load(f)
    for filename in data.get('uploaded', []):
        name = Path(filename).stem.lstrip('0')
        match = re.match(r'^(\d+)', name)
        if match:
            sku = match.group(1)
            rest = name[len(sku):]
            var_match = re.search(r'_(\d+)', rest)
            if var_match:
                image_counts[sku].append(f'{sku}_{var_match.group(1)}')

# From Räder round 2
rader2_file = Path('/Users/matt/Desktop/home-and-verse/processed-rader-images/upload_progress_v2.json')
if rader2_file.exists():
    with open(rader2_file) as f:
        data = json.load(f)
    for filename in data.get('uploaded', []):
        name = Path(filename).stem.lstrip('0')
        match = re.match(r'^(\d+)', name)
        if match:
            sku = match.group(1)
            rest = name[len(sku):]
            var_match = re.search(r'_(\d+)', rest)
            if var_match:
                image_counts[sku].append(f'{sku}_{var_match.group(1)}')

# Only keep SKUs with extra images
extras = {sku: sorted(set(variants)) for sku, variants in image_counts.items() if variants}

print(f'Products with extra images: {len(extras)}')
for sku in list(extras.keys())[:10]:
    print(f'  {sku}: {extras[sku]}')

# Save manifest
with open('/Users/matt/Desktop/home-and-verse/backend/data/image_extras.json', 'w') as f:
    json.dump(extras, f)

print(f'\nSaved to image_extras.json')
