#!/usr/bin/env python3
"""
Generate Google Merchant Center product feed for Home & Verse

UPDATED: Optimised product titles for Google Shopping performance.
Brand-first format with product type, material, and keyword enrichment.
"""

import json
import csv
import re
from pathlib import Path

PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")
OUTPUT_FILE = Path("/Users/matt/Desktop/home-and-verse/public/google-products.xml")
OUTPUT_CSV = Path("/Users/matt/Desktop/home-and-verse/public/google-products.csv")

SITE_URL = "https://homeandverse.co.uk"
CDN_BASE = "https://cdn.appdmbrands.com"

# Google Product Category IDs (numeric) - these are the OFFICIAL IDs from Google's taxonomy
GOOGLE_CATEGORIES = {
    'candles': 588,
    'candle_holders': 2784,
    'diffusers': 6997,
    'home_fragrances': 592,
    'vases': 602,
    'decorative_accents': 596,
    'figurines': 35,
    'picture_frames': 599,
    'blankets_throws': 4454,
    'cushions': 5874,
    'table_linens': 672,
    'serveware': 674,
    'bowls': 6743,
    'plates': 6745,
    'mugs': 2169,
    'tableware': 673,
    'lamps': 594,
    'night_lights': 2435,
    'christmas_decorations': 596,
    'christmas_ornaments': 603,
    'easter_decorations': 6073,
    'puzzles': 2864,
    'games': 1239,
    'card_games': 1247,
    'board_games': 1246,
    'default': 596,
}

COLOR_PATTERNS = [
    r'\b(white|black|grey|gray|blue|red|green|yellow|orange|purple|pink|brown|beige|cream|gold|silver|bronze|copper|navy|teal|turquoise|coral|mint|olive|burgundy|maroon|ivory|charcoal|natural|sand|stone|taupe|rose|blush|sage|terracotta|mustard|rust|ochre|indigo|lavender|lilac|violet|magenta|cyan|aqua)\b',
    r'\b(light blue|dark blue|light grey|dark grey|light green|dark green|rose gold|antique gold|brushed gold|matte black|matte white|off white|soft pink|dusty pink|dusty rose|forest green|ocean blue|sky blue|midnight blue)\b',
]


def optimise_title(product):
    """
    Create a Google Shopping optimised title.
    Best practice: Brand + Product Type + Key Attributes (material, colour, size)
    Max 150 chars. Front-load the most important keywords.
    """
    name = product.get('name', '')
    brand = product.get('brand', '')
    categories = product.get('categories', [])
    description = product.get('description', '').lower()
    text = f"{name} {description}".lower()
    
    # Clean up the product name
    clean_name = name.strip()
    
    # Remove brand if already in name (avoid duplication)
    for b in [brand, brand.lower(), brand.upper()]:
        if clean_name.lower().startswith(b.lower()):
            clean_name = clean_name[len(b):].strip(' -\u2013|')
    # Also remove brand after pipe at end
    if '|' in clean_name:
        parts = clean_name.rsplit('|', 1)
        if parts[1].strip().lower() in [brand.lower(), '']:
            clean_name = parts[0].strip()
    
    # Detect material from name/description
    material = ''
    material_keywords = [
        ('alpaca', 'Alpaca Wool'),
        ('porcelain', 'Porcelain'),
        ('ceramic', 'Ceramic'),
        ('stoneware', 'Stoneware'),
        ('glass', 'Glass'),
        ('oak', 'Oak'),
        ('walnut', 'Walnut'),
        ('bamboo', 'Bamboo'),
        ('wooden', 'Wooden'),
        ('wood', 'Wooden'),
        ('brass', 'Brass'),
        ('iron', 'Iron'),
        ('metal', 'Metal'),
        ('cotton', 'Cotton'),
        ('linen', 'Linen'),
        ('wool', 'Wool'),
        ('silk', 'Silk'),
        ('soy wax', 'Soy Wax'),
        ('paper', 'Paper'),
    ]
    
    for keyword, mat in material_keywords:
        if keyword in text:
            material = mat
            break
    
    # Brand-specific keyword enrichments
    brand_suffix = {
        'R\u00e4der': 'German Design',
        'Remember': 'Colourful German Design',
        'My Flame': 'Natural Soy Wax',
        'Relaxound': 'Motion Sensor Nature Sounds',
        'Elvang': 'Danish Luxury',
        'Ideas4Seasons': 'European Home D\u00e9cor',
        'PPD': 'Designer Paper Products',
    }
    
    suffix = brand_suffix.get(brand, '')
    
    # Build the optimised title: Brand + [Material] + Clean Name + [- Suffix]
    parts = [brand]
    
    # Add material if it's not already mentioned in the clean name
    if material and material.lower() not in clean_name.lower():
        parts.append(material)
    
    parts.append(clean_name)
    
    title = ' '.join(p for p in parts if p)
    
    # Add brand suffix if room
    if suffix and len(title) + len(suffix) + 3 < 145:
        title = f"{title} - {suffix}"
    
    # Ensure under 150 chars
    if len(title) > 150:
        title = title[:147] + '...'
    
    return title


