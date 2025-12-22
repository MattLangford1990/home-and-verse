#!/usr/bin/env python3
"""
Process Räder images for Home & Verse website and DM Sales App
- Match image filenames to product SKUs (strip leading zeros)
- Resize to web-friendly sizes
- Upload to Cloudinary with proper naming
"""

import os
import re
import json
import subprocess
from pathlib import Path
from collections import defaultdict
import cloudinary
import cloudinary.uploader

# Cloudinary config
cloudinary.config(
    cloud_name="dcfbgveei",
    api_key="657552718963831",
    api_secret="CqvJk9xq5wxEcrhmOGHjFYc8r_A",
    secure=True
)

# Paths
SOURCE_DIR = Path("/Users/matt/Downloads/Rader-Images")
OUTPUT_DIR = Path("/Users/matt/Desktop/home-and-verse/processed-rader-images")
PROGRESS_FILE = OUTPUT_DIR / "upload_progress.json"
PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")

# Image settings
MAX_SIZE = 1200  # Max dimension in pixels
JPEG_QUALITY = 85

def load_progress():
    """Load upload progress"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"uploaded": [], "failed": [], "skipped": [], "no_match": []}

def save_progress(progress):
    """Save upload progress"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_rader_skus():
    """Load all Räder product SKUs from database"""
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    skus = set()
    for p in data['products']:
        if p.get('brand') == 'Räder':
            skus.add(p['sku'])
    return skus

def extract_sku_from_filename(filename):
    """
    Extract SKU from Räder filename
    Examples:
    - 0051561.jpg -> 51561
    - 0017302_3.jpg -> 17302 (variant 3)
    - 00307.jpg -> 307
    """
    name = Path(filename).stem
    
    # Check for variant suffix like _3, _2, etc.
    variant = None
    if '_' in name:
        parts = name.rsplit('_', 1)
        name = parts[0]
        if parts[1].isdigit():
            variant = int(parts[1])
    
    # Strip leading zeros
    sku = name.lstrip('0') or '0'
    
    return sku, variant

def resize_image(input_path, output_path, max_size=1200, quality=85):
    """Resize image and convert to JPEG using sips"""
    try:
        subprocess.run([
            'sips', '-Z', str(max_size),
            '--setProperty', 'formatOptions', str(quality),
            '-s', 'format', 'jpeg',
            str(input_path),
            '--out', str(output_path)
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"    Error processing {input_path.name}: {e}")
        return False

def main():
    print("=" * 70)
    print("RÄDER IMAGE PROCESSOR FOR HOME & VERSE")
    print("=" * 70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load Räder SKUs from database
    valid_skus = load_rader_skus()
    print(f"\nRäder products in database: {len(valid_skus)}")
    
    # Get all image files
    image_files = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.png")) + list(SOURCE_DIR.glob("*.jpeg"))
    print(f"Images to process: {len(image_files)}")
    
    # Load progress
    progress = load_progress()
    already_done = set(progress["uploaded"] + progress["failed"] + progress["skipped"] + progress["no_match"])
    print(f"Already processed: {len(already_done)}")
    
    # Group images by SKU
    sku_images = defaultdict(list)
    no_match = []
    
    for img in image_files:
        if img.name in already_done:
            continue
        
        sku, variant = extract_sku_from_filename(img.name)
        
        if sku in valid_skus:
            sku_images[sku].append((img, variant))
        else:
            no_match.append(img.name)
    
    print(f"Images with matching SKUs: {sum(len(v) for v in sku_images.values())}")
    print(f"Images without match: {len(no_match)}")
    print(f"Unique SKUs to upload: {len(sku_images)}")
    
    # Process each SKU
    total_uploaded = 0
    total_failed = 0
    
    for sku in sorted(sku_images.keys()):
        images = sku_images[sku]
        
        # Sort by variant (None first, then 2, 3, etc.)
        images.sort(key=lambda x: (x[1] is not None, x[1] or 0))
        
        print(f"\n[{sku}] Processing {len(images)} image(s)...")
        
        for i, (img, variant) in enumerate(images):
            # First image (no variant) is main, variants become _2, _3, etc.
            if variant is None and i == 0:
                public_id = f"products/{sku}"
                output_name = f"{sku}.jpg"
            else:
                # Use variant number if specified, otherwise use position
                suffix = variant if variant else (i + 1)
                public_id = f"products/{sku}_{suffix}"
                output_name = f"{sku}_{suffix}.jpg"
            
            output_file = OUTPUT_DIR / output_name
            
            print(f"  {img.name} -> {public_id}")
            
            if resize_image(img, output_file):
                try:
                    result = cloudinary.uploader.upload(
                        str(output_file),
                        public_id=public_id,
                        overwrite=True,
                        resource_type='image'
                    )
                    progress["uploaded"].append(img.name)
                    total_uploaded += 1
                except Exception as e:
                    print(f"    Upload failed: {e}")
                    progress["failed"].append(img.name)
                    total_failed += 1
            else:
                progress["failed"].append(img.name)
                total_failed += 1
        
        # Save progress periodically
        if (total_uploaded + total_failed) % 50 == 0:
            save_progress(progress)
            print(f"  [Progress saved: {total_uploaded} uploaded, {total_failed} failed]")
    
    # Record no-match files
    progress["no_match"].extend(no_match)
    
    # Final save
    save_progress(progress)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print(f"Uploaded: {total_uploaded}")
    print(f"Failed: {total_failed}")
    print(f"No matching product: {len(no_match)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
