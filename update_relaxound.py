import json
import shutil
import os
from pathlib import Path

# Paths
BACKEND_DIR = "/Users/matt/Desktop/home-and-verse/backend"
PRODUCTS_FILE = f"{BACKEND_DIR}/data/products.json"
IMAGES_DIR = f"{BACKEND_DIR}/data/images"
RELAXOUND_DIR = "/Users/matt/Desktop/Relaxound 2026/Master Folder"
MOOD_DIR = "/Users/matt/Desktop/Relaxound 2026/MOOD SHOTS"

# Load products
with open(PRODUCTS_FILE) as f:
    data = json.load(f)

products = data.get("products", data)

# Relaxound product descriptions - compelling, lifestyle-focused copy
DESCRIPTIONS = {
    # ZWITSCHERBOX (Bird chirping - 2 minutes)
    "zwitscherbox": {
        "base": "Bring the calming sounds of a forest morning into your home. The Zwitscherbox plays two minutes of authentic birdsong, activated by a built-in motion sensor whenever you walk past. Mount it by the bathroom mirror for a peaceful start to your day, in the hallway to greet you home, or anywhere you need a moment of natural calm. The volume adjusts to suit your space, and three AA batteries provide months of gentle chirping.",
        "variants": {
            "red": " The bold red finish makes a striking statement while delivering soothing birdsong with every passing movement.",
            "black": " Sleek and minimalist in black, this sound box brings natural birdsong into contemporary spaces.",
            "grey": " Understated grey complements any decor while filling your space with refreshing birdsong.",
            "oak": " Real oak veneer brings natural warmth, perfectly matched to the forest birdsong within.",
            "bamboo": " Sustainable bamboo meets natural soundscapes - an eco-conscious choice for mindful living.",
            "walnut": " Rich walnut wood grain adds sophistication while the birdsong within soothes the soul.",
            "forest": " A woodland-inspired design housing the sounds of the forest it celebrates.",
            "viola": " Soft violet tones create a calming presence, enhanced by gentle bird melodies.",
            "robin": " Featuring the distinctive call of the robin redbreast - Britain's favourite garden bird.",
        }
    },
    
    # BIRDYBOX (Premium bird chirping)
    "birdybox": {
        "base": "The premium Birdybox elevates the birdsong experience with refined materials and authentic sound. Motion-activated for hands-free relaxation, it brings two minutes of forest ambiance to your home. Perfect for bathrooms, hallways, or anywhere you want nature's gentle reminder to pause and breathe.",
        "variants": {
            "oak": " Steamed oak brings depth and character to this premium birdsong box.",
            "terrazzo": " Contemporary terrazzo finish meets timeless natural sounds.",
            "brass": " Elegant brass accents add a touch of luxury to your daily soundscape.",
            "copper": " Warm copper tones create an inviting presence.",
        }
    },
    
    # LAKESIDEBOX (Forest lake - 2 minutes) 
    "lakesidebox": {
        "base": "Close your eyes and find yourself at a tranquil forest lake. Water gently lapping, birds calling across the water, crickets chirping in the reeds. The Lakesidebox plays two minutes of this immersive soundscape whenever you pass by, thanks to its motion sensor. Rechargeable and wall-mountable, it transforms any room into a peaceful retreat.",
        "variants": {
            "birch": " Birch-effect finish evokes the silver-barked trees that line Nordic lakeshores.",
            "white": " Clean white design lets the calming lake sounds take centre stage.",
            "peach": " Soft peach brings a gentle warmth to your lakeside escape.",
            "oak": " Natural oak finish grounds the water sounds in earthy elegance.",
            "lime": " Fresh lime adds a vibrant pop while lake sounds soothe.",
            "orange": " Bright orange energises while water sounds calm - the perfect balance.",
            "forest": " A forest lake scene wraps around this box of woodland tranquility.",
            "neon": " Bold neon brings modern energy to ancient natural sounds.",
        }
    },
    
    # OCEANBOX (Ocean waves - 100 seconds)
    "oceanbox": {
        "base": "Feel the pull of the tide with every passing step. The Oceanbox plays 100 seconds of rolling waves and distant seagulls, triggered by motion sensor whenever you walk by. It's an instant escape to the coast - the fresh sea air almost tangible. Wall-mount it in your bathroom for a coastal spa feel, or let it transport your living room to the shoreline.",
        "variants": {
            "waves": " Wave-pattern design echoes the ocean sounds within.",
            "white": " Crisp white captures the clean freshness of sea spray.",
            "oak": " Warm oak brings a beachside cabin feel to the ocean sounds.",
            "vintage": " Nostalgic vintage styling evokes classic seaside holidays.",
            "alder": " Alder wood finish connects you to coastal woodland.",
            "baltic": " Inspired by the Baltic Sea - gentle waves and crying gulls.",
            "seagull": " Inspired by the Baltic Sea - gentle waves and crying gulls.",
            "sky": " Sky blue captures the endless horizon where sea meets sky.",
            "surf": " Dynamic surf design for those who live for the waves.",
            "sun": " Sun-kissed warmth meets the refreshing ocean breeze.",
        }
    },
    
    # JUNGLEBOX (Tropical jungle - 120 seconds)
    "junglebox": {
        "base": "Escape to the rainforest canopy with 120 seconds of authentic Malaysian jungle ambiance. Exotic birds call through the trees, insects hum in the undergrowth, and distant wildlife rustles through the foliage. Motion-activated and rechargeable, the Junglebox transforms any room into a tropical sanctuary.",
        "variants": {
            "white": " Clean white creates a gallery-like frame for the exotic sounds within.",
            "lush": " Lush green design mirrors the verdant jungle it celebrates.",
            "rosy": " Soft rosy pink brings a feminine touch to tropical escape.",
            "oak": " Natural oak grounds the exotic sounds in familiar warmth.",
            "tropic": " Vibrant tropical artwork wraps around authentic jungle sounds.",
            "maliau": " Named for Malaysia's Lost World - pristine rainforest captured in sound.",
        }
    },
}

