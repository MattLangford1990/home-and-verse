#!/usr/bin/env python3
"""
Generate Google Merchant Center product feed for Home & Verse
"""

import json
import csv
from pathlib import Path

PRODUCTS_FILE = Path("/Users/matt/Desktop/home-and-verse/backend/data/products.json")
OUTPUT_FILE = Path("/Users/matt/Desktop/home-and-verse/public/google-products.xml")
OUTPUT_CSV = Path("/Users/matt/Desktop/home-and-verse/public/google-products.csv")

SITE_URL = "https://www.homeandverse.co.uk"
CLOUDINARY_BASE = "https://res.cloudinary.com/dcfbgveei/image/upload"

def get_image_url(product):
    """Get the correct image URL for a product, ensuring it's Google-compatible (JPG format)"""
    sku = product.get('sku', '')
    brand = product.get('brand', '')
    image_path = product.get('image_url', '')
    
    # If it's already a full Cloudinary URL, use it but ensure JPG format
    if image_path and 'cloudinary.com' in image_path:
        # Replace any f_auto with f_jpg for Google compatibility
        url = image_path.replace('f_auto', 'f_jpg')
        # Add transforms if missing
        if '/upload/' in url and 'w_' not in url:
            url = url.replace('/upload/', '/upload/w_800,q_85,f_jpg/')
        return url
    
    # Handle different brands with different folder structures
    if brand == 'Elvang':
        # Elvang images are in elvang/ folder with _1 suffix
        return f"{CLOUDINARY_BASE}/w_800,q_85,f_jpg/elvang/{sku}_1.jpg"
    
    # For products with local image paths like /images/SKU.jpg
    if image_path:
        # Extract filename and handle SKU variations (dots to underscores for My Flame etc)
        filename = image_path.split('/')[-1]
        # Remove extension and use as-is (already has correct format)
        sku_part = filename.replace('.jpg', '').replace('.png', '')
        return f"{CLOUDINARY_BASE}/w_800,q_85,f_jpg/products/{sku_part}.jpg"
    
    # Default fallback - construct from SKU
    # Replace dots with underscores for SKUs like GL.CO.SA
    safe_sku = sku.replace('.', '_')
    return f"{CLOUDINARY_BASE}/w_800,q_85,f_jpg/products/{safe_sku}.jpg"

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
            'condition',
            'product_type',
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
            
            # Image URL - use correct URL based on product data
            image_url = get_image_url(p)
            
            # Category path for Google
            category_path = ' > '.join(['Home & Garden', 'Home Decor'] + categories[:2])
            
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
                'new',                                  # condition
                category_path,                          # product_type
                '0.5 kg'                                # shipping_weight (estimate)
            ])
    
    print(f"\n✅ Generated: {OUTPUT_CSV}")
    print(f"   Products in feed: {len(in_stock)}")
    
    # Also generate XML feed (RSS 2.0 format)
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
        category_path = ' &gt; '.join(['Home &amp; Garden', 'Home Decor'] + [c.replace('&', '&amp;') for c in categories[:2]])
        
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
        xml_lines.append(f'  <g:condition>new</g:condition>')
        xml_lines.append(f'  <g:product_type>{category_path}</g:product_type>')
        xml_lines.append('</item>')
    
    xml_lines.append('</channel>')
    xml_lines.append('</rss>')
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"✅ Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_feed()
