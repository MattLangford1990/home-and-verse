#!/usr/bin/env python3
"""
Import Räder images to Home and Verse
- Copies main product images to the images folder
- Identifies products missing from database
"""

import os
import shutil
import json
import re

# Paths
SOURCE_DIR = "/Users/matt/Desktop/imageCollection-2025-12-14-20-23-12"
DEST_DIR = "/Users/matt/Desktop/home-and-verse/backend/data/images"
PRODUCTS_FILE = "/Users/matt/Desktop/home-and-verse/backend/data/products.json"

def load_products():
    """Load product SKUs from database"""
    with open(PRODUCTS_FILE, 'r') as f:
        data = json.load(f)
    products = data.get('products', data) if isinstance(data, dict) else data
    return {p.get('sku') for p in products}

def get_image_info(filename):
    """
    Parse image filename to extract base SKU and type
    Returns: (base_sku, image_type, extension)
    
    Examples:
    - 17462.jpg -> ('17462', 'main', 'jpg')
    - 17462_1.jpg -> ('17462', 'alt_1', 'jpg')
    - 17462_t.jpg -> ('17462', 'thumb', 'jpg')
    - 18187_V01.jpg -> ('18187', 'variant_V01', 'jpg')
    - 18264_PH_V01.jpg -> ('18264', 'variant_PH_V01', 'jpg')
    """
    name, ext = os.path.splitext(filename)
    ext = ext.lstrip('.')
    
    # Main image: just the code
    if re.match(r'^\d+$', name):
        return (name, 'main', ext)
    
    # Parse suffix
    match = re.match(r'^(\d+)_(.+)$', name)
    if match:
        base_sku, suffix = match.groups()
        if suffix == 't':
            return (base_sku, 'thumb', ext)
        elif suffix.isdigit():
            return (base_sku, f'alt_{suffix}', ext)
        else:
            return (base_sku, f'variant_{suffix}', ext)
    
    return (name, 'unknown', ext)

def main():
    # Load existing SKUs
    existing_skus = load_products()
    print(f"Loaded {len(existing_skus)} products from database\n")
    
    # Get all images from source
    images = os.listdir(SOURCE_DIR)
    print(f"Found {len(images)} images in source folder\n")
    
    # Categorise images
    main_images = []
    variant_images = []
    missing_from_db = set()
    
    for img in images:
        base_sku, img_type, ext = get_image_info(img)
        
        if img_type == 'main':
            main_images.append((img, base_sku))
            if base_sku not in existing_skus:
                missing_from_db.add(base_sku)
        else:
            variant_images.append((img, base_sku, img_type))
    
    # Report missing products
    if missing_from_db:
        print("⚠️  PRODUCTS MISSING FROM DATABASE (need adding to Zoho first):")
        for sku in sorted(missing_from_db):
            print(f"   - {sku}")
        print()
    
    # Copy main images
    print("📁 Copying main product images...")
    copied = 0
    skipped = 0
    
    for img, base_sku in main_images:
        src = os.path.join(SOURCE_DIR, img)
        dst = os.path.join(DEST_DIR, img)
        
        if os.path.exists(dst):
            print(f"   ⏭️  Skipped {img} (already exists)")
            skipped += 1
        else:
            shutil.copy2(src, dst)
            status = "✅" if base_sku in existing_skus else "⚠️ (not in DB)"
            print(f"   {status} Copied {img}")
            copied += 1
    
    print(f"\n📊 Summary:")
    print(f"   Main images copied: {copied}")
    print(f"   Main images skipped (existing): {skipped}")
    print(f"   Products missing from DB: {len(missing_from_db)}")
    print(f"   Variant/alt images available: {len(variant_images)}")
    
    # List variant images for reference
    if variant_images:
        print(f"\n📸 Variant images (not imported - your system uses single images):")
        for img, base_sku, img_type in sorted(variant_images):
            print(f"   - {img} ({img_type})")
    
    print("\n✅ Done!")
    print("\nNext steps:")
    print("1. Add missing products to Zoho CRM")
    print("2. Re-import products to sync the database")
    print("3. Upload images to Zoho (if using Zoho for image hosting)")

if __name__ == "__main__":
    main()
