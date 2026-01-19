#!/usr/bin/env python3
"""
Fix products.json - add in_stock boolean based on stock value
"""
import json
from pathlib import Path
from datetime import datetime

products_file = Path(__file__).parent / 'data' / 'products.json'

print('Loading products...')
with open(products_file) as f:
    data = json.load(f)

products = data['products']

for p in products:
    stock = p.get('stock', 0)
    p['in_stock'] = stock > 0
    
    if 'has_image' not in p:
        p['has_image'] = True

data['products'] = products

with open(products_file, 'w') as f:
    json.dump(data, f, indent=2)

in_stock_count = sum(1 for p in products if p['in_stock'])
print(f'Products in stock: {in_stock_count} / {len(products)}')
print('Saved!')
