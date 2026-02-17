"""
Generate optimized Google Merchant Center product feed
Run: python generate_google_feed.py
"""

import json
import csv
import re
from pathlib import Path

# Paths
DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"
OUTPUT_CSV = Path("../public/google-products.csv")
OUTPUT_XML = Path("../public/google-products.xml")


def get_optimized_title(product):
    """Generate SEO-optimized title for Google Shopping"""
    name = product.get('name', '')
    brand = product.get('brand', '')
    
    title = re.sub(r'\s*\|\s*\w+(\s+\w+)?\s*$', '', name).strip()
    title = re.sub(rf'^{re.escape(brand)}\s+', '', title, flags=re.IGNORECASE).strip()
    title = re.sub(r'^Rader\s+', '', title, flags=re.IGNORECASE).strip()
    title = re.sub(r'^My Flame Lifestyle\s+', '', title, flags=re.IGNORECASE).strip()
    title = re.sub(r'^My Flame\s+', '', title, flags=re.IGNORECASE).strip()
    
    title_lower = title.lower()
    
    if brand == 'Relaxound':
        if 'zwitscherbox' in title_lower:
            variant = re.search(r'Zwitscherbox\s+(\w+)', title, re.IGNORECASE)
            v = variant.group(1) if variant else ''
            return f"Relaxound Zwitscherbox {v} - Birdsong Box Motion Sensor Nature Sounds".strip()
        if 'birdybox' in title_lower:
            return f"Relaxound {title} - Portable USB Birdsong Box"
        if 'lakeside' in title_lower:
            return "Relaxound Lakesidebox - Water & Nature Sounds Relaxation Box"
        if 'seaside' in title_lower:
            return "Relaxound Seasidebox - Ocean Wave Sounds Relaxation Box"
        if 'ocean' in title_lower:
            return "Relaxound Oceanbox - Sea & Seagull Sounds Relaxation Box"
        if 'jungle' in title_lower:
            return "Relaxound Junglebox - Tropical Rainforest Sounds Box"
        return f"Relaxound {title} - Nature Sound Machine"
    
    if brand == 'Räder':
        if 'light' in title_lower and 'house' in title_lower:
            return f"Räder {title} - Porcelain Tealight House"
        if 'light object' in title_lower:
            return f"Räder {title} - Porcelain Tealight Holder"
        if 'vase' in title_lower:
            return f"Räder {title} - German Porcelain Vase"
        if 'cup' in title_lower:
            return f"Räder {title} - German Porcelain Cup"
        if 'plate' in title_lower:
            return f"Räder {title} - German Porcelain Plate"
        if 'bowl' in title_lower:
            return f"Räder {title} - German Porcelain Bowl"
        if 'easter' in title_lower:
            return f"Räder {title} - German Easter Decoration"
        if any(x in title_lower for x in ['christmas', 'santa', 'advent']):
            return f"Räder {title} - German Christmas Decoration"
        return f"Räder {title} - German Porcelain Décor"
    
    if brand == 'My Flame':
        if 'soy candle' in title_lower:
            msg = re.sub(r'Scented soy candle in glass jar\s*(with \w+\s*)*', '', title, flags=re.IGNORECASE).strip()[:50]
            return f"My Flame '{msg}' Hidden Message Candle - Soy Wax Gift"
        if 'diffuser' in title_lower:
            return f"My Flame {title[:40]} - Reed Diffuser Home Fragrance"
        if 'outdoor' in title_lower:
            return f"My Flame {title[:40]} - Citronella Garden Candle"
        return f"My Flame {title[:50]} - Dutch Gift"
    
    if brand == 'Remember':
        if 'lamp' in title_lower:
            return f"Remember {title} - Colourful German Designer Lamp"
        if 'lantern' in title_lower:
            return f"Remember {title} - Colourful German Lantern"
        if 'memo' in title_lower:
            return f"Remember {title} - Memory Game Gift"
        if 'game' in title_lower:
            return f"Remember {title} - German Family Game"
        return f"Remember {title} - Colourful German Design"
    
    if brand == 'Elvang':
        if 'throw' in title_lower or 'blanket' in title_lower:
            return f"Elvang {title} - Luxury Danish Alpaca Throw"
        if 'cushion' in title_lower:
            return f"Elvang {title} - Danish Alpaca Cushion"
        if 'rug' in title_lower:
            return f"Elvang {title} - Danish Design Rug"
        if 'scarf' in title_lower:
            return f"Elvang {title} - Danish Alpaca Scarf"
        return f"Elvang {title} - Danish Design"
    
    return f"{brand} {title}"[:150]