# Image mappings (SKU -> image file in Relaxound folder)
IMAGE_MAPPINGS = {
    # Zwitscherbox
    "11ZBX0101004": "Relaxound_Zwitscherbox_Red_FrontLow02.jpg",
    "11ZBX0101002": "Zwitscherbox_black_front_1.jpg",
    "11ZBX0101018": "Relaxound_Zwitscherbox_Grey_FrontLow.jpg",
    "11ZBX0201004": "Zwitscherbox_Oak_Front.jpg",
    "11ZBX0200002": "Zwitscherbox_bamboo_front_shadow.jpg",
    "11ZBX0202007": "Zwitscherbox_walnut_dark_front_shadow.jpg",
    "11ZBX0701004": "Zwitscherbox_forest_front_cutout.jpg",
    "11ZBX0301007": "Zwitscherbox_viola_front.jpg",
    "11ZBX0301018": "Zwitscherbox_Ambient_Robin.jpg",
    
    # Birdybox
    "11BBX0201003": "Birdybox_oak_frontlow.jpg",
    "11BBX0801002": "Birdybox_JesmoniteTerrazzo_FrontLow_03.jpg",
    
    # Lakesidebox
    "11LSB0201009": "Relaxound_LakesideBox_FrontLow_Birke_04_flattened.jpg",
    "11LSB0101004": "Relaxound_LakesideBox_Peach_FrontLow_flat02.jpg",
    
    # Oceanbox
    "11OBX0101001": "Oceanbox_waves_front.jpg",
    "11OBX0101002": "Relaxound_OceanBox_Weiss_FrontLow_01.jpg",
    "11OBX0201003": "Relaxound_OceanBox_Oak_FrontLow_01.jpg",
    "11OBX0201001": "Relaxound_OceanBox_Vintage_FrontLow_02.jpg",
    "11OBX0301005": "Relaxound_OceanBox_Alder_FrontLow_01.jpg",
    
    # Junglebox
    "11JGL0101001": "JungleBox_White_FrontLow_001.jpg",
    "11JGL0101003": "Relaxound_JungleBox_Lush_FrontLow_flat04.jpg",
    "11JGL0101002": "Relaxound_JungleBox_Rosy_FrontLow_02.jpg",
    "11JGL0201002": "Relaxound_JungleBox_Oak_FrontLow_02.jpg",
    "11JGL0701001": "JungleBox_Tropic_FrontLow_002.jpg",
    "11JGL0701002": "Relaxound_Junglebox_Maliau_FrontLow_flat02.jpg",
}

def get_description(product_name):
    """Generate appropriate description based on product name"""
    name_lower = product_name.lower()
    
    # Determine product type
    if "birdybox" in name_lower:
        product_type = "birdybox"
    elif "zwitscherbox" in name_lower:
        product_type = "zwitscherbox"
    elif "lakesidebox" in name_lower or "lakeside box" in name_lower:
        product_type = "lakesidebox"
    elif "oceanbox" in name_lower:
        product_type = "oceanbox"
    elif "junglebox" in name_lower:
        product_type = "junglebox"
    else:
        return None
    
    desc_data = DESCRIPTIONS.get(product_type)
    if not desc_data:
        return None
    
    base_desc = desc_data["base"]
    
    # Find variant-specific addition
    variant_addition = ""
    for variant, addition in desc_data.get("variants", {}).items():
        if variant in name_lower:
            variant_addition = addition
            break
    
    return base_desc + variant_addition

def copy_image(sku, filename):
    """Copy image from Relaxound folder to backend images"""
    # Check Master Folder first
    src = os.path.join(RELAXOUND_DIR, filename)
    if not os.path.exists(src):
        # Check Mood Shots
        src = os.path.join(MOOD_DIR, filename)
    
    if not os.path.exists(src):
        print(f"  WARNING: Image not found: {filename}")
        return False
    
    dst = os.path.join(IMAGES_DIR, f"{sku}.jpg")
    shutil.copy2(src, dst)
    print(f"  Copied: {filename} -> {sku}.jpg")
    return True

# Process products
updated_count = 0
for product in products:
    if not isinstance(product, dict):
        continue
    
    name = product.get("name", "").lower()
    sku = product.get("sku", "")
    
    # Check if Relaxound product
    is_relaxound = any(x in name for x in ["zwitscherbox", "oceanbox", "lakesidebox", "junglebox", "birdybox"])
    
    if not is_relaxound:
        continue
    
    print(f"\nProcessing: {product.get('name')} ({sku})")
    
    # Update description if missing or short
    current_desc = product.get("description", "")
    if not current_desc or len(current_desc) < 50:
        new_desc = get_description(product.get("name", ""))
        if new_desc:
            product["description"] = new_desc
            print(f"  Added description ({len(new_desc)} chars)")
    
    # Copy image if mapped and either missing or we want to update
    if sku in IMAGE_MAPPINGS:
        if copy_image(sku, IMAGE_MAPPINGS[sku]):
            product["has_image"] = True
            product["image_url"] = f"/images/{sku}.jpg"
            product["images"] = [f"/images/{sku}.jpg"]
    
    updated_count += 1

# Save updated products
with open(PRODUCTS_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n\nUpdated {updated_count} Relaxound products")
print("Done!")
