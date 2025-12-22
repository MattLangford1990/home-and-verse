#!/usr/bin/env python3
"""
Generate XML sitemap for Home & Verse
Run this whenever products change: python3 generate_sitemap.py
"""

import json
from datetime import datetime
from urllib.parse import quote

BASE_URL = "https://www.homeandverse.co.uk"

# Categories and brands to include
CATEGORIES = [
    "Christmas",
    "Candles & Fragrance", 
    "Lighting",
    "Tableware",
    "Home Décor",
    "Gifts"
]

BRANDS = [
    "Räder",
    "Remember", 
    "My Flame",
    "Relaxound",
    "Ideas4Seasons"
]

def generate_sitemap():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load products
    with open('backend/data/products.json', 'r') as f:
        data = json.load(f)
        products = data if isinstance(data, list) else data.get('products', [])
    
    # Filter to in-stock products only
    in_stock_products = [p for p in products if p.get('in_stock', False) or p.get('stock', 0) > 0]
    
    print(f"Found {len(in_stock_products)} in-stock products")
    
    urls = []
    
    # Homepage - highest priority
    urls.append({
        'loc': BASE_URL,
        'lastmod': today,
        'changefreq': 'daily',
        'priority': '1.0'
    })
    
    # Category pages
    for cat in CATEGORIES:
        urls.append({
            'loc': f"{BASE_URL}/?category={quote(cat)}",
            'lastmod': today,
            'changefreq': 'daily',
            'priority': '0.9'
        })
    
    # Brand pages
    for brand in BRANDS:
        urls.append({
            'loc': f"{BASE_URL}/?brand={quote(brand)}",
            'lastmod': today,
            'changefreq': 'weekly',
            'priority': '0.8'
        })
    
    # Static pages
    static_pages = [
        ('/?view=about', '0.6', 'monthly'),
        ('/?view=delivery', '0.5', 'monthly'),
        ('/?view=returns', '0.5', 'monthly'),
        ('/?view=faqs', '0.5', 'monthly'),
        ('/?view=contact', '0.5', 'monthly'),
        ('/?view=sustainability', '0.5', 'monthly'),
        ('/?view=privacy', '0.3', 'yearly'),
        ('/?view=terms', '0.3', 'yearly'),
        ('/?view=cookies', '0.3', 'yearly'),
    ]
    
    for path, priority, changefreq in static_pages:
        urls.append({
            'loc': f"{BASE_URL}{path}",
            'lastmod': today,
            'changefreq': changefreq,
            'priority': priority
        })
    
    # Product pages
    for product in in_stock_products:
        sku = product.get('sku', '')
        if sku:
            urls.append({
                'loc': f"{BASE_URL}/?product={quote(sku)}",
                'lastmod': today,
                'changefreq': 'weekly',
                'priority': '0.7'
            })
    
    # Generate XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    
    for url in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{url["loc"]}</loc>')
        xml_lines.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{url["priority"]}</priority>')
        xml_lines.append('  </url>')
    
    xml_lines.append('</urlset>')
    
    # Write sitemap
    sitemap_content = '\n'.join(xml_lines)
    with open('sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    
    print(f"✅ Sitemap generated with {len(urls)} URLs")
    print(f"   - 1 homepage")
    print(f"   - {len(CATEGORIES)} category pages")
    print(f"   - {len(BRANDS)} brand pages")
    print(f"   - {len(static_pages)} static pages")
    print(f"   - {len(in_stock_products)} product pages")
    print(f"\nSaved to: sitemap.xml")

if __name__ == '__main__':
    generate_sitemap()
