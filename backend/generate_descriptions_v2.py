"""
Home & Verse - Enhanced Product Description Generator V2
=========================================================
Generates rich, varied SEO-friendly descriptions using templates.
No AI tokens required - pure template-based generation.

Usage:
    cd /Users/matt/Desktop/home-and-verse/backend
    python3 generate_descriptions_v2.py
"""

import json
import re
import random
from pathlib import Path
from hashlib import md5

# Paths
DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"
OUTPUT_FILE = DATA_DIR / "products.json"

# Use product SKU as seed for consistent but varied descriptions
def get_seed(sku: str) -> int:
    return int(md5(sku.encode()).hexdigest()[:8], 16)

def pick(options: list, sku: str, offset: int = 0) -> str:
    """Pick consistently from options based on SKU"""
    seed = get_seed(sku) + offset
    return options[seed % len(options)]

# ============ BRAND DATA ============

BRAND_INFO = {
    "Räder": {
        "origin": "Germany",
        "adjectives": ["minimalist", "poetic", "elegant", "refined", "timeless"],
        "materials": ["porcelain", "ceramic", "glass"],
        "vibe": ["Scandinavian-inspired simplicity", "understated elegance", "quiet sophistication"],
        "story": "Founded in 1990, Räder creates pieces that tell stories through thoughtful design.",
        "tagline": "German craftsmanship meets Nordic simplicity."
    },
    "Remember": {
        "origin": "Germany",
        "adjectives": ["bold", "vibrant", "playful", "colourful", "cheerful"],
        "materials": ["melamine", "porcelain", "textile"],
        "vibe": ["joyful colour", "geometric patterns", "playful sophistication"],
        "story": "Remember brings colour and joy to everyday living with designs that make you smile.",
        "tagline": "Bold German design that celebrates colour."
    },
    "My Flame": {
        "origin": "the Netherlands",
        "adjectives": ["fragrant", "thoughtful", "meaningful", "heartfelt", "luxurious"],
        "materials": ["natural soy wax", "cotton wick", "glass"],
        "vibe": ["hidden surprises", "meaningful gifting", "warm ambiance"],
        "story": "Each My Flame candle reveals a hidden message as it burns - a thoughtful touch for gifting.",
        "tagline": "Hand-poured Dutch candles with hidden messages."
    },
    "Relaxound": {
        "origin": "Germany",
        "adjectives": ["innovative", "calming", "natural", "soothing", "unique"],
        "materials": ["sustainable wood", "bamboo", "recycled materials"],
        "vibe": ["nature indoors", "mindful living", "peaceful moments"],
        "story": "Relaxound's Zwitscherbox brings the sounds of nature into your home at the wave of a hand.",
        "tagline": "Bringing the sounds of nature indoors."
    },
    "GEFU": {
        "origin": "Germany",
        "adjectives": ["precision-engineered", "professional", "durable", "functional", "sleek"],
        "materials": ["stainless steel", "silicone", "high-quality plastics"],
        "vibe": ["German engineering", "kitchen excellence", "professional results"],
        "story": "Since 1943, GEFU has been creating premium kitchen tools that professionals and home cooks love.",
        "tagline": "German precision for your kitchen."
    },
    "Elvang Denmark": {
        "origin": "Denmark",
        "adjectives": ["luxurious", "soft", "sustainable", "elegant", "cosy"],
        "materials": ["alpaca wool", "baby alpaca", "merino wool"],
        "vibe": ["Scandinavian hygge", "sustainable luxury", "timeless comfort"],
        "story": "Elvang creates exquisite throws and cushions from the finest alpaca wool, woven with care.",
        "tagline": "Danish luxury in sustainable alpaca wool."
    },
    "Paper Products Design": {
        "origin": "Germany",
        "adjectives": ["artistic", "stylish", "decorative", "elegant", "festive"],
        "materials": ["FSC-certified paper", "eco-friendly materials"],
        "vibe": ["artistic expression", "table styling", "sustainable celebrations"],
        "story": "PPD creates beautiful paper products that elevate any table setting or occasion.",
        "tagline": "Artful paper products for stylish tables."
    },
    "Ideas4Seasons": {
        "origin": "Europe",
        "adjectives": ["seasonal", "decorative", "charming", "festive", "trendy"],
        "materials": ["quality materials", "durable finishes"],
        "vibe": ["seasonal styling", "on-trend décor", "affordable luxury"],
        "story": "Ideas4Seasons brings you the latest trends in seasonal and home decoration.",
        "tagline": "On-trend décor for every season."
    }
}

# Default for unknown brands
DEFAULT_BRAND = {
    "origin": "Europe",
    "adjectives": ["quality", "stylish", "elegant", "refined"],
    "materials": ["quality materials"],
    "vibe": ["European design", "thoughtful craftsmanship"],
    "story": "Carefully selected for quality and design.",
    "tagline": "European quality and style."
}

