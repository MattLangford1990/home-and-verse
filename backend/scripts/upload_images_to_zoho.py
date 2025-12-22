#!/usr/bin/env python3
"""
Upload local images to Zoho Inventory

This script:
1. Fetches all items from Zoho Inventory
2. Identifies items missing images
3. Checks if we have a local image for that SKU
4. Uploads the image to Zoho

Usage:
    python3 upload_images_to_zoho.py              # Dry run - show what would be uploaded
    python3 upload_images_to_zoho.py --upload     # Actually upload images
    python3 upload_images_to_zoho.py --sku 17462  # Upload specific SKU only
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load credentials
ENV_PATH = "/Users/matt/Desktop/dm-sales-app/backend/.env"
load_dotenv(ENV_PATH)

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

# Local images directory
IMAGES_DIR = Path(__file__).parent.parent / "data" / "images"


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
    
    def get_all_items(self):
        """Fetch all items from Zoho Inventory"""
        all_items = []
        page = 1
        
        while True:
            response = requests.get(
                f"{self.BASE_URL}/items",
                headers=self.get_headers(),
                params={"page": page, "per_page": 200}
            )
            
            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
            
            data = response.json()
            items = data.get("items", [])
            all_items.extend(items)
            print(f"  Page {page}: {len(items)} items (total: {len(all_items)})")
            
            if not data.get("page_context", {}).get("has_more_page", False):
                break
            page += 1
            if page > 100:
                break
        
        return all_items
    
    def upload_image(self, item_id, image_path):
        """Upload an image to a Zoho Inventory item"""
        with open(image_path, 'rb') as img_file:
            files = {
                'image': (image_path.name, img_file, 'image/jpeg')
            }
            
            response = requests.post(
                f"{self.BASE_URL}/items/{item_id}/image",
                headers=self.get_headers(),
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            # Zoho returns code 0 for success
            if result.get('code') == 0:
                return True, result
            return False, result
        else:
            return False, response.text


def find_local_image(sku):
    """Find a local image for a given SKU"""
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        img_path = IMAGES_DIR / f"{sku}{ext}"
        if img_path.exists():
            return img_path
    return None


def main():
    parser = argparse.ArgumentParser(description='Upload images to Zoho Inventory')
    parser.add_argument('--upload', action='store_true', help='Actually upload (default is dry run)')
    parser.add_argument('--sku', help='Upload specific SKU only')
    args = parser.parse_args()
    
    print("=" * 60)
    print("UPLOAD IMAGES TO ZOHO INVENTORY")
    print("=" * 60)
    
    if not args.upload:
        print("🔍 DRY RUN MODE - use --upload to actually upload\n")
    else:
        print("⬆️  UPLOAD MODE - will upload images to Zoho\n")
    
    # Check credentials
    if not all([ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN, ZOHO_ORG_ID]):
        print("❌ Missing Zoho credentials")
        return
    
    # Check images directory
    if not IMAGES_DIR.exists():
        print(f"❌ Images directory not found: {IMAGES_DIR}")
        return
    
    zoho = ZohoAPI()
    
    # Fetch all items
    print("Fetching items from Zoho...")
    all_items = zoho.get_all_items()
    print(f"✅ Found {len(all_items)} items in Zoho\n")
    
    # Find items missing images that we have locally
    to_upload = []
    
    for item in all_items:
        sku = item.get("sku", "")
        item_id = item.get("item_id")
        has_zoho_image = item.get("image_name") or item.get("images") or item.get("image_document_id")
        
        # Filter by specific SKU if provided
        if args.sku and sku != args.sku:
            continue
        
        # Check if missing image in Zoho
        if not has_zoho_image:
            local_image = find_local_image(sku)
            if local_image:
                to_upload.append({
                    "sku": sku,
                    "item_id": item_id,
                    "name": item.get("name", ""),
                    "local_image": local_image
                })
    
    if not to_upload:
        if args.sku:
            print(f"No images to upload for SKU {args.sku}")
            # Check why
            item = next((i for i in all_items if i.get("sku") == args.sku), None)
            if item:
                has_img = item.get("image_name") or item.get("images") or item.get("image_document_id")
                local_img = find_local_image(args.sku)
                print(f"  - Has Zoho image: {bool(has_img)}")
                print(f"  - Has local image: {local_img}")
            else:
                print(f"  - SKU {args.sku} not found in Zoho")
        else:
            print("No images to upload - all products either have Zoho images or no local images")
        return
    
    print(f"Found {len(to_upload)} items to upload:\n")
    
    # Process uploads
    success_count = 0
    fail_count = 0
    
    for item in to_upload:
        sku = item["sku"]
        name = item["name"][:40]
        local_image = item["local_image"]
        
        if args.upload:
            print(f"  ⬆️  Uploading {sku}: {name}...")
            success, result = zoho.upload_image(item["item_id"], local_image)
            if success:
                print(f"      ✅ Success")
                success_count += 1
            else:
                print(f"      ❌ Failed: {result}")
                fail_count += 1
        else:
            print(f"  📷 {sku}: {name}")
            print(f"      Local: {local_image.name}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if args.upload:
        print(f"✅ Uploaded: {success_count}")
        print(f"❌ Failed: {fail_count}")
    else:
        print(f"📷 Ready to upload: {len(to_upload)} images")
        print("\nRun with --upload to actually upload to Zoho")


if __name__ == "__main__":
    main()