def extract_colour(product):
    """Extract colour from product name/description"""
    text = f"{product.get('name', '')} {product.get('description', '')}".lower()
    brand = product.get('brand', '')
    
    colours = {
        'white': 'White', 'black': 'Black', 'grey': 'Grey', 'gray': 'Grey',
        'blue': 'Blue', 'navy': 'Navy Blue', 'green': 'Green', 'mint': 'Mint Green',
        'sage': 'Sage Green', 'red': 'Red', 'burgundy': 'Burgundy', 'pink': 'Pink',
        'rose': 'Rose', 'coral': 'Coral', 'yellow': 'Yellow', 'orange': 'Orange',
        'purple': 'Purple', 'brown': 'Brown', 'beige': 'Beige', 'cream': 'Cream',
        'sand': 'Sand', 'taupe': 'Taupe', 'camel': 'Camel', 'natural': 'Natural',
        'oak': 'Oak', 'walnut': 'Walnut', 'gold': 'Gold', 'silver': 'Silver',
        'multicolour': 'Multicolour', 'multi': 'Multicolour'
    }
    
    for key, value in colours.items():
        if key in text:
            return value
    
    # Default by brand
    if brand == 'Räder':
        return 'White'
    if brand == 'Elvang':
        return 'Natural'
    if brand == 'My Flame':
        return 'White'
    
    return 'Multicolour'


def extract_material(product):
    """Extract material from product"""
    text = f"{product.get('name', '')} {product.get('description', '')}".lower()
    brand = product.get('brand', '')
    
    if brand == 'Räder':
        return 'Porcelain'
    if brand == 'Elvang':
        return 'Alpaca Wool' if 'alpaca' in text else 'Wool Blend'
    if brand == 'My Flame' and 'candle' in text:
        return 'Soy Wax'
    if brand == 'Relaxound':
        if 'oak' in text:
            return 'Oak Wood'
        if 'walnut' in text:
            return 'Walnut Wood'
        if 'bamboo' in text:
            return 'Bamboo'
        return 'Wood'
    
    materials = ['porcelain', 'ceramic', 'glass', 'wood', 'cotton', 'wool', 'metal', 'paper']
    for m in materials:
        if m in text:
            return m.capitalize()
    return ''


def get_google_product_category(product):
    """Map product to appropriate Google Product Category"""
    name = product.get('name', '').lower()
    description = product.get('description', '').lower()
    categories = product.get('categories', [])
    brand = product.get('brand', '')
    text = f"{name} {description}"
    
    if 'candle' in text or brand == 'My Flame':
        return 'Home & Garden > Decor > Candles'
    if 'diffuser' in text:
        return 'Home & Garden > Decor > Home Fragrances > Fragrance Diffusers'
    if brand == 'Relaxound' or 'sound' in text or 'birdsong' in text:
        return 'Home & Garden > Decor > Decorative Accents'
    if brand == 'Elvang' or any(x in text for x in ['throw', 'blanket', 'cushion', 'pillow']):
        return 'Home & Garden > Linens & Bedding > Bedding > Blankets & Throws'
    if any(x in text for x in ['vase', 'porcelain', 'ceramic']):
        return 'Home & Garden > Decor > Vases'
    if any(x in text for x in ['bowl', 'plate', 'dish', 'cup', 'mug']):
        return 'Home & Garden > Kitchen & Dining > Tableware > Serveware'
    if 'Christmas' in categories or any(x in text for x in ['christmas', 'advent', 'santa']):
        return 'Home & Garden > Decor > Seasonal & Holiday Decorations > Christmas Decorations'
    if 'Easter' in categories or 'easter' in text:
        return 'Home & Garden > Decor > Seasonal & Holiday Decorations > Easter Decorations'
    if any(x in text for x in ['game', 'puzzle', 'memo']):
        return 'Toys & Games > Puzzles'
    if any(x in text for x in ['lamp', 'light', 'lantern', 'tealight']):
        return 'Home & Garden > Lighting > Lamps'
    return 'Home & Garden > Decor > Decorative Accents'


def estimate_weight(product):
    """Estimate shipping weight based on product type"""
    name = product.get('name', '').lower()
    brand = product.get('brand', '')
    
    if brand == 'Elvang':
        if 'throw' in name or 'blanket' in name:
            return '1.2 kg'
        if 'cushion' in name:
            return '0.4 kg'
        if 'rug' in name:
            return '1.5 kg' if '170x240' not in name else '3.0 kg'
        if 'scarf' in name:
            return '0.2 kg'
        return '0.5 kg'
    if brand == 'Relaxound':
        return '0.15 kg' if 'birdybox' in name else '0.3 kg'
    if brand == 'Räder':
        if 'light house' in name and 'large' in name:
            return '0.8 kg'
        if 'vase' in name and 'large' in name:
            return '0.8 kg'
        if 'cup' in name or 'mug' in name:
            return '0.25 kg'
        return '0.3 kg'
    if brand == 'My Flame':
        if 'outdoor' in name:
            return '0.8 kg'
        if 'tin' in name:
            return '0.15 kg'
        if 'giftbox' in name or 'spa' in name:
            return '0.6 kg'
        return '0.35 kg'
    if brand == 'Remember':
        if 'memo' in name or 'game' in name:
            return '0.8 kg'
        if 'lamp' in name:
            return '0.4 kg'
        return '0.3 kg'
    return '0.5 kg'