def extract_color(product):
    """Extract color from product name or description"""
    text = f"{product.get('name', '')} {product.get('description', '')}".lower()
    
    for pattern in reversed(COLOR_PATTERNS):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).title()
    
    brand = product.get('brand', '')
    if brand == 'R\u00e4der':
        return 'White'
    if brand == 'Elvang':
        return 'Natural'
    if 'candle' in text or brand == 'My Flame':
        return 'White'
    
    return 'Multicolour'


def get_google_product_category(product):
    """Map product to Google Product Category numeric ID."""
    name = product.get('name', '').lower()
    description = product.get('description', '').lower()
    categories = product.get('categories', [])
    brand = product.get('brand', '')
    text = f"{name} {description}"
    
    if 'candle' in text or brand == 'My Flame':
        if 'holder' in text or 'lantern' in text:
            return GOOGLE_CATEGORIES['candle_holders']
        return GOOGLE_CATEGORIES['candles']
    
    if 'diffuser' in text:
        return GOOGLE_CATEGORIES['diffusers']
    
    if brand == 'Relaxound' or 'sound' in text or 'birdsong' in text:
        return GOOGLE_CATEGORIES['decorative_accents']
    
    if brand == 'Elvang' or any(x in text for x in ['throw', 'blanket']):
        return GOOGLE_CATEGORIES['blankets_throws']
    
    if any(x in text for x in ['cushion', 'pillow']):
        return GOOGLE_CATEGORIES['cushions']
    
    if any(x in text for x in ['vase', 'porcelain vase', 'flower vase']):
        return GOOGLE_CATEGORIES['vases']
    
    if 'bowl' in text:
        return GOOGLE_CATEGORIES['bowls']
    
    if any(x in text for x in ['plate', 'dish']):
        return GOOGLE_CATEGORIES['plates']
    
    if any(x in text for x in ['cup', 'mug']):
        return GOOGLE_CATEGORIES['mugs']
    
    if any(x in text for x in ['figurine', 'figure', 'statue', 'sculpture']):
        return GOOGLE_CATEGORIES['figurines']
    
    if 'Christmas' in categories or any(x in text for x in ['christmas', 'advent', 'santa', 'xmas']):
        if 'ornament' in text or 'bauble' in text or 'hanging' in text:
            return GOOGLE_CATEGORIES['christmas_ornaments']
        return GOOGLE_CATEGORIES['christmas_decorations']
    
    if 'Easter' in categories or 'easter' in text:
        return GOOGLE_CATEGORIES['easter_decorations']
    
    if 'puzzle' in text:
        return GOOGLE_CATEGORIES['puzzles']
    
    if 'game' in text or 'memo' in text:
        if 'card' in text:
            return GOOGLE_CATEGORIES['card_games']
        if 'board' in text:
            return GOOGLE_CATEGORIES['board_games']
        return GOOGLE_CATEGORIES['games']
    
    if any(x in text for x in ['lamp', 'light', 'lantern', 'tealight']):
        if 'night' in text:
            return GOOGLE_CATEGORIES['night_lights']
        return GOOGLE_CATEGORIES['lamps']
    
    if any(x in text for x in ['napkin', 'tablecloth', 'placemat', 'coaster', 'runner']):
        return GOOGLE_CATEGORIES['table_linens']
    
    return GOOGLE_CATEGORIES['default']


def get_image_url(product):
    """Get the correct image URL for a product from self-hosted CDN"""
    sku = product.get('sku', '')
    brand = product.get('brand', '')
    
    if brand == 'Elvang':
        return f"{CDN_BASE}/products/elvang/{sku}_1.jpg"
    if brand == 'Relaxound':
        return f"{CDN_BASE}/products/relaxound/{sku}.jpg"
    
    return f"{CDN_BASE}/products/{sku}.jpg"


