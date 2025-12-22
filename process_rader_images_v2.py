#!/usr/bin/env python3
"""
Process remaining Räder images - Round 2
Better SKU extraction from longer filenames
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
PROGRESS_FILE = OUTPUT_DIR / "upload_progress_v2.json"
PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")

# Image settings
MAX_SIZE = 1200
JPEG_QUALITY = 85

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"uploaded": [], "failed": [], "skipped": []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_rader_skus():
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return set(p['sku'] for p in data['products'] if p.get('brand') == 'Räder')

def extract_sku(filename):
    """Extract SKU from various Räder filename formats"""
    name = Path(filename).stem
    
    # Strip leading zeros
    name_stripped = name.lstrip('0') or name
    
    # Get the first number sequence (the SKU)
    match = re.match(r'^(\d+)', name_stripped)
    if match:
        sku = match.group(1)
        
        # Check for variant indicator after SKU
        # Patterns: _01, _02, _2, _3, _hgr, _a, _b, etc
        rest = name_stripped[len(sku):]
        variant = None
        
        # Look for numeric variant like _01, _02, _2, _3
        var_match = re.search(r'_(\d+)', rest)
        if var_match:
            variant = int(var_match.group(1))
        
        return sku, variant
    
    return None, None

def resize_image(input_path, output_path):
    try:
        subprocess.run([
            'sips', '-Z', str(MAX_SIZE),
            '--setProperty', 'formatOptions', str(JPEG_QUALITY),
            '-s', 'format', 'jpeg',
            str(input_path),
            '--out', str(output_path)
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 70)
    print("RÄDER IMAGE PROCESSOR - ROUND 2")
    print("=" * 70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    valid_skus = load_rader_skus()
    print(f"\nRäder products in database: {len(valid_skus)}")
    
    # Load what was already uploaded in round 1
    round1_file = OUTPUT_DIR / "upload_progress.json"
    already_uploaded = set()
    if round1_file.exists():
        with open(round1_file) as f:
            r1 = json.load(f)
            already_uploaded = set(r1.get('uploaded', []))
    
    print(f"Already uploaded in round 1: {len(already_uploaded)}")
    
    # Get all images
    image_files = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.png"))
    print(f"Total images: {len(image_files)}")
    
    # Load round 2 progress
    progress = load_progress()
    already_done_v2 = set(progress["uploaded"] + progress["failed"] + progress["skipped"])
    
    # Group by SKU
    sku_images = defaultdict(list)
    
    for img in image_files:
        if img.name in already_uploaded or img.name in already_done_v2:
            continue
        
        sku, variant = extract_sku(img.name)
        if sku and sku in valid_skus:
            sku_images[sku].append((img, variant))
    
    print(f"New images to process: {sum(len(v) for v in sku_images.values())}")
    print(f"Unique SKUs: {len(sku_images)}")
    
    # Track what's already in Cloudinary per SKU (from round 1)
    # We need to know what suffix to use
    sku_existing_count = defaultdict(int)
    for f in already_uploaded:
        sku, var = extract_sku(f)
        if sku:
            sku_existing_count[sku] += 1
    
    total_uploaded = 0
    total_failed = 0
    
    for sku in sorted(sku_images.keys()):
        images = sku_images[sku]
        
        # Sort: no variant first, then by variant number
        images.sort(key=lambda x: (x[1] is not None, x[1] or 0))
        
        print(f"\n[{sku}] Processing {len(images)} image(s)...")
        
        # Start numbering from existing count + 1
        existing = sku_existing_count.get(sku, 0)
        
        for i, (img, variant) in enumerate(images):
            # If no images exist yet for this SKU, first one is main image
            if existing == 0 and i == 0:
                public_id = f"products/{sku}"
                output_name = f"{sku}.jpg"
            else:
                # Use variant if specified, otherwise next number
                suffix = variant if variant else (existing + i + 1)
                public_id = f"products/{sku}_{suffix}"
                output_name = f"{sku}_{suffix}.jpg"
            
            output_file = OUTPUT_DIR / output_name
            
            print(f"  {img.name[:50]}... -> {public_id}")
            
            if resize_image(img, output_file):
                try:
                    cloudinary.uploader.upload(
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
        
        if (total_uploaded + total_failed) % 50 == 0:
            save_progress(progress)
            print(f"  [Progress saved: {total_uploaded} uploaded]")
    
    save_progress(progress)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print(f"Uploaded: {total_uploaded}")
    print(f"Failed: {total_failed}")
    print(f"Total Räder images now: {len(already_uploaded) + total_uploaded}")
    print("=" * 70)

if __name__ == "__main__":
    main()
