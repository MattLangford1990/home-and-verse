#!/usr/bin/env python3
"""
Upload additional Relaxound images to Zoho Inventory

This script uploads the extra images (_2, _3, _4, _5) for Relaxound products
"""

import os
import sys
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

# Local images directory
IMAGES_DIR = Path("/Users/matt/Desktop/home-and-verse/backend/data/images")
PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")


class ZohoAPI:
    BASE_URL = "https://www.zohoapis.eu/inventory/v1"
    
    def __init__(self):
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self):
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        print("  Refreshing Zoho access token...")
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
            raise Exception(f"Token refresh failed: {response.status_code} - {response.text}")
        
        data = response.json()
        if "error" in data:
            raise Exception(f"Token error: {data.get('error')}")
        
        self.access_token = data["access_token"]
        self.token_expiry = datetime.now() + timedelta(seconds=data.get("expires_in", 3600) - 300)
        print("  ✅ Token refreshed")
        return self.access_token
    
    def get_headers(self):
        return {
            "Authorization": f"Zoho-oauthtoken {self.get_access_token()}",
            "X-com-zoho-inventory-organizationid": ZOHO_ORG_ID
        }
    
    def get_item(self, item_id):
        """Get a single item's details including images"""
        response = requests.get(
            f"{self.BASE_URL}/items/{item_id}",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            return response.json().get("item", {})
        return None
    
    def upload_image(self, item_id, image_path):
        """Upload an image to a Zoho Inventory item"""
        # Determine mime type
        ext = image_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        with open(image_path, 'rb') as img_file:
            files = {
                'image': (image_path.name, img_file, mime_type)
            }
            
            response = requests.post(
                f"{self.BASE_URL}/items/{item_id}/image",
                headers=self.get_headers(),
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return True, result
            return False, result
        else:
            return False, response.text


def main():
    print("=" * 60)
    print("UPLOAD RELAXOUND ADDITIONAL IMAGES TO ZOHO")
    print("=" * 60)
    
    # Check credentials
    if not all([ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN, ZOHO_ORG_ID]):
        print("❌ Missing Zoho credentials")
        return
    
    # Load products
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    # Find Relaxound products with additional images
    relaxound_skus = []
    for p in data['products']:
        brand = p.get('brand', '').lower()
        name = p.get('name', '').lower()
        
        if 'relaxound' in brand or any(x in name for x in ['zwitscherbox', 'birdybox', 'oceanbox', 'junglebox', 'lakesidebox', 'zirpybox']):
            images = p.get('images', [])
            # Only include if has additional images (more than 1)
            if len(images) > 1:
                relaxound_skus.append({
                    'sku': p['sku'],
                    'id': p['id'],
                    'name': p['name'],
                    'images': images
                })
    
    print(f"Found {len(relaxound_skus)} Relaxound products with multiple images\n")
    
    zoho = ZohoAPI()
    
    # Process each product
    total_uploaded = 0
    total_failed = 0
    
    for product in relaxound_skus:
        sku = product['sku']
        name = product['name']
        images = product['images']
        zoho_item_id = product['id']
        
        print(f"\n{sku}: {name}")
        print(f"  Images: {len(images)}")
        
        # Upload images 2-5 (skip the first one as it should already be in Zoho)
        for img_url in images[1:]:
            # Extract filename from URL
            img_filename = img_url.replace('/images/', '')
            img_path = IMAGES_DIR / img_filename
            
            if not img_path.exists():
                print(f"  ❌ Not found: {img_filename}")
                continue
            
            print(f"  ⬆️  Uploading: {img_filename}...", end=" ")
            
            success, result = zoho.upload_image(zoho_item_id, img_path)
            
            if success:
                print("✅")
                total_uploaded += 1
            else:
                print(f"❌ {result}")
                total_failed += 1
            
            # Rate limit - be gentle with API
            time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Uploaded: {total_uploaded}")
    print(f"❌ Failed: {total_failed}")


if __name__ == "__main__":
    main()
