"""
Home & Verse - Product Description Generator
=============================================
Generates SEO-friendly descriptions for products with thin/missing content.

Usage:
    cd /Users/matt/Desktop/home-and-verse/backend
    python3 generate_descriptions.py
"""

import json
import re
from pathlib import Path

# Paths
DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"
OUTPUT_FILE = DATA_DIR / "products.json"

# Minimum description length to be considered "good"
MIN_DESCRIPTION_LENGTH = 80

# Brand descriptions for context
BRAND_CONTEXT = {
    "Räder": {
        "origin": "German",
        "style": "minimalist Scandinavian-inspired",
        "known_for": "poetic porcelain and atmospheric lighting",
        "aesthetic": "understated elegance with clean lines"
    },
    "Remember": {
        "origin": "German",
        "style": "bold and colourful",
        "known_for": "vibrant homeware that celebrates colour and pattern",
        "aesthetic": "playful sophistication with geometric designs"
    },
    "My Flame": {
        "origin": "Dutch",
        "style": "contemporary",
        "known_for": "hand-poured soy candles with hidden messages",
        "aesthetic": "thoughtful gifting with beautiful fragrance"
    },
    "Relaxound": {
        "origin": "German",
        "style": "innovative",
        "known_for": "nature soundboxes including the original Zwitscherbox",
        "aesthetic": "bringing nature indoors through sound"
    }
}

# Category-specific description elements
CATEGORY_TEMPLATES = {
    "Christmas": [
        "Perfect for adding festive charm to your home.",
        "A wonderful addition to your Christmas decorations.",
        "Brings warmth and magic to the festive season.",
        "An ideal gift for the holiday season."
    ],
    "Candles & Fragrance": [
        "Creates a warm, inviting atmosphere in any room.",
        "Perfect for moments of relaxation and calm.",
        "Fills your home with beautiful fragrance.",
        "An ideal way to unwind after a long day."
    ],
    "Lighting": [
        "Casts a beautiful warm glow in any space.",
        "Creates atmospheric lighting for cosy evenings.",
        "Perfect for adding ambiance to your home.",
        "Brings warmth and character to any room."
    ],
    "Tableware": [
        "Elevates your dining experience with thoughtful design.",
        "Perfect for everyday use or special occasions.",
        "Adds a touch of European style to your table.",
        "Makes every meal feel special."
    ],
    "Home Décor": [
        "A beautiful accent piece for any room.",
        "Adds character and charm to your living space.",
        "Perfect for creating a stylish, curated home.",
        "Brings European design flair to your interior."
    ],
    "Gifts": [
        "A thoughtful gift for someone special.",
        "Perfect for birthdays, housewarmings, or just because.",
        "Beautifully presented and ready to give.",
        "A unique gift they'll treasure."
    ]
}

# Product type descriptions
PRODUCT_TYPES = {
    "candle": "hand-poured candle",
    "light house": "porcelain light house",
    "lighthouse": "decorative lighthouse",
    "lantern": "atmospheric lantern",
    "vase": "elegant vase",
    "bowl": "decorative bowl",
    "plate": "beautiful plate",
    "mug": "ceramic mug",
    "cup": "stylish cup",
    "napkin": "quality paper napkins",
    "coaster": "practical coasters",
    "cushion": "comfortable cushion",
    "towel": "quality towel",
    "basket": "woven basket",
    "tray": "serving tray",
    "jar": "storage jar",
    "box": "decorative box",
    "figure": "decorative figure",
    "ornament": "beautiful ornament",
    "card": "greeting card",
    "keychain": "keychain",
    "keyring": "keyring",
    "game": "entertaining game",
    "puzzle": "challenging puzzle",
    "soap": "luxurious soap",
    "diffuser": "reed diffuser",
    "bath bomb": "fizzing bath bombs",
    "zwitscherbox": "nature soundbox",
    "birdybox": "birdsong soundbox",
    "relaxound": "nature soundbox",
    "etagere": "tiered serving stand",
    "advent": "advent calendar",
    "bauble": "Christmas bauble",
    "star": "decorative star",
    "angel": "angel decoration",
    "santa": "Santa decoration",
    "tree": "decorative tree",
    "apron": "kitchen apron",
    "bottle opener": "bottle opener",
    "carafe": "glass carafe",
    "glass": "drinking glass",
    "espresso": "espresso cup",
    "egg cup": "egg cup",
    "lamp": "table lamp",
    "uri": "portable LED lamp",
    "fan": "portable fan",
    "rug": "decorative rug",
    "blanket": "cosy blanket",
    "pillow": "decorative pillow"
}


