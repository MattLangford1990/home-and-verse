#!/usr/bin/env python3
"""
Generate Google Merchant Center product feed for Home & Verse

UPDATED: Using numeric Google Product Category IDs to fix 
"Invalid product category" errors in Merchant Center.
"""

import json
import csv
import re
from pathlib import Path

PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")
OUTPUT_FILE = Path("/Users/matt/Desktop/home-and-verse/public/google-products.xml")
OUTPUT_CSV = Path("/Users/matt/Desktop/home-and-verse/public/google-products.csv")

SITE_URL = "https://www.homeandverse.co.uk"
CDN_BASE = "https://cdn.appdmbrands.com"

# Google Product Category IDs (numeric) - these are the OFFICIAL IDs from Google's taxonomy
# Using numeric IDs avoids any text formatting issues
GOOGLE_CATEGORIES = {
    # Home Fragrances
    'candles': 588,                    # Home & Garden > Decor > Home Fragrances > Candles
    'candle_holders': 2784,            # Home & Garden > Decor > Home Fragrance Accessories > Candle Holders
    'diffusers': 6997,                 # Home & Garden > Decor > Home Fragrances > Fragrance Diffusers
    'home_fragrances': 592,            # Home & Garden > Decor > Home Fragrances
    
    # Decor
    'vases': 602,                      # Home & Garden > Decor > Vases
    'decorative_accents': 596,         # Home & Garden > Decor > Decorative Accents
    'figurines': 35,                   # Home & Garden > Decor > Figurines
    'picture_frames': 599,             # Home & Garden > Decor > Picture Frames
    
    # Textiles / Linens
    'blankets_throws': 4454,           # Home & Garden > Linens & Bedding > Bedding > Blankets & Throws
    'cushions': 5874,                  # Home & Garden > Linens & Bedding > Bedding > Pillows
    'table_linens': 672,               # Home & Garden > Kitchen & Dining > Table Linens
    
    # Kitchen & Dining
    'serveware': 674,                  # Home & Garden > Kitchen & Dining > Tableware > Serveware
    'bowls': 6743,                     # Home & Garden > Kitchen & Dining > Tableware > Serveware > Serving Bowls
    'plates': 6745,                    # Home & Garden > Kitchen & Dining > Tableware > Dinnerware > Plates
    'mugs': 2169,                      # Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs
    'tableware': 673,                  # Home & Garden > Kitchen & Dining > Tableware
    
    # Lighting
    'lamps': 594,                      # Home & Garden > Lighting > Lamps
    'night_lights': 2435,              # Home & Garden > Lighting > Night Lights
    
    # Seasonal
    'christmas_decorations': 596,      # Home & Garden > Decor > Seasonal & Holiday Decorations > Christmas Decorations
    'christmas_ornaments': 603,        # Home & Garden > Decor > Seasonal & Holiday Decorations > Holiday Ornaments
    'easter_decorations': 6073,        # Home & Garden > Decor > Seasonal & Holiday Decorations > Easter Decorations
    
    # Toys & Games
    'puzzles': 2864,                   # Toys & Games > Puzzles
    'games': 1239,                     # Toys & Games > Games
    'card_games': 1247,                # Toys & Games > Games > Card Games
    'board_games': 1246,               # Toys & Games > Games > Board Games
    
    # Default fallback
    'default': 596,                    # Home & Garden > Decor > Decorative Accents
}

# Color extraction patterns
COLOR_PATTERNS = [
    # Common colors
    r'\b(white|black|grey|gray|blue|red|green|yellow|orange|purple|pink|brown|beige|cream|gold|silver|bronze|copper|navy|teal|turquoise|coral|mint|olive|burgundy|maroon|ivory|charcoal|natural|sand|stone|taupe|rose|blush|sage|terracotta|mustard|rust|ochre|indigo|lavender|lilac|violet|magenta|cyan|aqua)\b',
    # Multi-word colors
    r'\b(light blue|dark blue|light grey|dark grey|light green|dark green|rose gold|antique gold|brushed gold|matte black|matte white|off white|soft pink|dusty pink|dusty rose|forest green|ocean blue|sky blue|midnight blue)\b',
]

def extract_color(product):
    """Extract color from product name or description"""
    text = f"{product.get('name', '')} {product.get('description', '')}".lower()
    
    # Try multi-word patterns first
    for pattern in reversed(COLOR_PATTERNS):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).title()
    
    # Default based on brand/category
    brand = product.get('brand', '')
    categories = product.get('categories', [])
    
    if brand == 'Räder':
        return 'White'  # Most Räder is white porcelain
    if brand == 'Elvang':
        return 'Natural'  # Textiles
    if 'candle' in text or brand == 'My Flame':
        return 'White'
    
    return 'Multicolour'  # Safe default for homeware

