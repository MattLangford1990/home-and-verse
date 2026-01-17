#!/usr/bin/env python3
"""
Add descriptions to the 4 remaining products
"""
import json

PRODUCTS_FILE = '/Users/matt/Desktop/home-and-verse/backend/data/products.json'

# Manual descriptions for the 4 items
DESCRIPTIONS = {
    "XXXX 51452": "A charming porcelain cup from the Trevoly collection, featuring Räder's signature sun motif. Part of the beloved German design house's everyday tableware range.",
    "92191": "Display stand containing 36 lucky star decorations across 6 delightful designs. A complete retail display solution for these popular Räder collectibles.",
    "16727": "Retail display featuring 72 miniature porcelain hearts in 6 charming designs. These delicate Räder pieces make thoughtful gifts and decorative accents.",
    "RC": "Remember brand catalogues and marketing materials for trade customers.",
}

with open(PRODUCTS_FILE) as f:
    data = json.load(f)

updated = 0
for p in data['products']:
    sku = p['sku']
    if sku in DESCRIPTIONS:
        p['description'] = DESCRIPTIONS[sku]
        p['ai_description'] = DESCRIPTIONS[sku]
        print(f"✓ Updated {sku}")
        updated += 1

with open(PRODUCTS_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nUpdated {updated} products")