def get_product_type(name: str) -> str:
    """Extract product type from name"""
    name_lower = name.lower()
    for keyword, description in PRODUCT_TYPES.items():
        if keyword in name_lower:
            return description
    return "decorative piece"


def extract_color(name: str) -> str:
    """Extract color from product name if present"""
    colors = [
        "white", "black", "grey", "gray", "blue", "green", "red", "pink", 
        "yellow", "orange", "purple", "gold", "silver", "coral", "teal",
        "mint", "sage", "navy", "cream", "beige", "natural", "olive"
    ]
    name_lower = name.lower()
    for color in colors:
        if color in name_lower:
            return color
    return None


def extract_size(name: str) -> str:
    """Extract size from product name if present"""
    # Look for patterns like "large", "small", "set of X"
    name_lower = name.lower()
    if "large" in name_lower:
        return "large"
    if "small" in name_lower:
        return "small"
    if "mini" in name_lower:
        return "mini"
    
    # Set of X
    match = re.search(r'set of (\d+)', name_lower)
    if match:
        return f"set of {match.group(1)}"
    
    return None


def generate_description(product: dict) -> str:
    """Generate a rich SEO-friendly description for a product"""
    name = product.get("name", "")
    brand = product.get("brand", "")
    categories = product.get("categories", [])
    price = product.get("price", 0)
    
    # Get brand context
    brand_info = BRAND_CONTEXT.get(brand, {
        "origin": "European",
        "style": "contemporary",
        "known_for": "quality homeware",
        "aesthetic": "thoughtful design"
    })
    
    # Get product type
    product_type = get_product_type(name)
    
    # Get color and size if present
    color = extract_color(name)
    size = extract_size(name)
    
    # Build description
    parts = []
    
    # Opening line with product type and brand
    if color and size:
        opening = f"This {color} {product_type} ({size}) from {brand} showcases {brand_info['style']} design."
    elif color:
        opening = f"This {color} {product_type} from {brand} showcases {brand_info['style']} design."
    elif size:
        opening = f"This {product_type} ({size}) from {brand} showcases {brand_info['style']} design."
    else:
        opening = f"This {product_type} from {brand} showcases {brand_info['style']} design."
    parts.append(opening)
    
    # Add brand context
    parts.append(f"{brand} is known for {brand_info['known_for']}, and this piece embodies their signature {brand_info['aesthetic']}.")
    
    # Add category-specific line
    primary_category = categories[0] if categories else "Home Décor"
    category_lines = CATEGORY_TEMPLATES.get(primary_category, CATEGORY_TEMPLATES["Home Décor"])
    parts.append(category_lines[hash(name) % len(category_lines)])
    
    # Add free delivery mention if applicable
    if price >= 30:
        parts.append("Free UK delivery included.")
    
    return " ".join(parts)


def main():
    """Main function to process products"""
    
    # Load products
    if not PRODUCTS_FILE.exists():
        print(f"Error: {PRODUCTS_FILE} not found")
        return
    
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    products = data.get("products", [])
    print(f"Loaded {len(products)} products")
    
    # Count products needing descriptions
    needs_description = [p for p in products if len(p.get("description", "")) < MIN_DESCRIPTION_LENGTH]
    print(f"Products needing better descriptions: {len(needs_description)}")
    
    # Generate descriptions
    updated_count = 0
    for product in products:
        current_desc = product.get("description", "")
        
        # Only update if description is too short
        if len(current_desc) < MIN_DESCRIPTION_LENGTH:
            new_desc = generate_description(product)
            product["description"] = new_desc
            updated_count += 1
    
    print(f"Updated {updated_count} descriptions")
    
    # Save updated products
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved to {OUTPUT_FILE}")
    
    # Show some examples
    print("\n--- Sample Generated Descriptions ---")
    for product in products[:5]:
        if len(product.get("description", "")) >= MIN_DESCRIPTION_LENGTH:
            print(f"\n{product.get('name')}:")
            print(f"  {product.get('description')[:150]}...")


if __name__ == "__main__":
    main()
