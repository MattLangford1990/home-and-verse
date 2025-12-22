#!/usr/bin/env python3
"""
Process Remember HiDrive images for Home & Verse website
- Resize to web-friendly sizes
- Convert to JPEG
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
SOURCE_DIR = Path("/Users/matt/Downloads/HiDrive-Alle Fotos")
OUTPUT_DIR = Path("/Users/matt/Desktop/home-and-verse/processed-images")
PROGRESS_FILE = OUTPUT_DIR / "upload_progress.json"

# Image settings
MAX_SIZE = 1200  # Max dimension in pixels
JPEG_QUALITY = 85

def load_progress():
    """Load upload progress"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"uploaded": [], "failed": [], "skipped": []}

def save_progress(progress):
    """Save upload progress"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def extract_sku(filename):
    """Extract SKU from Remember filename
    Examples:
    - AD4_Adventskalender_Dorf_Ambiente_02_2022.jpg -> AD4
    - BK20_BK21_Blockkerzen_2er_Set_Ambiente_01_2023.jpg -> BK20 (primary)
    - KH10_Kerzenhaeuser_4er_Set_Ambiente_01_2024.jpg -> KH10
    """
    name = Path(filename).stem
    
    # Get first part before underscore - this is usually the SKU
    parts = name.split('_')
    if parts:
        # Check if it looks like a SKU (letters followed by numbers)
        sku = parts[0]
        if re.match(r'^[A-Z]{2,4}\d{1,3}$', sku):
            return sku
        # Some files have multiple SKUs like "BK20_BK21_..."
        # Return the first one
        for part in parts[:3]:
            if re.match(r'^[A-Z]{2,4}\d{1,3}$', part):
                return part
    return None

def get_image_type(filename):
    """Determine if image is product shot or mood shot"""
    name = filename.lower()
    if 'ambiente' in name:
        return 'mood'
    elif 'freisteller' in name:
        return 'product'
    else:
        return 'other'

def resize_and_convert(input_path, output_path, max_size=1200, quality=85):
    """Resize image and convert to JPEG using sips"""
    try:
        # Use sips (built into macOS) for image processing
        # First resize
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
    print("REMEMBER IMAGE PROCESSOR FOR HOME & VERSE")
    print("=" * 70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    image_files = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.png")) + list(SOURCE_DIR.glob("*.jpeg"))
    print(f"\nFound {len(image_files)} images to process")
    
    # Load progress
    progress = load_progress()
    already_done = set(progress["uploaded"] + progress["failed"] + progress["skipped"])
    print(f"Already processed: {len(already_done)}")
    
    # Group images by SKU
    sku_images = defaultdict(list)
    no_sku = []
    
    for img in image_files:
        if img.name in already_done:
            continue
        sku = extract_sku(img.name)
        if sku:
            img_type = get_image_type(img.name)
            sku_images[sku].append((img, img_type))
        else:
            no_sku.append(img)
    
    print(f"Images with valid SKUs: {sum(len(v) for v in sku_images.values())}")
    print(f"Images without SKU: {len(no_sku)}")
    print(f"Unique SKUs: {len(sku_images)}")
    
    # Process each SKU
    total_uploaded = 0
    total_failed = 0
    
    for sku in sorted(sku_images.keys()):
        images = sku_images[sku]
        print(f"\n[{sku}] Processing {len(images)} images...")
        
        # Separate product shots and mood shots
        product_shots = [(img, t) for img, t in images if t == 'product']
        mood_shots = [(img, t) for img, t in images if t == 'mood']
        other_shots = [(img, t) for img, t in images if t == 'other']
        
        # Process product shots (main product images)
        for i, (img, _) in enumerate(product_shots):
            # First product shot is main image, rest are _2, _3, etc.
            if i == 0:
                public_id = f"products/{sku}"
            else:
                public_id = f"products/{sku}_{i+1}"
            
            output_file = OUTPUT_DIR / f"{sku}_{i+1}.jpg"
            
            print(f"  Product: {img.name[:40]}... -> {public_id}")
            
            if resize_and_convert(img, output_file):
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
        
        # Process mood shots
        for i, (img, _) in enumerate(mood_shots):
            public_id = f"products/{sku}_mood{i+1}"
            output_file = OUTPUT_DIR / f"{sku}_mood{i+1}.jpg"
            
            print(f"  Mood: {img.name[:40]}... -> {public_id}")
            
            if resize_and_convert(img, output_file):
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
        if (total_uploaded + total_failed) % 20 == 0:
            save_progress(progress)
            print(f"  [Progress saved: {total_uploaded} uploaded, {total_failed} failed]")
    
    # Final save
    save_progress(progress)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print(f"Uploaded: {total_uploaded}")
    print(f"Failed: {total_failed}")
    print(f"Skipped (no SKU): {len(no_sku)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
