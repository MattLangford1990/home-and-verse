#!/usr/bin/env python3
"""
Quick stock update from Zoho - fixes in_stock and has_image fields
"""
import json
import os
import time
from datetime import datetime
from pathlib import Path

# Load .env manually
env_path = Path(__file__).parent / '.env'
env_vars = {}
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")

ZOHO_CLIENT_ID = env_vars.get('ZOHO_CLIENT_ID')
ZOHO_CLIENT_SECRET = env_vars.get('ZOHO_CLIENT_SECRET')
ZOHO_REFRESH_TOKEN = env_vars.get('ZOHO_REFRESH_TOKEN')
ZOHO_ORG_ID = env_vars.get('ZOHO_ORG_ID')

import requests

def get_token():
    resp = requests.post('https://accounts.zoho.eu/oauth/v2/token', data={
        'refresh_token': ZOHO_REFRESH_TOKEN,
        'client_id': ZOHO_CLIENT_ID,
        'client_secret': ZOHO_CLIENT_SECRET,
        'grant_type': 'refresh_token'
    })
    return resp.json()['access_token']

def fetch_stock(token):
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    stock_map = {}
    page = 1
    
    while True:
        resp = requests.get(
            'https://www.zohoapis.eu/inventory/v1/items',
            headers=headers,
            params={'organization_id': ZOHO_ORG_ID, 'page': page, 'per_page': 200}
        )
        
        if resp.status_code == 429:
            print('Rate limited, waiting 60s...')
            time.sleep(60)
            continue
            
        data = resp.json()
        items = data.get('items', [])
        
        if not items:
            break
        
        for item in items:
            sku = item.get('sku')
            if sku:
                stock_map[sku] = int(item.get('stock_on_hand', 0) or 0)
        
        print(f'Page {page}: {len(stock_map)} SKUs')
        
        if not data.get('page_context', {}).get('has_more_page'):
            break
            
        page += 1
        time.sleep(0.5)
    
    return stock_map

def main():
    print('=' * 50)
    print('HOME & VERSE - STOCK UPDATE')
    print('=' * 50)
    
    print('\nFetching fresh stock from Zoho...')
    token = get_token()
    stock_map = fetch_stock(token)
    print(f'Got stock for {len(stock_map)} SKUs')
    
    # Load products
    products_file = Path(__file__).parent / 'data' / 'products.json'
    with open(products_file) as f:
        data = json.load(f)
    
    products = data['products']
    updated = 0
    
    for p in products:
        sku = p.get('sku')
        old_stock = p.get('stock', 0)
        
        if sku in stock_map:
            new_stock = stock_map[sku]
            p['stock'] = new_stock
            p['in_stock'] = new_stock > 0
            if new_stock != old_stock:
                updated += 1
        else:
            # SKU not in Zoho - keep existing stock, set in_stock boolean
            p['in_stock'] = p.get('stock', 0) > 0
        
        # Ensure has_image is set
        if 'has_image' not in p:
            p['has_image'] = True
    
    # Save
    data['products'] = products
    data['stock_updated_at'] = datetime.now().isoformat()
    
    with open(products_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    in_stock_count = sum(1 for p in products if p['in_stock'])
    print(f'\nUpdated {updated} stock levels')
    print(f'In stock: {in_stock_count} / {len(products)}')
    print('Saved!')

if __name__ == '__main__':
    main()
