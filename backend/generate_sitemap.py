"""
Home & Verse - SEO Sitemap Generator
=====================================
Generates a comprehensive sitemap.xml including all products, categories, and brands.

Usage:
    cd /Users/matt/Desktop/home-and-verse/backend
    python3 generate_sitemap.py
"""

import json
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

# Paths
DATA_DIR = Path("data")
STATIC_DIR = Path("static")
PRODUCTS_FILE = DATA_DIR / "products.json"
SITEMAP_FILE = STATIC_DIR / "sitemap.xml"

# Base URL
BASE_URL = "https://www.homeandverse.co.uk"

# Categories with URL slugs
CATEGORIES = [
    {"name": "Christmas", "slug": "christmas", "priority": "0.9"},
    {"name": "Candles & Fragrance", "slug": "candles-fragrance", "priority": "0.8"},
    {"name": "Lighting", "slug": "lighting", "priority": "0.8"},
    {"name": "Tableware", "slug": "tableware", "priority": "0.8"},
    {"name": "Home Décor", "slug": "home-decor", "priority": "0.8"},
    {"name": "Gifts", "slug": "gifts", "priority": "0.8"},
    {"name": "Throws & Blankets", "slug": "throws-blankets", "priority": "0.8"},
    {"name": "Cushions & Pillows", "slug": "cushions-pillows", "priority": "0.8"},
    {"name": "Fashion Accessories", "slug": "fashion-accessories", "priority": "0.7"},
    {"name": "Rugs & Mats", "slug": "rugs-mats", "priority": "0.7"},
    {"name": "Bathroom", "slug": "bathroom", "priority": "0.7"},
    {"name": "Bedroom", "slug": "bedroom", "priority": "0.7"},
]

# Brands with URL slugs
BRANDS = [
    {"name": "Räder", "slug": "rader", "priority": "0.7"},
    {"name": "Remember", "slug": "remember", "priority": "0.7"},
    {"name": "My Flame", "slug": "my-flame", "priority": "0.7"},
    {"name": "Relaxound", "slug": "relaxound", "priority": "0.7"},
    {"name": "Elvang", "slug": "elvang", "priority": "0.8"},
]


def slugify(text: str) -> str:
    """Convert text to URL-safe slug"""
    return text.lower().replace(" ", "-").replace("&", "and").replace("'", "").replace('"', "")


def load_products() -> list[dict]:
    """Load products from JSON file"""
    if not PRODUCTS_FILE.exists():
        print(f"Warning: {PRODUCTS_FILE} not found")
        return []
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return data.get("products", [])


def generate_sitemap():
    """Generate comprehensive sitemap.xml"""
    
    products = load_products()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Start XML
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        '',
    ]
    
    # Homepage
    xml_parts.append(f'''  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>''')
    
    # About page
    xml_parts.append(f'''  <url>
    <loc>{BASE_URL}/about</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>''')
    
    # Category pages
    for cat in CATEGORIES:
        xml_parts.append(f'''  <url>
    <loc>{BASE_URL}/category/{cat["slug"]}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{cat["priority"]}</priority>
  </url>''')
    
    # Brand pages
    for brand in BRANDS:
        xml_parts.append(f'''  <url>
    <loc>{BASE_URL}/brand/{brand["slug"]}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{brand["priority"]}</priority>
  </url>''')
    
    # Product pages - products with images (include out of stock for SEO)
    product_count = 0
    for product in products:
        if not product.get("has_image", False) and not product.get("image_url"):
            continue
            
        sku = product.get("sku", "")
        name = product.get("name", "")
        
        if not sku:
            continue
        
        # Use pre-generated slug if available, otherwise create one
        product_slug = product.get("slug") or f"{slugify(name)}-{sku.lower()}"
        product_url = f"{BASE_URL}/product/{product_slug}"
        
        # Get image URL if available
        image_url = product.get("image_url", "")
        if image_url and image_url.startswith("/"):
            image_url = f"{BASE_URL}{image_url}"
        
        # Build product entry
        product_xml = f'''  <url>
    <loc>{product_url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>'''
        
        # Add image if available
        if image_url:
            # Escape special XML characters in name
            safe_name = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            brand = product.get("brand", "")
            safe_brand = brand.replace("&", "&amp;") if brand else ""
            
            product_xml += f'''
    <image:image>
      <image:loc>{image_url}</image:loc>
      <image:title>{safe_name}</image:title>
      <image:caption>{safe_brand} {safe_name}</image:caption>
    </image:image>'''
        
        product_xml += '\n  </url>'
        xml_parts.append(product_xml)
        product_count += 1
    
    # Close XML
    xml_parts.append('')
    xml_parts.append('</urlset>')
    
    # Write sitemap
    STATIC_DIR.mkdir(exist_ok=True)
    sitemap_content = '\n'.join(xml_parts)
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"✓ Generated sitemap.xml")
    print(f"  - 1 homepage")
    print(f"  - 1 about page")
    print(f"  - {len(CATEGORIES)} category pages")
    print(f"  - {len(BRANDS)} brand pages")
    print(f"  - {product_count} product pages")
    print(f"  - Total: {1 + 1 + len(CATEGORIES) + len(BRANDS) + product_count} URLs")
    print(f"  - Saved to: {SITEMAP_FILE}")


if __name__ == "__main__":
    generate_sitemap()
