#!/usr/bin/env python3
"""
Quick fix - add in_stock boolean based on existing stock numbers
No Zoho API call - just fixes the missing fields
"""
import json
from pathlib import Path
from datetime import datetime

products_file = Path(__file__).parent / 'data' / 'products.json'

print('Loading products...')
with open(products_file) as f:
    data = json.load(f)

products = data['products']

fixed_in_stock = 0
fixed_has_image = 0

for p in products:
    # Fix in_stock boolean based on stock number
    stock = p.get('stock', 0)
    if 'in_stock' not in p or p['in_stock'] != (stock > 0):
        p['in_stock'] = stock > 0
        fixed_in_stock += 1
    
    # Ensure has_image is set
    if 'has_image' not in p:
        p['has_image'] = True
        fixed_has_image += 1

# Save
data['products'] = products
data['fields_fixed_at'] = datetime.now().isoformat()

with open(products_file, 'w') as f:
    json.dump(data, f, indent=2)

in_stock_count = sum(1 for p in products if p['in_stock'])
print(f'Fixed in_stock field: {fixed_in_stock}')
print(f'Fixed has_image field: {fixed_has_image}')
print(f'Products in stock: {in_stock_count} / {len(products)}')
print('Saved!')