def get_google_product_category(product):
    """
    Map product to appropriate Google Product Category ID.
    Returns numeric ID for reliability.
    """
    name = product.get('name', '').lower()
    description = product.get('description', '').lower()
    categories = product.get('categories', [])
    brand = product.get('brand', '')
    text = f"{name} {description}"
    
    # Candles - ID 588
    if 'candle' in text or brand == 'My Flame':
        if 'holder' in text or 'lantern' in text:
            return GOOGLE_CATEGORIES['candle_holders']
        return GOOGLE_CATEGORIES['candles']
    
    # Diffusers - ID 6997
    if 'diffuser' in text:
        return GOOGLE_CATEGORIES['diffusers']
    
    # Sound boxes (Relaxound) - Decorative Accents
    if brand == 'Relaxound' or 'sound' in text or 'birdsong' in text:
        return GOOGLE_CATEGORIES['decorative_accents']
    
    # Textiles (Elvang)
    if brand == 'Elvang' or any(x in text for x in ['throw', 'blanket']):
        return GOOGLE_CATEGORIES['blankets_throws']
    
    if any(x in text for x in ['cushion', 'pillow']):
        return GOOGLE_CATEGORIES['cushions']
    
    # Porcelain/ceramics - Vases
    if any(x in text for x in ['vase', 'porcelain vase', 'flower vase']):
        return GOOGLE_CATEGORIES['vases']
    
    # Tableware
    if 'bowl' in text:
        return GOOGLE_CATEGORIES['bowls']
    
    if any(x in text for x in ['plate', 'dish']):
        return GOOGLE_CATEGORIES['plates']
    
    if any(x in text for x in ['cup', 'mug']):
        return GOOGLE_CATEGORIES['mugs']
    
    # Figurines
    if any(x in text for x in ['figurine', 'figure', 'statue', 'sculpture']):
        return GOOGLE_CATEGORIES['figurines']
    
    # Christmas - ID 596 (or 603 for ornaments)
    if 'Christmas' in categories or any(x in text for x in ['christmas', 'advent', 'santa', 'xmas']):
        if 'ornament' in text or 'bauble' in text or 'hanging' in text:
            return GOOGLE_CATEGORIES['christmas_ornaments']
        return GOOGLE_CATEGORIES['christmas_decorations']
    
    # Easter - ID 6073
    if 'Easter' in categories or 'easter' in text:
        return GOOGLE_CATEGORIES['easter_decorations']
    
    # Games/puzzles
    if 'puzzle' in text:
        return GOOGLE_CATEGORIES['puzzles']
    
    if 'game' in text or 'memo' in text:
        if 'card' in text:
            return GOOGLE_CATEGORIES['card_games']
        if 'board' in text:
            return GOOGLE_CATEGORIES['board_games']
        return GOOGLE_CATEGORIES['games']
    
    # Lamps/lighting
    if any(x in text for x in ['lamp', 'light', 'lantern', 'tealight']):
        if 'night' in text:
            return GOOGLE_CATEGORIES['night_lights']
        return GOOGLE_CATEGORIES['lamps']
    
    # Table linens
    if any(x in text for x in ['napkin', 'tablecloth', 'placemat', 'coaster', 'runner']):
        return GOOGLE_CATEGORIES['table_linens']
    
    # Default - Decorative Accents (ID 596)
    return GOOGLE_CATEGORIES['default']

def get_image_url(product):
    """Get the correct image URL for a product from self-hosted CDN"""
    sku = product.get('sku', '')
    brand = product.get('brand', '')
    image_path = product.get('image_url', '')
    
    # Handle different brands
    if brand == 'Elvang':
        return f"{CDN_BASE}/products/elvang/{sku}_1.jpg"
    
    if brand == 'Relaxound':
        return f"{CDN_BASE}/products/relaxound/{sku}.jpg"
    
    # Standard products folder
    return f"{CDN_BASE}/products/{sku}.jpg"

