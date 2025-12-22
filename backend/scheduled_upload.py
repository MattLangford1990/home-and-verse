#!/usr/bin/env python3
"""
Upload additional Relaxound images to Zoho Inventory
SCHEDULED VERSION - runs slowly and logs everything
"""

import os
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import json
import time

LOG_FILE = "/tmp/zoho_scheduled_upload.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

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

log("=" * 50)
log("SCHEDULED ZOHO IMAGE UPLOAD STARTING")
log("=" * 50)

# Get access token
log("Getting Zoho access token...")
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
    log(f"Token refresh failed: {response.status_code}")
    exit(1)

data = response.json()
if "error" in data:
    log(f"Token error: {data.get('error')}")
    exit(1)

access_token = data["access_token"]
log("Token obtained!")

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

total_to_upload = sum(len(p['images']) - 1 for p in relaxound)
log(f"Found {len(relaxound)} products, {total_to_upload} images to upload")

# Upload additional images
total_uploaded = 0
total_failed = 0
total_skipped = 0

for product in relaxound:
    sku = product['sku']
    name = product['name']
    images = product['images']
    zoho_item_id = product['id']
    
    log(f"Processing: {sku} - {name}")
    
    for img_url in images[1:]:
        img_filename = img_url.replace('/images/', '')
        img_path = IMAGES_DIR / img_filename
        
        if not img_path.exists():
            log(f"  SKIP (not found): {img_filename}")
            total_skipped += 1
            continue
        
        ext = img_path.suffix.lower()
        mime_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        # Retry logic
        max_retries = 3
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
                        log(f"  OK: {img_filename}")
                        total_uploaded += 1
                        success = True
                        break
                    else:
                        log(f"  FAIL: {img_filename} - {result.get('message')}")
                        total_failed += 1
                        break
                elif response.status_code == 429:
                    wait_time = 120 * (attempt + 1)
                    log(f"  Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    log(f"  HTTP {response.status_code}: {img_filename}")
                    total_failed += 1
                    break
            except Exception as e:
                log(f"  ERROR: {img_filename} - {e}")
                total_failed += 1
                break
        
        if not success and not (response.status_code != 429):
            total_failed += 1
        
        # Wait 15 seconds between uploads
        time.sleep(15)

log("=" * 50)
log("COMPLETE!")
log(f"Uploaded: {total_uploaded}")
log(f"Failed: {total_failed}")
log(f"Skipped: {total_skipped}")
log("=" * 50)
