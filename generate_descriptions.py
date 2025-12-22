#!/usr/bin/env python3
"""
Generate product descriptions locally by parsing product names
No API calls - uses rules and templates
"""

import json
import re
import random
import sys
from pathlib import Path

# Load products
with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json') as f:
    data = json.load(f)

# ============ EXTRACTION PATTERNS ============

def extract_dimensions(name):
    """Extract dimensions from product name - return as readable string"""
    parts = []
    
    # Diameter
    match = re.search(r'(?:Dia\.?|Ø|O)\s*(\d+[,.]?\d*)\s*(?:cm)?', name, re.IGNORECASE)
    if match:
        val = match.group(1).replace(',', '.')
        parts.append(f"{val}cm diameter")
    
    # Height
    match = re.search(r'[Hh]\.?\s*(\d+[,.]?\d*)\s*(?:cm)?', name)
    if match:
        val = match.group(1).replace(',', '.')
        if f"{val}cm" not in ' '.join(parts):  # Avoid duplicates
            parts.append(f"{val}cm tall")
    
    # Length
    match = re.search(r'[Ll]\.?\s*(\d+[,.]?\d*)\s*(?:cm)?', name)
    if match:
        val = match.group(1).replace(',', '.')
        parts.append(f"{val}cm long")
    
    # Width x Height format
    match = re.search(r'(\d+[,.]?\d*)\s*x\s*(\d+[,.]?\d*)\s*cm', name, re.IGNORECASE)
    if match and not parts:
        w = match.group(1).replace(',', '.')
        h = match.group(2).replace(',', '.')
        parts.append(f"{w}x{h}cm")
    
    if parts:
        return ', '.join(parts[:2])
    return None

def extract_material(name):
    """Extract material from product name"""
    materials = {
        'porcelain': ['porcelain', 'porzellan'],
        'ceramic': ['ceramic', 'keramik'],
        'glass': ['glass', 'glas', 'glasbecher'],
        'wood': ['wood', 'holz', 'wooden', 'bamboo', 'bambus'],
        'metal': ['metal', 'metall', 'iron', 'steel', 'brass'],
        'cotton': ['cotton', 'baumwoll'],
        'linen': ['linen', 'leinen'],
        'concrete': ['concrete', 'beton'],
        'stone': ['stone', 'stein'],
        'paper': ['paper', 'papier'],
        'felt': ['felt', 'filz'],
        'soy wax': ['soy', 'soja'],
    }
    
    name_lower = name.lower()
    for material, keywords in materials.items():
        for kw in keywords:
            if kw in name_lower:
                return material
    return None

def extract_colour(name):
    """Extract colour from product name"""
    colours = {
        'white': ['white', 'weiß', 'weiss'],
        'black': ['black', 'schwarz'],
        'gold': ['gold'],
        'silver': ['silver', 'silber'],
        'grey': ['grey', 'gray', 'grau'],
        'cream': ['cream', 'creme'],
        'red': ['red', 'rot'],
        'blue': ['blue', 'blau'],
        'green': ['green', 'grün'],
        'yellow': ['yellow', 'gelb'],
        'orange': ['orange'],
        'pink': ['pink', 'rosa'],
        'purple': ['purple', 'lila', 'violet'],
        'rose': ['rose', 'rosé'],
        'mint': ['mint'],
        'turquoise': ['turquoise', 'türkis'],
        'navy': ['navy'],
        'beige': ['beige'],
        'brown': ['brown', 'braun'],
        'copper': ['copper', 'kupfer'],
        'natural': ['natural', 'natur'],
    }
    
    name_lower = name.lower()
    for colour, keywords in colours.items():
        for kw in keywords:
            if kw in name_lower:
                return colour
    return None