def get_additional_image_urls(product, max_images=10):
    """Get additional image URLs from verified extras"""
    extras_file = Path(__file__).parent / "backend" / "data" / "verified_image_extras.json"
    if not hasattr(get_additional_image_urls, '_cache'):
        try:
            with open(extras_file, 'r') as f:
                get_additional_image_urls._cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            get_additional_image_urls._cache = {}
    
    sku = product.get('sku', '')
    brand = product.get('brand', '')
    suffixes = get_additional_image_urls._cache.get(sku, [])
    
    urls = []
    for suffix in suffixes[:max_images]:
        if brand == 'Elvang':
            urls.append(f"{CDN_BASE}/products/elvang/{suffix}.jpg")
        else:
            urls.append(f"{CDN_BASE}/products/{suffix}.jpg")
    return urls


def generate_feed():
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('products', data)
    
    in_stock = [
        p for p in products 
        if p.get('in_stock', False) 
        and p.get('stock', 0) > 0
        and p.get('has_image', False)
        and 'test' not in p.get('name', '').lower()
        and not p.get('sku', '').startswith('DMB')
    ]
    
    print(f"Total products: {len(products)}")
    print(f"In stock with images: {len(in_stock)}")
    
    category_counts = {}
    
    # Show title transformation samples
    print(f"\n\U0001f4dd Title optimisation samples:")
    for p in in_stock[:10]:
        old_title = f"{p.get('name', '')} | {p.get('brand', '')}"
        new_title = optimise_title(p)
        print(f"  OLD: {old_title}")
        print(f"  NEW: {new_title}")
        print()
    
    # Generate CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow([
            'id', 'title', 'description', 'link', 'image_link',
            'additional_image_link',
            'availability', 'price', 'brand', 'gtin', 'identifier_exists',
            'condition', 'google_product_category', 'product_type',
            'age_group', 'gender', 'color', 'shipping_weight'
        ])
        
        for p in in_stock:
            sku = p.get('sku', '')
            description = p.get('description', p.get('name', ''))
            brand = p.get('brand', '')
            price = p.get('price', 0)
            ean = p.get('ean', '')
            categories = p.get('categories', [])
            
            title = optimise_title(p)
            product_url = f"{SITE_URL}/product/{sku}"
            image_url = get_image_url(p)
            google_category_id = get_google_product_category(p)
            category_counts[google_category_id] = category_counts.get(google_category_id, 0) + 1
            category_path = ' > '.join(['Home & Garden', 'Home Decor'] + categories[:2])
            color = extract_color(p)
            identifier_exists = 'yes' if ean else 'no'
            additional_images = get_additional_image_urls(p)
            additional_image_str = ','.join(additional_images) if additional_images else ''
            
            writer.writerow([
                sku, title, description[:5000], product_url, image_url,
                additional_image_str,
                'in_stock', f"{price:.2f} GBP", brand,
                ean if ean else '', identifier_exists, 'new',
                google_category_id, category_path,
                'adult', 'unisex', color, '0.5 kg'
            ])
    
    print(f"\n\u2705 Generated: {OUTPUT_CSV}")
    print(f"   Products in feed: {len(in_stock)}")
    print(f"\n\U0001f4ca Category distribution:")
    for cat_id, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"   Category {cat_id}: {count} products")
    
    # Generate XML feed
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
        title = optimise_title(p).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        description = p.get('description', p.get('name', '')).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        brand = p.get('brand', '')
        price = p.get('price', 0)
        ean = p.get('ean', '')
        categories = p.get('categories', [])
        
        product_url = f"{SITE_URL}/product/{sku}"
        image_url = get_image_url(p)
        google_category_id = get_google_product_category(p)
        category_path = ' &gt; '.join(['Home &amp; Garden', 'Home Decor'] + [c.replace('&', '&amp;') for c in categories[:2]])
        color = extract_color(p)
        identifier_exists = 'yes' if ean else 'no'
        
        xml_lines.append('<item>')
        xml_lines.append(f'  <g:id>{sku}</g:id>')
        xml_lines.append(f'  <g:title>{title}</g:title>')
        xml_lines.append(f'  <g:description>{description[:5000]}</g:description>')
        xml_lines.append(f'  <g:link>{product_url}</g:link>')
        xml_lines.append(f'  <g:image_link>{image_url}</g:image_link>')
        for extra_url in get_additional_image_urls(p):
            xml_lines.append(f'  <g:additional_image_link>{extra_url}</g:additional_image_link>')
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
    
    # Count products with additional images
    extras_count = sum(1 for p in in_stock if get_additional_image_urls(p))
    total_extras = sum(len(get_additional_image_urls(p)) for p in in_stock)
    print(f"\u2705 Generated: {OUTPUT_FILE}")
    print(f"\n\U0001f5bc\ufe0f  Additional images: {extras_count} products with {total_extras} extra images")


if __name__ == "__main__":
    generate_feed()