# ============ PRODUCT TYPES ============

PRODUCT_TYPES = {
    # Candles & Fragrance
    "candle": {"type": "candle", "category": "fragrance", "action": "burns", "benefit": "fills your space with beautiful fragrance"},
    "duftkerze": {"type": "scented candle", "category": "fragrance", "action": "burns", "benefit": "creates a warm, inviting atmosphere"},
    "diffuser": {"type": "reed diffuser", "category": "fragrance", "action": "diffuses", "benefit": "gently scents your room for weeks"},
    "room spray": {"type": "room spray", "category": "fragrance", "action": "freshens", "benefit": "instantly refreshes any space"},
    "wax melt": {"type": "wax melt", "category": "fragrance", "action": "melts", "benefit": "releases beautiful fragrance without flame"},
    
    # Lighting
    "light house": {"type": "porcelain light house", "category": "lighting", "action": "glows", "benefit": "casts a warm, atmospheric glow"},
    "lighthouse": {"type": "decorative lighthouse", "category": "lighting", "action": "shines", "benefit": "creates magical ambiance"},
    "lantern": {"type": "lantern", "category": "lighting", "action": "illuminates", "benefit": "adds warmth to any setting"},
    "tealight": {"type": "tealight holder", "category": "lighting", "action": "holds", "benefit": "creates flickering candlelight"},
    "lamp": {"type": "lamp", "category": "lighting", "action": "lights up", "benefit": "provides beautiful illumination"},
    "led": {"type": "LED light", "category": "lighting", "action": "glows", "benefit": "offers safe, long-lasting light"},
    
    # Tableware
    "mug": {"type": "mug", "category": "tableware", "action": "holds", "benefit": "makes every cuppa special"},
    "cup": {"type": "cup", "category": "tableware", "action": "holds", "benefit": "elevates your daily ritual"},
    "plate": {"type": "plate", "category": "tableware", "action": "presents", "benefit": "makes food look beautiful"},
    "bowl": {"type": "bowl", "category": "tableware", "action": "serves", "benefit": "perfect for serving and display"},
    "glass": {"type": "glass", "category": "tableware", "action": "holds", "benefit": "adds elegance to any drink"},
    "carafe": {"type": "carafe", "category": "tableware", "action": "pours", "benefit": "serves drinks in style"},
    "napkin": {"type": "paper napkins", "category": "tableware", "action": "complement", "benefit": "adds style to your table"},
    "coaster": {"type": "coasters", "category": "tableware", "action": "protect", "benefit": "keeps surfaces pristine"},
    "tray": {"type": "tray", "category": "tableware", "action": "serves", "benefit": "makes entertaining effortless"},
    "etagere": {"type": "serving stand", "category": "tableware", "action": "displays", "benefit": "creates a stunning centrepiece"},
    
    # Home Décor
    "vase": {"type": "vase", "category": "décor", "action": "displays", "benefit": "showcases flowers beautifully"},
    "figure": {"type": "decorative figure", "category": "décor", "action": "adorns", "benefit": "adds character to any shelf"},
    "ornament": {"type": "ornament", "category": "décor", "action": "decorates", "benefit": "brings charm to your space"},
    "cushion": {"type": "cushion", "category": "décor", "action": "softens", "benefit": "adds comfort and style"},
    "throw": {"type": "throw", "category": "décor", "action": "drapes", "benefit": "adds warmth and texture"},
    "blanket": {"type": "blanket", "category": "décor", "action": "wraps", "benefit": "provides cosy comfort"},
    "rug": {"type": "rug", "category": "décor", "action": "grounds", "benefit": "defines your space beautifully"},
    
    # Sound
    "zwitscherbox": {"type": "birdsong box", "category": "sound", "action": "plays", "benefit": "brings nature's soundtrack indoors"},
    "birdybox": {"type": "nature soundbox", "category": "sound", "action": "plays", "benefit": "creates a calming atmosphere"},
    "relaxound": {"type": "soundbox", "category": "sound", "action": "plays", "benefit": "brings peaceful sounds to your space"},
    "soundbox": {"type": "soundbox", "category": "sound", "action": "plays", "benefit": "fills your room with soothing sounds"},
    
    # Christmas
    "advent": {"type": "advent calendar", "category": "christmas", "action": "counts down", "benefit": "builds excitement for Christmas"},
    "bauble": {"type": "bauble", "category": "christmas", "action": "hangs", "benefit": "adds sparkle to your tree"},
    "star": {"type": "star decoration", "category": "christmas", "action": "shines", "benefit": "tops your tree beautifully"},
    "angel": {"type": "angel decoration", "category": "christmas", "action": "watches over", "benefit": "adds festive magic"},
    "santa": {"type": "Santa decoration", "category": "christmas", "action": "brings joy", "benefit": "captures Christmas spirit"},
    "wreath": {"type": "wreath", "category": "christmas", "action": "welcomes", "benefit": "greets guests with festive cheer"},
    
    # Kitchen
    "apron": {"type": "apron", "category": "kitchen", "action": "protects", "benefit": "keeps you clean while cooking"},
    "tea towel": {"type": "tea towel", "category": "kitchen", "action": "dries", "benefit": "adds style to your kitchen"},
    "oven glove": {"type": "oven glove", "category": "kitchen", "action": "protects", "benefit": "handles hot dishes safely"},
    "bottle opener": {"type": "bottle opener", "category": "kitchen", "action": "opens", "benefit": "makes opening bottles easy"},
    
    # Games & Puzzles
    "puzzle": {"type": "puzzle", "category": "games", "action": "challenges", "benefit": "provides hours of entertainment"},
    "game": {"type": "game", "category": "games", "action": "entertains", "benefit": "brings people together"},
    "memory": {"type": "memory game", "category": "games", "action": "tests", "benefit": "fun for all ages"},
    
    # Bath & Body
    "soap": {"type": "soap", "category": "bath", "action": "cleanses", "benefit": "pampers your skin"},
    "bath bomb": {"type": "bath bomb", "category": "bath", "action": "fizzes", "benefit": "transforms bathtime"},
    "hand cream": {"type": "hand cream", "category": "bath", "action": "nourishes", "benefit": "keeps hands soft"},
}

