#!/usr/bin/env python3
"""
Generate AI descriptions for new products only (ones without descriptions)
Uses Claude API with rate limiting to avoid issues
"""
import json
import os
import time
import anthropic
from dotenv import load_dotenv

load_dotenv()

PRODUCTS_FILE = '/Users/matt/Desktop/home-and-verse/backend/data/products.json'
DELAY_BETWEEN_CALLS = 0.5  # seconds

# Brand-specific tone guidelines
BRAND_TONES = {
    "Räder": "Poetic, whimsical German design. Emphasize craftsmanship, sentiment, and the poetry of everyday moments.",
    "Ideas4Seasons": "Fresh, seasonal, nature-inspired. Focus on bringing the outdoors in and seasonal transitions.",
    "Remember": "Bold, colourful, playful German design. Highlight fun patterns, vibrant colours, and joyful living.",
    "Elvang": "Scandinavian luxury, understated elegance. Emphasize premium materials, timeless design, and Danish craftsmanship.",
    "My Flame": "Warm, personal, meaningful gifts. Focus on the message, sentiment, and the joy of giving.",
    "Relaxound": "Calming, nature sounds, mindfulness. Emphasize relaxation, ambient soundscapes, and wellbeing.",
}

def generate_description(client, product):
    """Generate a description for a single product"""
    brand = product.get('brand', '')
    name = product.get('name', '')
    sku = product.get('sku', '')
    
    tone = BRAND_TONES.get(brand, "Elegant, thoughtful homeware.")
    
    prompt = f"""Write a short, engaging product description (2-3 sentences, max 50 words) for an online homeware store.

Product: {name}
Brand: {brand}
SKU: {sku}

Brand tone: {tone}

Rules:
- No generic phrases like "perfect for any home"
- No exclamation marks
- British English spelling
- Focus on what makes this product special
- Don't mention the SKU or repeat the full product name"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"  Error generating for {sku}: {e}")
        return None

def main():
    print("=" * 50)
    print("Home & Verse - Generate Descriptions for New Products")
    print("=" * 50)
    
    # Load products
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    products = data['products']
    
    # Find products without descriptions
    needs_description = []
    for p in products:
        desc = p.get('description', '') or ''
        ai_desc = p.get('ai_description', '') or ''
        if not desc.strip() and not ai_desc.strip():
            needs_description.append(p)
    
    print(f"Total products: {len(products)}")
    print(f"Need descriptions: {len(needs_description)}")
    
    if not needs_description:
        print("\nAll products have descriptions!")
        return
    
    # Count by brand
    by_brand = {}
    for p in needs_description:
        brand = p.get('brand', 'Unknown')
        by_brand[brand] = by_brand.get(brand, 0) + 1
    
    print("\nBy brand:")
    for brand, count in sorted(by_brand.items(), key=lambda x: -x[1]):
        print(f"  {brand}: {count}")
    
    print(f"\nGenerating descriptions (with {DELAY_BETWEEN_CALLS}s delay)...")
    print("=" * 50)
    
    # Initialize Claude client
    client = anthropic.Anthropic()
    
    generated = 0
    failed = 0
    
    # Build SKU to index map for updating
    sku_to_idx = {p['sku']: i for i, p in enumerate(products)}
    
    for i, product in enumerate(needs_description):
        sku = product['sku']
        name = product['name']
        
        desc = generate_description(client, product)
        
        if desc:
            # Update the product in the main list
            idx = sku_to_idx[sku]
            products[idx]['ai_description'] = desc
            products[idx]['description'] = desc
            generated += 1
            
            if generated % 25 == 0:
                print(f"✓ Generated {generated}/{len(needs_description)}...")
                # Save progress
                data['products'] = products
                with open(PRODUCTS_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
        else:
            failed += 1
        
        time.sleep(DELAY_BETWEEN_CALLS)
    
    # Final save
    data['products'] = products
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print()
    print("=" * 50)
    print(f"COMPLETE")
    print(f"  Generated: {generated}")
    print(f"  Failed: {failed}")
    print(f"\nSaved to {PRODUCTS_FILE}")

if __name__ == '__main__':
    main()
