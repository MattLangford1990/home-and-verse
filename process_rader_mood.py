#!/usr/bin/env python3
"""
Process Räder mood images
- Extract SKUs from filenames
- Resize to web-friendly size
- Upload to Cloudinary as mood images
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
SOURCE_FOLDERS = [
    Path("/Users/matt/Desktop/Images 2026/Rader Images/Mood1"),
    Path("/Users/matt/Desktop/Images 2026/Rader Images/Mood 2"),
    Path("/Users/matt/Desktop/Images 2026/Rader Images/Mood 3"),
    Path("/Users/matt/Desktop/Images 2026/Rader Images/Mood 4"),
]
OUTPUT_DIR = Path("/Users/matt/Desktop/home-and-verse/processed-rader-mood")
PROGRESS_FILE = OUTPUT_DIR / "upload_progress.json"
PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")

MAX_SIZE = 1200
JPEG_QUALITY = 85

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"uploaded": [], "failed": [], "sku_mood_count": {}}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_rader_skus():
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return set(p['sku'] for p in data['products'] if p.get('brand') == 'Räder')

def extract_skus_from_filename(filename):
    """
    Extract SKUs from mood image filename
    Examples:
    - 10412_15700_17993_Kat-S_D_Div-AG_Y24_V01.jpg -> [10412, 15700, 17993]
    - 11873_Milieu_Div_AG_Div-Art_Y23_PV_V01_hgr.jpg -> [11873]
    """
    name = Path(filename).stem
    
    # Find all number sequences at the start (SKUs are typically 5 digits)
    skus = []
    parts = name.split('_')
    
    for part in parts:
        # Check if it's a number (SKU)
        if re.match(r'^\d{4,6}$', part):
            skus.append(part)
        else:
            # Stop when we hit a non-SKU part
            break
    
    return skus

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
    print("RÄDER MOOD IMAGE PROCESSOR")
    print("=" * 70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    valid_skus = load_rader_skus()
    print(f"\nRäder products in database: {len(valid_skus)}")
    
    # Collect all images from all mood folders
    all_images = []
    for folder in SOURCE_FOLDERS:
        if folder.exists():
            images = list(folder.glob("*.jpg")) + list(folder.glob("*.JPG"))
            all_images.extend(images)
            print(f"{folder.name}: {len(images)} images")
    
    print(f"\nTotal mood images: {len(all_images)}")
    
    # Load progress
    progress = load_progress()
    already_done = set(progress["uploaded"] + progress["failed"])
    sku_mood_count = progress.get("sku_mood_count", {})
    
    print(f"Already processed: {len(already_done)}")
    
    total_uploaded = 0
    total_failed = 0
    total_matched = 0
    
    for img in all_images:
        if img.name in already_done:
            continue
        
        # Extract SKUs from filename
        skus = extract_skus_from_filename(img.name)
        
        # Filter to only valid SKUs
        valid_matches = [s for s in skus if s in valid_skus]
        
        if not valid_matches:
            continue
        
        total_matched += 1
        
        # Upload for each matching SKU
        for sku in valid_matches:
            # Determine mood number for this SKU
            current_count = sku_mood_count.get(sku, 0) + 1
            sku_mood_count[sku] = current_count
            
            public_id = f"products/{sku}_mood{current_count}"
            output_name = f"{sku}_mood{current_count}.jpg"
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
                    total_uploaded += 1
                except Exception as e:
                    print(f"    Upload failed: {e}")
                    total_failed += 1
            else:
                total_failed += 1
        
        progress["uploaded"].append(img.name)
        
        # Save progress periodically
        if len(progress["uploaded"]) % 20 == 0:
            progress["sku_mood_count"] = sku_mood_count
            save_progress(progress)
            print(f"  [Progress saved: {total_uploaded} uploaded]")
    
    # Final save
    progress["sku_mood_count"] = sku_mood_count
    save_progress(progress)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print(f"Images with matching SKUs: {total_matched}")
    print(f"Total uploads: {total_uploaded}")
    print(f"Failed: {total_failed}")
    print(f"SKUs with mood images: {len(sku_mood_count)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