# ============ TEMPLATES ============

OPENING_TEMPLATES = [
    "Introducing the {product_type} from {brand} - a {adj} piece that {benefit}.",
    "This {adj} {product_type} from {brand} {benefit}.",
    "From {brand} comes this {adj} {product_type} - it {benefit}.",
    "Meet the {product_type} by {brand} - {adj} design that {benefit}.",
    "Crafted by {brand}, this {adj} {product_type} {benefit}.",
    "The {product_type} from {brand} brings {adj} style that {benefit}.",
]

MIDDLE_TEMPLATES = [
    "Made in {origin}, it reflects {vibe}.",
    "Designed in {origin} with {vibe} at its heart.",
    "A beautiful example of {vibe} from {origin}.",
    "Embodying {vibe}, it's crafted with care in {origin}.",
    "True to {brand}'s {origin} heritage, it showcases {vibe}.",
]

# Category-specific endings
CATEGORY_ENDINGS = {
    "fragrance": [
        "Perfect for creating a cosy atmosphere at home.",
        "An ideal way to scent your space beautifully.",
        "Transform any room with its beautiful fragrance.",
        "A thoughtful gift for someone who loves their home.",
    ],
    "lighting": [
        "Creates the perfect ambiance for relaxed evenings.",
        "A beautiful way to light up your home.",
        "Perfect for adding warmth to any room.",
        "Brings a magical glow to your space.",
    ],
    "tableware": [
        "Elevates everyday dining to something special.",
        "Perfect for both daily use and special occasions.",
        "A beautiful addition to any table setting.",
        "Makes entertaining effortlessly stylish.",
    ],
    "décor": [
        "A beautiful accent for any room in your home.",
        "Adds personality and charm to your space.",
        "Perfect for creating a curated, stylish interior.",
        "A piece you'll treasure for years to come.",
    ],
    "sound": [
        "Bring the calming sounds of nature into your home.",
        "Perfect for creating moments of peace and relaxation.",
        "A unique way to add tranquility to any room.",
        "The perfect antidote to busy modern life.",
    ],
    "christmas": [
        "A wonderful addition to your festive decorations.",
        "Brings magic and joy to the Christmas season.",
        "Perfect for creating cherished holiday memories.",
        "A beautiful way to celebrate the festive season.",
    ],
    "kitchen": [
        "Makes time in the kitchen more enjoyable.",
        "A practical piece with beautiful design.",
        "Perfect for anyone who loves to cook.",
        "Combines function with gorgeous style.",
    ],
    "games": [
        "Perfect for bringing friends and family together.",
        "Hours of entertainment for all ages.",
        "A wonderful gift for curious minds.",
        "Makes quality time even more fun.",
    ],
    "bath": [
        "Turn your bathroom into a spa retreat.",
        "A little luxury for everyday self-care.",
        "Perfect for pampering yourself or someone special.",
        "Makes bathtime a beautiful ritual.",
    ],
}

DEFAULT_ENDINGS = [
    "A perfect gift for someone special.",
    "Beautifully designed and made to last.",
    "A lovely addition to any home.",
    "Makes everyday moments feel special.",
]

# ============ EXTRACTION FUNCTIONS ============

