import json
import shutil
import os

# Paths
BACKEND_DIR = "/Users/matt/Desktop/home-and-verse/backend"
PRODUCTS_FILE = f"{BACKEND_DIR}/data/products.json"
IMAGES_DIR = f"{BACKEND_DIR}/data/images"
MOOD_DIR = "/Users/matt/Desktop/Relaxound 2026/MOOD SHOTS"

# Load products
with open(PRODUCTS_FILE) as f:
    data = json.load(f)

products = data.get("products", data)

# Mood shot mappings - additional lifestyle images for product pages
# Format: SKU -> [(filename, suffix), ...]
MOOD_MAPPINGS = {
    # Zwitscherbox
    "11ZBX0101004": [("Zwitscherbox_Red_bathroom.jpg", "_mood1")],  # Red
    "11ZBX0201004": [("Zwitscherbox_Oak_bathroom2.jpg", "_mood1")],  # Oak
    "11ZBX0200002": [("Zwitscherbox_Bamboo_bathroom.jpg", "_mood1")],  # Bamboo
    
    # Birdybox  
    "11BBX0201003": [("Birdybox_Oak_Ambient.jpg", "_mood1"), ("Birdybox_Oak_hallway_1_landscape.jpg", "_mood2")],
    "11BBX0801002": [("221109_BB-Terrazzo_Mood-Kueche.jpg", "_mood1")],
    
    # Lakesidebox
    "11LSB0201009": [("Lakesidebox_Birch_Desk_1_landscape.jpg", "_mood1"), ("Lakesidebox_birch_homeoffice_landscape.jpg", "_mood2")],
    "11LSB0101004": [("lakesidebox_peach.jpg", "_mood1")],
    
    # Oceanbox
    "11OBX0201001": [("Oceanbox_Vintage_sideboard.jpg", "_mood1"), ("Oceanbox_Vintage_bathroom_landscape.jpg", "_mood2")],
    "11OBX0201003": [("Oceanbox_Ambient_Oak.jpg", "_mood1")],
    "11OBX0101001": [("Oceanbox_wave_bathroom_landscape.jpg", "_mood1")],
    "11OBX0101002": [("Oceanbox_White_bathroom_1_landscape.jpg", "_mood1")],
    "11OBX0301005": [("Oceanbox_Alder_Ambient.jpg", "_mood1")],
    
    # Junglebox
    "11JGL0101003": [("Junglebox_lush.jpg", "_mood1"), ("Junglebox_lush_2.jpg", "_mood2")],
    "11JGL0101002": [("Junglebox_rosy.jpg", "_mood1"), ("Junglebox_rosy_2.jpg", "_mood2")],
    "11JGL0201002": [("Junglebox_oak.jpg", "_mood1")],
    "11JGL0701001": [("Junglebox_Tropic.jpg", "_mood1")],
    "11JGL0701002": [("JB_Maliau_ambient.jpg", "_mood1")],
}

def copy_mood_image(sku, filename, suffix):
    """Copy mood image and add to product images array"""
    src = os.path.join(MOOD_DIR, filename)
    if not os.path.exists(src):
        print(f"  WARNING: Mood image not found: {filename}")
        return None
    
    new_filename = f"{sku}{suffix}.jpg"
    dst = os.path.join(IMAGES_DIR, new_filename)
    shutil.copy2(src, dst)
    print(f"  Copied mood: {filename} -> {new_filename}")
    return f"/images/{new_filename}"

# Process products
updated_count = 0
for product in products:
    if not isinstance(product, dict):
        continue
    
    sku = product.get("sku", "")
    
    if sku not in MOOD_MAPPINGS:
        continue
    
    print(f"\nProcessing: {product.get('name')} ({sku})")
    
    # Get current images array
    images = product.get("images", [])
    if not images and product.get("image_url"):
        images = [product.get("image_url")]
    
    # Add mood images
    for filename, suffix in MOOD_MAPPINGS[sku]:
        image_url = copy_mood_image(sku, filename, suffix)
        if image_url and image_url not in images:
            images.append(image_url)
    
    product["images"] = images
    updated_count += 1

# Save updated products
with open(PRODUCTS_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n\nAdded mood images to {updated_count} products")
print("Done!")