def generate_feed():
    # Load products
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('products', data)
    
    # Filter to in-stock items with images only, excluding test products
    in_stock = [
        p for p in products 
        if p.get('in_stock', False) 
        and p.get('stock', 0) > 0
        and p.get('has_image', False)
        and 'test' not in p.get('name', '').lower()
        and not p.get('sku', '').startswith('DMB')  # Internal test SKUs
    ]
    
    print(f"Total products: {len(products)}")
    print(f"In stock with images: {len(in_stock)}")
    
    # Track category distribution for debugging
    category_counts = {}
    
    # Generate CSV (easier to upload to Merchant Center)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header row - Google Merchant Center required fields
        writer.writerow([
            'id',
            'title',
            'description',
            'link',
            'image_link',
            'availability',
            'price',
            'brand',
            'gtin',
            'identifier_exists',
            'condition',
            'google_product_category',
            'product_type',
            'age_group',
            'gender',
            'color',
            'shipping_weight'
        ])
        
        for p in in_stock:
            sku = p.get('sku', '')
            name = p.get('name', '')
            description = p.get('description', name)
            brand = p.get('brand', '')
            price = p.get('price', 0)
            ean = p.get('ean', '')
            categories = p.get('categories', [])
            
            # Product URL - using SKU parameter
            product_url = f"{SITE_URL}/?product={sku}"
            
            # Image URL from self-hosted CDN
            image_url = get_image_url(p)
            
            # Google product category (NUMERIC ID)
            google_category_id = get_google_product_category(p)
            
            # Track for debugging
            category_counts[google_category_id] = category_counts.get(google_category_id, 0) + 1
            
            # Custom product type path (this can be your own hierarchy)
            category_path = ' > '.join(['Home & Garden', 'Home Decor'] + categories[:2])
            
            # Extract color from product
            color = extract_color(p)
            
            # Identifier exists - false if no EAN
            identifier_exists = 'yes' if ean else 'no'
            
            writer.writerow([
                sku,                                    # id
                f"{name} | {brand}",                   # title (brand in title helps)
                description[:5000],                     # description (max 5000 chars)
                product_url,                            # link
                image_url,                              # image_link
                'in_stock',                             # availability
                f"{price:.2f} GBP",                     # price
                brand,                                  # brand
                ean if ean else '',                     # gtin (EAN)
                identifier_exists,                      # identifier_exists
                'new',                                  # condition
                google_category_id,                     # google_product_category (NUMERIC ID)
                category_path,                          # product_type (your own categorization)
                'adult',                                # age_group (required for some categories)
                'unisex',                               # gender (required for some categories)
                color,                                  # color
                '0.5 kg'                                # shipping_weight (estimate)
            ])
    
    print(f"\n✅ Generated: {OUTPUT_CSV}")
    print(f"   Products in feed: {len(in_stock)}")
    print(f"\n📊 Category distribution:")
    for cat_id, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"   Category {cat_id}: {count} products")
    
    # Also generate XML feed (RSS 2.0 format with Google namespace)
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        '<channel>',
        '<title>Home &amp; Verse Products</title>',
        f'<link>{SITE_URL}</link>',
        '<description>Luxury European homeware from Home &amp; Verse</description>',
    ]
    
    for p in in_stock:
        sku = p.get('sku', '')
        name = p.get('name', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        description = p.get('description', name).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        brand = p.get('brand', '')
        price = p.get('price', 0)
        ean = p.get('ean', '')
        categories = p.get('categories', [])
        
        product_url = f"{SITE_URL}/?product={sku}"
        image_url = get_image_url(p)
        google_category_id = get_google_product_category(p)
        category_path = ' &gt; '.join(['Home &amp; Garden', 'Home Decor'] + [c.replace('&', '&amp;') for c in categories[:2]])
        color = extract_color(p)
        identifier_exists = 'yes' if ean else 'no'
        
        xml_lines.append('<item>')
        xml_lines.append(f'  <g:id>{sku}</g:id>')
        xml_lines.append(f'  <g:title>{name} | {brand}</g:title>')
        xml_lines.append(f'  <g:description>{description[:5000]}</g:description>')
        xml_lines.append(f'  <g:link>{product_url}</g:link>')
        xml_lines.append(f'  <g:image_link>{image_url}</g:image_link>')
        xml_lines.append(f'  <g:availability>in_stock</g:availability>')
        xml_lines.append(f'  <g:price>{price:.2f} GBP</g:price>')
        xml_lines.append(f'  <g:brand>{brand}</g:brand>')
        if ean:
            xml_lines.append(f'  <g:gtin>{ean}</g:gtin>')
        xml_lines.append(f'  <g:identifier_exists>{identifier_exists}</g:identifier_exists>')
        xml_lines.append(f'  <g:condition>new</g:condition>')
        xml_lines.append(f'  <g:google_product_category>{google_category_id}</g:google_product_category>')
        xml_lines.append(f'  <g:product_type>{category_path}</g:product_type>')
        xml_lines.append(f'  <g:age_group>adult</g:age_group>')
        xml_lines.append(f'  <g:gender>unisex</g:gender>')
        xml_lines.append(f'  <g:color>{color}</g:color>')
        xml_lines.append('</item>')
    
    xml_lines.append('</channel>')
    xml_lines.append('</rss>')
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"✅ Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_feed()
