#!/usr/bin/env python3
"""
Process Ideas4Seasons images for Home & Verse website
"""

import os
import json
import subprocess
from pathlib import Path
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
SOURCE_DIR = Path("/Users/matt/Downloads/Ideas4Seasons-Images")
OUTPUT_DIR = Path("/Users/matt/Desktop/home-and-verse/processed-i4s-images")
PROGRESS_FILE = OUTPUT_DIR / "upload_progress.json"
PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")

MAX_SIZE = 1200
JPEG_QUALITY = 85

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"uploaded": [], "failed": [], "no_match": []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_i4s_skus():
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return set(p['sku'] for p in data['products'] if p.get('brand') == 'Ideas4Seasons')

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
    print("IDEAS4SEASONS IMAGE PROCESSOR")
    print("=" * 70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    valid_skus = load_i4s_skus()
    print(f"\nIdeas4Seasons products in database: {len(valid_skus)}")
    
    # Get all images
    image_files = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.png")) + list(SOURCE_DIR.glob("*.JPG"))
    print(f"Images to process: {len(image_files)}")
    
    progress = load_progress()
    already_done = set(progress["uploaded"] + progress["failed"] + progress["no_match"])
    print(f"Already processed: {len(already_done)}")
    
    total_uploaded = 0
    total_failed = 0
    no_match = []
    
    for img in sorted(image_files):
        if img.name in already_done:
            continue
        
        # SKU is the filename without extension
        sku = img.stem
        
        if sku not in valid_skus:
            no_match.append(img.name)
            continue
        
        public_id = f"products/{sku}"
        output_file = OUTPUT_DIR / f"{sku}.jpg"
        
        print(f"[{sku}] {img.name} -> {public_id}")
        
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
                print(f"  Upload failed: {e}")
                progress["failed"].append(img.name)
                total_failed += 1
        else:
            progress["failed"].append(img.name)
            total_failed += 1
        
        if (total_uploaded + total_failed) % 50 == 0:
            save_progress(progress)
            print(f"  [Progress saved: {total_uploaded} uploaded, {total_failed} failed]")
    
    progress["no_match"].extend(no_match)
    save_progress(progress)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print(f"Uploaded: {total_uploaded}")
    print(f"Failed: {total_failed}")
    print(f"No matching product: {len(no_match)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
