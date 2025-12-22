import json
import os
import shutil
from pathlib import Path

# Paths
MASTER_FOLDER = '/Users/matt/Desktop/Relaxound 2026/Master Folder'
MOOD_FOLDER = '/Users/matt/Desktop/Relaxound 2026/MOOD SHOTS'
IMAGES_DIR = '/Users/matt/Desktop/home-and-verse/backend/data/images'

with open('data/products.json') as f:
    data = json.load(f)

# Mapping of SKUs to image search patterns
# Format: SKU -> (search_patterns_in_master, search_patterns_in_mood)
image_mapping = {
    # Zwitscherbox
    '11ZBX0101004': (['Zwitscherbox_Red'], ['Zwitscherbox']),  # Red
    '11ZBX0200002': (['Zwitscherbox_Bamboo'], []),  # Bamboo - no specific images
    '11ZBX0101002': (['Zwitscherbox_Black'], []),  # Black
    '11ZBX0701004': (['Zwitscherbox_Forest', 'Zwitscherbox_Green'], []),  # Forest
    '11ZBX0101018': (['Zwitscherbox_Grey'], []),  # Grey
    '11ZBX0201004': (['Zwitscherbox_Oak'], []),  # Oak
    '11ZBX0301018': (['Zwitscherbox_Red'], []),  # Robin Redbreast (red box)
    '11ZBX0301007': (['Zwitscherbox_Viola'], []),  # Viola
    '11ZBX0202007': (['Zwitscherbox_Walnut'], []),  # Walnut Dark
    
    # Birdybox
    '11BBX0201003': (['Birdybox_Oak', 'Birdybox_Steamed'], ['Birdybox_Oak']),  # Steamed Oak
    '11BBX0801002': (['Birdybox_Terrazzo', 'Birdybox_Toffee'], ['Birdybox']),  # Toffee Terrazzo
    
    # Junglebox
    '11JGL0101003': (['Junglebox_Lush', 'JungleBox_Lush'], ['Junglebox_lush']),  # Lush
    '11JGL0701002': (['Junglebox_Maliau'], ['Maliau']),  # Maliau
    '11JGL0201002': (['JungleBox_Oak', 'Junglebox_Oak'], ['Junglebox_oak']),  # Oak
    '11JGL0101002': (['JungleBox_Rosy', 'Junglebox_Rosy'], ['Junglebox_rosy']),  # Rosy
    '11JGL0701001': (['Junglebox_Tropic'], ['Junglebox_Tropic']),  # Tropic
    '11JGL0101001': (['Junglebox_White', 'Junglebox_weiss'], ['Junglebox_weiss']),  # White
    
    # Lakesidebox
    '11LSB0201009': (['LakesideBox_Birch', 'LakesideBox_Birke'], ['Lakesidebox_Birch', 'Lakesidebox_birch']),  # Birch
    '11LSB0101004': (['LakesideBox_Peach'], ['Lakesidebox_peach']),  # Peach
    
    # Oceanbox
    '11OBX0301005': (['OceanBox_Baltic', 'OceanBox_Sky'], ['Oceanbox']),  # Baltic Seagull
    '11OBX0201003': (['OceanBox_Oak'], ['Oceanbox_Oak', 'Oceannox_Oak']),  # Oak
    '11OBX0201001': (['OceanBox_Vintage'], ['Oceanbox_Vintage']),  # Vintage
    '11OBX0101001': (['OceanBox_Waves', 'OceanBox_Surf'], ['Oceanbox_wave', 'Oceanbox_Waves']),  # Waves
    '11OBX0101002': (['OceanBox_White', 'OceanBox_Weiss'], ['Oceanbox_White', 'Oceanbox_white']),  # White
    
    # Zirpybox - no specific images available
    '11ZPB0701001': ([], []),  # Meadow
    '11ZPB0201001': ([], []),  # Wood
    
    # Satellitebox
    '11NIG0101001': (['Satellite', 'Nightingale'], []),  # Nightingale Green
}

def find_images(patterns, folder):
    """Find images matching any of the patterns in folder"""
    found = []
    if not os.path.exists(folder):
        return found
    
    for f in os.listdir(folder):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        if f.startswith('.'):
            continue
        # Skip duplicates with " 2" in name
        if ' 2.' in f or ' 2 ' in f:
            continue
            
        for pattern in patterns:
            if pattern.lower() in f.lower():
                found.append(os.path.join(folder, f))
                break
    
    return found

def copy_image(src, dest_name):
    """Copy image to images folder with new name"""
    dest = os.path.join(IMAGES_DIR, dest_name)
    if not os.path.exists(dest):
        shutil.copy2(src, dest)
        print(f"  Copied: {os.path.basename(src)} -> {dest_name}")
        return True
    return False

# Process each product
for product in data['products']:
    sku = product.get('sku')
    if sku not in image_mapping:
        continue
    
    master_patterns, mood_patterns = image_mapping[sku]
    
    # Get current images
    current_images = product.get('images', [])
    if not current_images and product.get('image_url'):
        current_images = [product['image_url']]
    
    print(f"\n{sku}: {product.get('name')}")
    print(f"  Current images: {len(current_images)}")
    
    # Find additional product images
    master_images = find_images(master_patterns, MASTER_FOLDER)
    mood_images = find_images(mood_patterns, MOOD_FOLDER)
    
    print(f"  Found in Master: {len(master_images)}")
    print(f"  Found in Mood: {len(mood_images)}")
    
    # Add new images (up to 5 total)
    new_images = []
    img_counter = len(current_images)
    
    # Prioritize: FrontLow/FrontHigh first, then Back, Side, Packaging, then mood shots
    all_found = master_images + mood_images
    
    # Sort by preference
    def sort_key(path):
        name = os.path.basename(path).lower()
        if 'frontlow' in name or 'fronthigh' in name:
            return 0
        if 'back' in name:
            return 1
        if 'side' in name:
            return 2
        if 'packaging' in name:
            return 3
        if 'ambient' in name or 'mood' in name:
            return 4
        return 5
    
    all_found.sort(key=sort_key)
    
    for img_path in all_found:
        if img_counter >= 5:  # Max 5 images per product
            break
        
        # Check if we already have this (by comparing base patterns)
        base = os.path.basename(img_path).lower()
        already_have = False
        for existing in current_images:
            if sku.lower() in existing.lower():
                # Simple check - if same view type, skip
                pass
        
        img_counter += 1
        ext = os.path.splitext(img_path)[1]
        new_name = f"{sku}_{img_counter}{ext}"
        
        if copy_image(img_path, new_name):
            new_images.append(f"/images/{new_name}")
    
    # Update product images array
    if new_images:
        product['images'] = current_images + new_images
        print(f"  Added {len(new_images)} new images, total: {len(product['images'])}")

# Save
with open('data/products.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n\nDone!")