def extract_quantity(name):
    """Extract set quantity"""
    patterns = [
        r'set of (\d+)',
        r'(\d+)er[- ]?set',
        r'(\d+)[- ]?piece',
        r'(\d+)[- ]?pack',
        r'set (\d+)',
        r'(\d+)er set',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def identify_product_type(name, categories):
    """Identify the type of product"""
    name_lower = name.lower()
    
    # Product type mappings - order matters (more specific first)
    types = [
        ('keychain', ['keychain', 'key chain', 'key ring', 'schlüssel']),
        ('light house', ['lichthaus', 'light house', 'lichthäuser', 'house light']),
        ('tealight holder', ['teelicht', 'tealight', 'tea light', 'tea-light', 'poesielicht']),
        ('candle', ['kerze', 'candle', 'stumpenkerze', 'duftkerze']),
        ('vase', ['vase', 'vasen', 'blümchenvase']),
        ('bowl', ['schale', 'bowl', 'schälchen']),
        ('plate', ['teller', 'plate']),
        ('mug', ['tasse', 'mug', 'becher', 'cup']),
        ('figurine', ['figur', 'figurine', 'figure']),
        ('ornament', ['ornament', 'anhänger', 'hänger', 'baumschmuck']),
        ('lantern', ['laterne', 'lantern']),
        ('lamp', ['lampe', 'lamp', 'leuchte']),
        ('necklace', ['kette', 'necklace', 'chain', 'halskette']),
        ('soundbox', ['box', 'zwitscherbox', 'lakesidebox', 'birdybox', 'seabird']),
        ('advent calendar', ['adventskalender', 'advent calendar', 'advent']),
        ('cushion', ['kissen', 'cushion', 'pillow']),
        ('throw', ['decke', 'throw', 'blanket']),
        ('cutting board', ['brett', 'board', 'brettchen', 'servierbrett']),
        ('egg cup', ['eierbecher', 'egg cup']),
        ('napkin holder', ['serviettenhalter', 'napkin holder']),
        ('puzzle', ['puzzle']),
        ('game', ['spiel', 'game', 'memory', 'kubus', 'eckolo']),
        ('socks', ['socken', 'socks']),
        ('bag', ['tasche', 'bag', 'beutel']),
    ]
    
    for product_type, keywords in types:
        for kw in keywords:
            if kw in name_lower:
                return product_type
    
    # Fall back to category
    if categories:
        cat = categories[0].lower() if categories[0] else ''
        if 'candle' in cat:
            return 'candle'
        if 'light' in cat:
            return 'light'
        if 'table' in cat:
            return 'tableware item'
        if 'gift' in cat:
            return 'gift'
        if 'décor' in cat or 'decor' in cat:
            return 'decorative piece'
    
    return 'piece'

# ============ BRAND TEMPLATES ============

BRAND_TEMPLATES = {
    'Räder': {
        'intro': [
            "A beautifully crafted {product_type} from Räder's German design studio.",
            "From Räder's collection of poetic homeware, this {product_type} brings warmth to any space.",
            "This {product_type} showcases Räder's signature blend of minimalist design and warmth.",
            "Handcrafted with care, this Räder {product_type} embodies understated elegance.",
        ],
        'features': [
            "Perfect for creating atmospheric moments at home.",
            "A timeless addition that complements both modern and traditional interiors.",
            "Designed to bring a touch of Scandinavian-inspired simplicity to your home.",
            "Makes a thoughtful gift for design lovers.",
        ],
        'origin': "Designed in Germany.",
    },
    'Remember': {
        'intro': [
            "A bold and colourful {product_type} from Remember.",
            "This vibrant {product_type} showcases Remember's signature playful style.",
            "Add a pop of colour to your home with this eye-catching {product_type}.",
            "From Germany's most colourful design house, this {product_type} celebrates the joy of colour.",
        ],
        'features': [
            "Perfect for those who believe life is too short for beige.",
            "A conversation starter that brightens any room.",
            "Quality German craftsmanship meets bold, contemporary design.",
            "Makes an unforgettable gift.",
        ],
        'origin': "Designed in Germany.",
    },
    'My Flame': {
        'intro': [
            "A hand-poured soy candle with a hidden message inside.",
            "This thoughtfully crafted candle reveals a special surprise as it burns.",
            "More than just a candle — a meaningful gift with a hidden message.",
            "Hand-poured in the Netherlands using natural soy wax.",
        ],
        'features': [
            "Burns cleanly for up to 40 hours.",
            "Made with natural soy wax and a cotton wick for a clean burn.",
            "The hidden message is revealed as the candle burns down.",
            "Beautifully packaged and ready to gift.",
        ],
        'origin': "Hand-poured in the Netherlands.",
    },
    'My Flame Keychain': {
        'intro': [
            "A charming keychain with an inspiring message.",
            "Carry a little positivity with you every day.",
            "A stylish keychain with a meaningful sentiment.",
            "The perfect small gift with a big message.",
        ],
        'features': [
            "Lightweight and durable.",
            "Features an inspiring word or message.",
            "A thoughtful token gift for friends and loved ones.",
            "Part of My Flame's collection of meaningful gifts.",
        ],
        'origin': "From the Netherlands.",
    },
    'Relaxound': {
        'intro': [
            "Bring the sounds of nature indoors with this {product_type} from Relaxound.",
            "The original motion-activated {product_type} that brings nature into your home.",
            "Transform any space into a calming retreat with this {product_type}.",
            "Award-winning German design that delivers a moment of calm whenever you need it.",
        ],
        'features': [
            "Motion-activated — simply wave your hand to start the sounds.",
            "Plays authentic nature sounds for a relaxing 2-minute escape.",
            "Battery-powered and completely portable.",
            "Perfect for the office, bedroom, bathroom, or anywhere you need a moment of peace.",
        ],
        'origin': "Designed in Germany.",
    },
    'Ideas4Seasons': {
        'intro': [
            "A charming {product_type} to celebrate the seasons.",
            "Bring seasonal style to your home with this decorative {product_type}.",
            "This {product_type} captures the spirit of the season beautifully.",
            "On-trend seasonal décor from Ideas4Seasons.",
        ],
        'features': [
            "Perfect for seasonal displays and tablescapes.",
            "Coordinates beautifully with other seasonal decorations.",
            "A lovely way to mark the changing seasons.",
            "Great for creating a warm, festive atmosphere.",
        ],
        'origin': "Made in Europe.",
    },
}

DEFAULT_TEMPLATE = {
    'intro': [
        "A stylish {product_type} for your home.",
        "This {product_type} adds character to any room.",
        "A quality {product_type} designed with care.",
    ],
    'features': [
        "A lovely addition to your home.",
        "Perfect for everyday use or special occasions.",
        "Makes a thoughtful gift.",
    ],
    'origin': "",
}

def generate_description(product):
    """Generate a description for a product"""
    name = product['name']
    brand = product.get('brand', '')
    categories = product.get('categories', [product.get('category', '')])
    
    # Extract details
    dimensions = extract_dimensions(name)
    material = extract_material(name)
    colour = extract_colour(name)
    quantity = extract_quantity(name)
    product_type = identify_product_type(name, categories)
    
    # Special handling for My Flame keychains
    template_key = brand
    if brand == 'My Flame' and product_type == 'keychain':
        template_key = 'My Flame Keychain'
    
    # Get brand template
    template = BRAND_TEMPLATES.get(template_key, DEFAULT_TEMPLATE)
    
    # Build description parts
    parts = []
    
    # Intro
    intro = random.choice(template['intro']).format(product_type=product_type)
    parts.append(intro)
    
    # Details sentence - only if we have meaningful details
    details = []
    if material:
        details.append(f"crafted from {material}")
    if quantity and quantity > 1:
        details.append(f"available as a set of {quantity}")
    if dimensions:
        details.append(f"measuring {dimensions}")
    if colour and product_type not in ['candle', 'keychain']:  # Don't repeat colour for these
        details.append(f"in a lovely {colour} finish")
    
    if details:
        detail_sentence = details[0].capitalize()
        if len(details) > 1:
            detail_sentence += ", " + ", ".join(details[1:])
        detail_sentence += "."
        parts.append(detail_sentence)
    
    # Feature
    feature = random.choice(template['features'])
    parts.append(feature)
    
    # Origin
    if template.get('origin'):
        parts.append(template['origin'])
    
    return " ".join(parts)


# ============ MAIN ============

apply_mode = '--apply' in sys.argv

if not apply_mode:
    # Generate samples first
    print("=" * 70)
    print("SAMPLE DESCRIPTIONS (20 products)")
    print("=" * 70)
    
    # Get diverse sample
    samples = []
    brands_seen = {}
    for p in data['products']:
        brand = p.get('brand', 'Unknown')
        if brand not in brands_seen:
            brands_seen[brand] = 0
        if brands_seen[brand] < 4:
            samples.append(p)
            brands_seen[brand] += 1
        if len(samples) >= 20:
            break
    
    for p in samples:
        old_desc = p.get('description', '')[:80]
        new_desc = generate_description(p)
        
        print(f"\n{p.get('brand', '?')} | {p['sku']}: {p['name'][:50]}")
        print(f"  OLD: {old_desc}...")
        print(f"  NEW: {new_desc}")
    
    print("\n" + "=" * 70)
    print("Review the above. Run with --apply to update all products.")
    print("=" * 70)

else:
    # Apply to all products
    print("Generating descriptions for all products...")
    
    updated = 0
    for p in data['products']:
        p['description'] = generate_description(p)
        updated += 1
        if updated % 500 == 0:
            print(f"  {updated} products updated...")
    
    # Save
    with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nDone! Updated {updated} product descriptions.")
    print("Saved to products.json")