def get_image_url(product):
    """Get image URL - must match frontend's getImageUrl logic.
    products.json stores /images/SKU.jpg but CDN serves from /products/SKU.jpg
    The frontend translates this at runtime; we must do the same."""
    image_url = product.get('image_url', '')
    if not image_url:
        return ''
    cdn_base = 'https://cdn.appdmbrands.com'
    # Extract SKU from /images/SKU.jpg path
    if image_url.startswith('/images/'):
        filename = image_url.replace('/images/', '')
        return f"{cdn_base}/products/{filename}"
    return f"{cdn_base}{image_url}"


def generate_csv(products):
    """Generate Google Merchant CSV feed"""
    fieldnames = [
        'id', 'title', 'description', 'link', 'image_link', 'availability',
        'price', 'brand', 'gtin', 'identifier_exists', 'condition', 
        'google_product_category', 'product_type', 'age_group', 'gender',
        'color', 'material', 'shipping_weight'
    ]
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in products:
            if not product.get('in_stock', False):
                continue
            if not product.get('has_image', False):
                continue
            
            categories = product.get('categories', [])
            product_type = ' > '.join(['Home & Garden', 'Home Decor'] + categories[:2])
            ean = product.get('ean', '')
            identifier_exists = 'yes' if ean else 'no'
            
            row = {
                'id': product.get('sku', ''),
                'title': get_optimized_title(product),
                'description': product.get('description', '')[:5000],
                'link': f"https://www.homeandverse.co.uk/?product={product.get('sku', '')}",
                'image_link': get_image_url(product),
                'availability': 'in_stock',
                'price': f"{product.get('price', 0):.2f} GBP",
                'brand': product.get('brand', ''),
                'gtin': ean,
                'identifier_exists': identifier_exists,
                'condition': 'new',
                'google_product_category': get_google_product_category(product),
                'product_type': product_type,
                'age_group': 'adult',
                'gender': 'unisex',
                'color': extract_colour(product),
                'material': extract_material(product),
                'shipping_weight': estimate_weight(product)
            }
            writer.writerow(row)
    
    print(f"Generated {OUTPUT_CSV}")


def generate_xml(products):
    """Generate Google Merchant XML feed"""
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        '<channel>',
        '<title>Home and Verse Products</title>',
        '<link>https://www.homeandverse.co.uk</link>',
        '<description>Curated European homeware</description>'
    ]
    
    for product in products:
        if not product.get('in_stock', False):
            continue
        if not product.get('has_image', False):
            continue
        
        sku = product.get('sku', '')
        categories = product.get('categories', [])
        product_type = ' > '.join(['Home & Garden', 'Home Decor'] + categories[:2])
        ean = product.get('ean', '')
        identifier_exists = 'yes' if ean else 'no'
        
        xml_lines.append('<item>')
        xml_lines.append(f"<g:id>{sku}</g:id>")
        xml_lines.append(f"<g:title><![CDATA[{get_optimized_title(product)}]]></g:title>")
        xml_lines.append(f"<g:description><![CDATA[{product.get('description', '')[:5000]}]]></g:description>")
        xml_lines.append(f"<g:link>https://www.homeandverse.co.uk/?product={sku}</g:link>")
        xml_lines.append(f"<g:image_link>{get_image_url(product)}</g:image_link>")
        xml_lines.append("<g:availability>in_stock</g:availability>")
        xml_lines.append(f"<g:price>{product.get('price', 0):.2f} GBP</g:price>")
        xml_lines.append(f"<g:brand>{product.get('brand', '')}</g:brand>")
        if ean:
            xml_lines.append(f"<g:gtin>{ean}</g:gtin>")
        xml_lines.append(f"<g:identifier_exists>{identifier_exists}</g:identifier_exists>")
        xml_lines.append("<g:condition>new</g:condition>")
        xml_lines.append(f"<g:google_product_category><![CDATA[{get_google_product_category(product)}]]></g:google_product_category>")
        xml_lines.append(f"<g:product_type><![CDATA[{product_type}]]></g:product_type>")
        xml_lines.append("<g:age_group>adult</g:age_group>")
        xml_lines.append("<g:gender>unisex</g:gender>")
        xml_lines.append(f"<g:color>{extract_colour(product)}</g:color>")
        material = extract_material(product)
        if material:
            xml_lines.append(f"<g:material>{material}</g:material>")
        xml_lines.append(f"<g:shipping_weight>{estimate_weight(product)}</g:shipping_weight>")
        xml_lines.append('</item>')
    
    xml_lines.append('</channel>')
    xml_lines.append('</rss>')
    
    with open(OUTPUT_XML, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"Generated {OUTPUT_XML}")


def main():
    print("=" * 50)
    print("GOOGLE MERCHANT FEED GENERATOR")
    print("=" * 50)
    
    if not PRODUCTS_FILE.exists():
        print(f"ERROR: {PRODUCTS_FILE} not found!")
        return
    
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    products = data.get('products', [])
    in_stock = [p for p in products if p.get('in_stock', False)]
    
    print(f"\nTotal products: {len(products)}")
    print(f"In stock: {len(in_stock)}")
    
    generate_csv(in_stock)
    generate_xml(in_stock)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