def extract_color(name: str) -> str:
    colors = {
        "white": "white", "black": "black", "grey": "grey", "gray": "grey",
        "blue": "blue", "green": "green", "red": "red", "pink": "pink",
        "yellow": "yellow", "orange": "orange", "purple": "purple",
        "gold": "gold", "silver": "silver", "coral": "coral", "teal": "teal",
        "mint": "mint", "sage": "sage", "navy": "navy", "cream": "cream",
        "beige": "beige", "natural": "natural", "olive": "olive", "rose": "rose",
        "copper": "copper", "bronze": "bronze", "oak": "oak", "walnut": "walnut",
    }
    name_lower = name.lower()
    for keyword, color in colors.items():
        if keyword in name_lower:
            return color
    return None

def extract_size(name: str) -> str:
    name_lower = name.lower()
    if "large" in name_lower or "grande" in name_lower:
        return "large"
    if "small" in name_lower or "mini" in name_lower:
        return "small"
    if "medium" in name_lower:
        return "medium"
    match = re.search(r'set of (\d+)', name_lower)
    if match:
        return f"set of {match.group(1)}"
    return None

def get_product_info(name: str) -> dict:
    name_lower = name.lower()
    for keyword, info in PRODUCT_TYPES.items():
        if keyword in name_lower:
            return info
    return {"type": "piece", "category": "décor", "action": "decorates", "benefit": "adds style to your home"}

def get_brand_info(brand: str) -> dict:
    return BRAND_INFO.get(brand, DEFAULT_BRAND)

# ============ MAIN GENERATOR ============

def generate_description(product: dict) -> str:
    """Generate a rich, varied description for a product"""
    sku = product.get("sku", "")
    name = product.get("name", "")
    brand = product.get("brand", "")
    price = product.get("price", 0)
    categories = product.get("categories", [])
    
    brand_info = get_brand_info(brand)
    product_info = get_product_info(name)
    
    color = extract_color(name)
    size = extract_size(name)
    
    # Build product type string
    product_type = product_info["type"]
    if color and size:
        product_type = f"{color} {product_type} ({size})"
    elif color:
        product_type = f"{color} {product_type}"
    elif size:
        product_type = f"{product_type} ({size})"
    
    # Pick templates based on SKU for consistency
    opening = pick(OPENING_TEMPLATES, sku, 0).format(
        product_type=product_type,
        brand=brand,
        adj=pick(brand_info["adjectives"], sku, 1),
        benefit=product_info["benefit"]
    )
    
    middle = pick(MIDDLE_TEMPLATES, sku, 2).format(
        origin=brand_info["origin"],
        brand=brand,
        vibe=pick(brand_info["vibe"], sku, 3)
    )
    
    category_endings = CATEGORY_ENDINGS.get(product_info["category"], DEFAULT_ENDINGS)
    ending = pick(category_endings, sku, 4)
    
    # Build description
    parts = [opening, middle, ending]
    
    # Add delivery note for qualifying items
    if price >= 30:
        parts.append("Free UK delivery.")
    
    return " ".join(parts)

# ============ MAIN ============

def main():
    print("=" * 60)
    print("HOME & VERSE - DESCRIPTION GENERATOR V2")
    print("=" * 60)
    
    if not PRODUCTS_FILE.exists():
        print(f"Error: {PRODUCTS_FILE} not found")
        return
    
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    products = data.get("products", [])
    print(f"\nLoaded {len(products)} products")
    
    # Find products needing descriptions
    MIN_LENGTH = 80
    needs_update = [p for p in products if len(p.get("description", "")) < MIN_LENGTH]
    print(f"Products needing descriptions: {len(needs_update)}")
    
    # Also find products with generic "This decorative" descriptions
    generic_pattern = re.compile(r'^This (decorative )?(box|piece) from')
    has_generic = [p for p in products if generic_pattern.match(p.get("description", ""))]
    print(f"Products with generic descriptions: {len(has_generic)}")
    
    # Generate descriptions
    updated = 0
    for product in products:
        desc = product.get("description", "")
        
        # Update if too short or generic
        if len(desc) < MIN_LENGTH or generic_pattern.match(desc):
            new_desc = generate_description(product)
            product["description"] = new_desc
            updated += 1
    
    print(f"\nUpdated {updated} descriptions")
    
    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved to {OUTPUT_FILE}")
    
    # Show samples
    print("\n" + "=" * 60)
    print("SAMPLE DESCRIPTIONS")
    print("=" * 60)
    
    # Show a variety of brands
    shown_brands = set()
    for product in products:
        brand = product.get("brand", "")
        if brand not in shown_brands and len(product.get("description", "")) >= MIN_LENGTH:
            print(f"\n[{brand}] {product.get('name', '')[:40]}")
            print(f"  {product.get('description', '')}")
            shown_brands.add(brand)
            if len(shown_brands) >= 5:
                break

if __name__ == "__main__":
    main()
