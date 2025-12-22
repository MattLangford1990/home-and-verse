#!/usr/bin/env python3
"""
Upload additional Relaxound images to Zoho Inventory
With conservative rate limit handling - SLOW MODE
"""

import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import json
import time

# Load credentials
ENV_PATH = "/Users/matt/Desktop/dm-sales-app/backend/.env"
load_dotenv(ENV_PATH)

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

IMAGES_DIR = Path("/Users/matt/Desktop/home-and-verse/backend/data/images")
PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")
BASE_URL = "https://www.zohoapis.eu/inventory/v1"

# Get access token
print("Getting Zoho access token...")
response = requests.post(
    "https://accounts.zoho.eu/oauth/v2/token",
    data={
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
)

if response.status_code != 200:
    print(f"Token refresh failed: {response.status_code}")
    exit(1)

data = response.json()
if "error" in data:
    print(f"Token error: {data.get('error')}")
    exit(1)

access_token = data["access_token"]
print("Token obtained!")

headers = {
    "Authorization": f"Zoho-oauthtoken {access_token}",
    "X-com-zoho-inventory-organizationid": ZOHO_ORG_ID
}

# Load products
with open(PRODUCTS_FILE) as f:
    products_data = json.load(f)

# Find Relaxound products with additional images
relaxound = []
for p in products_data['products']:
    brand = p.get('brand', '').lower()
    name = p.get('name', '').lower()
    
    if 'relaxound' in brand or any(x in name for x in ['zwitscherbox', 'birdybox', 'oceanbox', 'junglebox', 'lakesidebox', 'zirpybox']):
        images = p.get('images', [])
        if len(images) > 1:
            relaxound.append({
                'sku': p['sku'],
                'id': p['id'],
                'name': p['name'],
                'images': images
            })

print(f"Found {len(relaxound)} Relaxound products with multiple images")

# Count total images to upload
total_to_upload = sum(len(p['images']) - 1 for p in relaxound)
print(f"Total images to upload: {total_to_upload}")
print(f"Estimated time: {total_to_upload * 10 / 60:.1f} minutes")

print("\nWaiting 2 minutes for rate limit to reset...")
time.sleep(120)

# Upload additional images
total_uploaded = 0
total_failed = 0
total_skipped = 0

for product in relaxound:
    sku = product['sku']
    name = product['name']
    images = product['images']
    zoho_item_id = product['id']
    
    print(f"\n{sku}: {name} ({len(images)} images)")
    
    # Upload images 2-5 (skip the first one)
    for img_url in images[1:]:
        img_filename = img_url.replace('/images/', '')
        img_path = IMAGES_DIR / img_filename
        
        if not img_path.exists():
            print(f"  Not found: {img_filename}")
            total_skipped += 1
            continue
        
        # Determine mime type
        ext = img_path.suffix.lower()
        mime_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        print(f"  Uploading: {img_filename}...", end=" ", flush=True)
        
        # Retry logic for rate limits
        max_retries = 5
        success = False
        
        for attempt in range(max_retries):
            try:
                with open(img_path, 'rb') as img_file:
                    files = {'image': (img_path.name, img_file, mime_type)}
                    response = requests.post(
                        f"{BASE_URL}/items/{zoho_item_id}/image",
                        headers=headers,
                        files=files
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 0:
                        print("OK")
                        total_uploaded += 1
                        success = True
                        break
                    else:
                        print(f"Failed: {result.get('message', 'Unknown error')}")
                        total_failed += 1
                        break
                elif response.status_code == 429:
                    wait_time = 60 * (attempt + 1)  # 60s, 120s, 180s, etc.
                    print(f"Rate limited (attempt {attempt+1}), waiting {wait_time}s...", end=" ", flush=True)
                    time.sleep(wait_time)
                    # Continue to retry
                else:
                    print(f"HTTP {response.status_code}")
                    total_failed += 1
                    break
            except Exception as e:
                print(f"Error: {e}")
                total_failed += 1
                break
        
        if not success and response.status_code == 429:
            print("Max retries exceeded, skipping")
            total_failed += 1
        
        # Wait 10 seconds between uploads to stay under rate limit
        print(f"  [Uploaded: {total_uploaded}, Progress: {total_uploaded + total_failed + total_skipped}/{total_to_upload}]")
        time.sleep(10)

print(f"\n\n{'='*50}")
print("COMPLETE!")
print(f"{'='*50}")
print(f"Uploaded: {total_uploaded}")
print(f"Failed: {total_failed}")
print(f"Skipped (not found): {total_skipped}")
