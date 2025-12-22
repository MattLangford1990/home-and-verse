#!/usr/bin/env python3
"""
Setup multi-image support for Home and Verse products.

This script:
1. Scans the images folder for all images per SKU
2. Updates products.json with an 'images' array for each product
3. Imports additional images from a source folder (if provided)

Image naming convention:
- Main image: {SKU}.jpg (displayed as primary)
- Additional: {SKU}_2.jpg, {SKU}_3.jpg, etc.

The script will also recognize and rename variant patterns:
- {SKU}_1.jpg, {SKU}_V01.jpg, etc. -> {SKU}_2.jpg, {SKU}_3.jpg
"""

import json
import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

# Paths
BACKEND_DIR = Path(__file__).parent.parent
DATA_DIR = BACKEND_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
PRODUCTS_FILE = DATA_DIR / "products.json"


def get_sku_from_filename(filename):
    """Extract SKU from image filename."""
    name = Path(filename).stem  # Remove extension
    
    # Pattern: SKU followed by optional suffix (_1, _2, _V01, _t, etc.)
    # SKU can be alphanumeric with some special chars
    match = re.match(r'^([A-Za-z0-9_\-\.]+?)(?:_(?:\d+|V\d+|t|[A-Z]{2}_V\d+))?$', name)
    if match:
        return match.group(1)
    return name


def scan_existing_images():
    """Scan images folder and group by SKU."""
    sku_images = defaultdict(list)
    
    if not IMAGES_DIR.exists():
        print(f"Images directory not found: {IMAGES_DIR}")
        return sku_images
    
    for img_file in IMAGES_DIR.iterdir():
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
            filename = img_file.name
            stem = img_file.stem
            
            # Check if this is a main image (just SKU) or additional
            # Main images: exact SKU match (e.g., "17462.jpg")
            # Additional: SKU with suffix (e.g., "17462_2.jpg")
            
            sku_images[stem].append({
                'filename': filename,
                'is_main': True,
                'path': f'/images/{filename}'
            })
            
            # Also check for _2, _3 etc patterns
            match = re.match(r'^(.+?)_(\d+)$', stem)
            if match:
                base_sku = match.group(1)
                idx = int(match.group(2))
                # This is an additional image for base_sku
                if base_sku in sku_images or any(f'{base_sku}.jpg' == f['filename'] for f in sku_images.get(base_sku, [])):
                    sku_images[base_sku].append({
                        'filename': filename,
                        'is_main': False,
                        'index': idx,
                        'path': f'/images/{filename}'
                    })
    
    return sku_images


def import_additional_images(source_dir, dry_run=False):
    """
    Import additional images from a source directory.
    Renames variant patterns to sequential numbering.
    """
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Source directory not found: {source_dir}")
        return
    
    # Group source images by base SKU
    sku_source_images = defaultdict(list)
    
    for img_file in source_path.iterdir():
        if img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
            continue
        
        stem = img_file.stem
        
        # Parse different patterns
        # Pattern 1: SKU_1, SKU_2 (alternate shots)
        # Pattern 2: SKU_V01, SKU_V02 (variants)
        # Pattern 3: SKU_PH_V01, SKU_PL_V01 (color variants)
        # Pattern 4: SKU_t (thumbnail - skip)
        
        if stem.endswith('_t'):
            continue  # Skip thumbnails
        
        # Extract base SKU
        patterns = [
            (r'^(\d+)_(\d+)$', 'alternate'),           # 17462_1
            (r'^(\d+)_V(\d+)$', 'variant'),            # 18187_V01
            (r'^(\d+)_([A-Z]{2})_V(\d+)$', 'color'),   # 18264_PH_V01
            (r'^(\d+)$', 'main'),                       # 17462
        ]
        
        for pattern, img_type in patterns:
            match = re.match(pattern, stem)
            if match:
                base_sku = match.group(1)
                sku_source_images[base_sku].append({
                    'file': img_file,
                    'type': img_type,
                    'stem': stem,
                })
                break
    
    # Process each SKU
    imported_count = 0
    for sku, images in sku_source_images.items():
        # Check what already exists
        existing_main = IMAGES_DIR / f"{sku}.jpg"
        
        # Find highest existing index
        existing_indices = [1]  # Main counts as 1
        for f in IMAGES_DIR.iterdir():
            match = re.match(rf'^{re.escape(sku)}_(\d+)\.', f.name)
            if match:
                existing_indices.append(int(match.group(1)))
        
        next_index = max(existing_indices) + 1
        
        for img_info in images:
            src_file = img_info['file']
            img_type = img_info['type']
            
            if img_type == 'main':
                # Only copy main if doesn't exist
                if not existing_main.exists():
                    dest = IMAGES_DIR / f"{sku}{src_file.suffix}"
                    if not dry_run:
                        shutil.copy2(src_file, dest)
                    print(f"{'[DRY RUN] ' if dry_run else ''}Copy main: {src_file.name} -> {dest.name}")
                    imported_count += 1
            else:
                # Additional image - assign next index
                dest = IMAGES_DIR / f"{sku}_{next_index}{src_file.suffix}"
                if not dry_run:
                    shutil.copy2(src_file, dest)
                print(f"{'[DRY RUN] ' if dry_run else ''}Copy additional: {src_file.name} -> {dest.name}")
                next_index += 1
                imported_count += 1
    
    return imported_count


def update_products_json():
    """Update products.json with images arrays."""
    if not PRODUCTS_FILE.exists():
        print(f"Products file not found: {PRODUCTS_FILE}")
        return
    
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('products', [])
    
    # Build lookup of available images
    available_images = defaultdict(list)
    for img_file in IMAGES_DIR.iterdir():
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
            stem = img_file.stem
            ext = img_file.suffix
            
            # Check if main image or additional
            match = re.match(r'^(.+?)_(\d+)$', stem)
            if match:
                base_sku = match.group(1)
                idx = int(match.group(2))
                available_images[base_sku].append({
                    'path': f'/images/{img_file.name}',
                    'index': idx,
                    'is_main': False
                })
            else:
                # This is a main image
                available_images[stem].append({
                    'path': f'/images/{img_file.name}',
                    'index': 1,
                    'is_main': True
                })
    
    # Update each product
    updated_count = 0
    for product in products:
        sku = product.get('sku')
        if not sku:
            continue
        
        images = available_images.get(sku, [])
        if images:
            # Sort: main first, then by index
            images.sort(key=lambda x: (0 if x['is_main'] else 1, x['index']))
            product['images'] = [img['path'] for img in images]
            product['has_image'] = True
            product['image_url'] = images[0]['path']  # Main image
            
            if len(images) > 1:
                updated_count += 1
                print(f"  {sku}: {len(images)} images")
        else:
            product['images'] = []
    
    # Save updated products
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated {updated_count} products with multiple images")
    return updated_count


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Setup multi-image support')
    parser.add_argument('--import-from', help='Source directory to import additional images from')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without making them')
    args = parser.parse_args()
    
    print("=" * 50)
    print("Multi-Image Setup for Home and Verse")
    print("=" * 50)
    
    if args.import_from:
        print(f"\n1. Importing images from: {args.import_from}")
        imported = import_additional_images(args.import_from, dry_run=args.dry_run)
        print(f"   Imported: {imported} images")
    
    if not args.dry_run:
        print("\n2. Updating products.json with image arrays...")
        update_products_json()
    
    print("\nDone!")


if __name__ == '__main__':
    main()
