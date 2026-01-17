#!/usr/bin/env python3
"""
Home & Verse - Gentle Zoho Product Import
=========================================
Re-imports products from Zoho with delays to avoid API rate limits.
Only fetches product data (no images) - images already on CDN.

Usage:
    cd /Users/matt/Desktop/home-and-verse/backend
    python3 import_from_zoho_gentle.py
"""

import json
import os
import re
import time
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

DELAY_BETWEEN_PAGES = 1.0  # seconds between API calls

# Brand mapping
BRAND_MAP = {
    "räder": "Räder",
    "rader": "Räder", 
    "rader gmbh": "Räder",
    "my flame lifestyle": "My Flame",
    "my flame": "My Flame",
    "remember": "Remember",
    "relaxound": "Relaxound",
    "ideas 4 seasons": "Ideas4Seasons",
    "ideas4seasons": "Ideas4Seasons",
    "elvang": "Elvang",
    "elvang denmark": "Elvang",
}

CONSUMER_BRANDS = {"Räder", "My Flame", "Remember", "Relaxound", "Ideas4Seasons", "Elvang"}

def get_token():
    resp = requests.post('https://accounts.zoho.eu/oauth/v2/token', data={
        'refresh_token': ZOHO_REFRESH_TOKEN,
        'client_id': ZOHO_CLIENT_ID,
        'client_secret': ZOHO_CLIENT_SECRET,
        'grant_type': 'refresh_token'
    })
    return resp.json()['access_token']

def normalize_brand(brand_raw):
    if not brand_raw:
        return None
    brand_lower = brand_raw.lower().strip()
    return BRAND_MAP.get(brand_lower)

def fetch_all_items(token):
    """Fetch all items from Zoho with delays"""
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    all_items = []
    page = 1
    
    print("Fetching items from Zoho (with delays)...")
    
    while True:
        resp = requests.get(
            'https://www.zohoapis.eu/inventory/v1/items',
            headers=headers,
            params={'organization_id': ZOHO_ORG_ID, 'page': page, 'per_page': 200}
        )
        
        if resp.status_code == 429:
            print("  Rate limited! Waiting 60 seconds...")
            time.sleep(60)
            continue
            
        data = resp.json()
        items = data.get('items', [])
        
        if not items:
            break
        
        all_items.extend(items)
        print(f"  Page {page}: {len(items)} items (total: {len(all_items)})")
        
        if not data.get('page_context', {}).get('has_more_page'):
            break
            
        page += 1
        time.sleep(DELAY_BETWEEN_PAGES)
    
    return all_items

def transform_product(item):
    """Transform Zoho item to Home & Verse product format"""
    brand_raw = item.get('brand', '')
    brand = normalize_brand(brand_raw)
    
    if not brand or brand not in CONSUMER_BRANDS:
        return None
    
    sku = item.get('sku', '')
    name = item.get('name', '')
    
    # Clean up name - remove brand prefix if present
    for prefix in [f"{brand} ", f"{brand_raw} "]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    
    # Get price
    price = item.get('rate', 0)
    
    # Get stock
    stock = item.get('stock_on_hand', 0) or 0
    
    # Get description
    description = item.get('description', '') or ''
    
    # Build image URL from CDN
    image_url = f"https://images.homeandverse.com/products/{sku}.jpg"
    
    product = {
        'sku': sku,
        'name': name,
        'brand': brand,
        'price': price,
        'stock': int(stock),
        'description': description,
        'image': image_url,
        'zoho_item_id': item.get('item_id'),
    }
    
    return product

def main():
    print("=" * 50)
    print("Home & Verse - Gentle Zoho Import")
    print("=" * 50)
    
    # Load existing products to preserve descriptions etc
    data_dir = '/Users/matt/Desktop/home-and-verse/backend/data'
    products_file = os.path.join(data_dir, 'products.json')
    
    existing_products = {}
    if os.path.exists(products_file):
        with open(products_file) as f:
            data = json.load(f)
            for p in data.get('products', []):
                existing_products[p['sku']] = p
        print(f"Loaded {len(existing_products)} existing products")
    
    # Fetch from Zoho
    token = get_token()
    items = fetch_all_items(token)
    print(f"\nFetched {len(items)} total items from Zoho")
    
    # Transform to products
    products = []
    new_count = 0
    updated_count = 0
    
    for item in items:
        product = transform_product(item)
        if not product:
            continue
        
        sku = product['sku']
        
        # Preserve existing description if we have one
        if sku in existing_products:
            existing = existing_products[sku]
            # Keep existing description, categories, slug etc
            if existing.get('description') and not product.get('description'):
                product['description'] = existing['description']
            if existing.get('categories'):
                product['categories'] = existing['categories']
            if existing.get('slug'):
                product['slug'] = existing['slug']
            if existing.get('ai_description'):
                product['ai_description'] = existing['ai_description']
            updated_count += 1
        else:
            new_count += 1
        
        products.append(product)
    
    # Count by brand
    brands = {}
    for p in products:
        brand = p['brand']
        brands[brand] = brands.get(brand, 0) + 1
    
    print(f"\n" + "=" * 50)
    print("RESULTS:")
    print(f"  Total products: {len(products)}")
    print(f"  New products: {new_count}")
    print(f"  Updated products: {updated_count}")
    print(f"\nBy brand:")
    for brand, count in sorted(brands.items(), key=lambda x: -x[1]):
        print(f"  {brand}: {count}")
    
    # Backup existing
    if os.path.exists(products_file):
        backup_file = products_file.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        os.rename(products_file, backup_file)
        print(f"\nBacked up existing to {os.path.basename(backup_file)}")
    
    # Save new products
    output = {
        'products': products,
        'imported_at': datetime.now().isoformat(),
        'count': len(products)
    }
    
    with open(products_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Saved to {products_file}")
    print("\nDone!")

if __name__ == '__main__':
    main()
