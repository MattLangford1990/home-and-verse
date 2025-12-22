#!/usr/bin/env python3
import json

with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json') as f:
    data = json.load(f)

print('Sample descriptions by brand:\n')

# Get a few from each brand
brands = {}
for p in data['products']:
    b = p.get('brand', 'Unknown')
    if b not in brands:
        brands[b] = []
    if len(brands[b]) < 3:
        brands[b].append(p)

for brand, products in list(brands.items())[:5]:
    print(f'=== {brand} ===')
    for p in products:
        desc = p.get('description', 'NO DESCRIPTION')
        print(f"{p['sku']}: {p['name'][:40]}")
        print(f"   {desc[:200]}...")
        print()
