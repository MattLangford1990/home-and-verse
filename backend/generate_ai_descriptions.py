"""
Generate AI-powered product descriptions
========================================
Uses Claude to analyze product images and create compelling descriptions.

Usage:
    cd ~/Desktop/home-and-verse/backend
    python3 generate_ai_descriptions.py
    
Options:
    --limit N       Only process N products (for testing)
    --sku SKU       Process single SKU
    --force         Regenerate even if description exists
"""

import anthropic
import base64
import json
import sys
import time
import os
from pathlib import Path
from PIL import Image
import io

PRODUCTS_FILE = Path("data/products.json")
IMAGES_DIR = Path("data/images")

# Parse args
LIMIT = None
SINGLE_SKU = None
FORCE = "--force" in sys.argv

for i, arg in enumerate(sys.argv):
    if arg == "--limit" and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])
    if arg == "--sku" and i + 1 < len(sys.argv):
        SINGLE_SKU = sys.argv[i + 1]

# Brand context for better descriptions
BRAND_CONTEXT = {
    "Räder": "Räder is a renowned German design house known for minimalist, poetic homewares with clean Scandinavian-inspired aesthetics.",
    "Remember": "Remember is a colourful German lifestyle brand creating playful, vibrant home accessories and gifts.",
    "My Flame": "My Flame Lifestyle creates premium scented candles with meaningful messages, made in the Netherlands.",
    "Relaxound": "Relaxound creates innovative motion-activated sound boxes that bring nature sounds indoors.",
    "Ideas4Seasons": "Ideas4Seasons specialises in seasonal decorations and festive home accessories.",
}


def get_image_data(image_path: Path) -> tuple[str, str]:
    """Read image, detect format, resize if needed, return (base64_data, media_type)"""
    
    # Read the file to detect actual format
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    # Detect actual format from magic bytes
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        media_type = "image/png"
    elif image_bytes[:2] == b'\xff\xd8':
        media_type = "image/jpeg"
    elif image_bytes[:4] == b'GIF8':
        media_type = "image/gif"
    elif image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        media_type = "image/webp"
    else:
        # Default to jpeg
        media_type = "image/jpeg"
    
    # Check file size - API limit is 5MB
    file_size = len(image_bytes)
    max_size = 4.5 * 1024 * 1024  # 4.5MB to be safe
    
    if file_size > max_size:
        # Resize image to reduce file size
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            media_type = "image/jpeg"  # Convert to JPEG for smaller size
        
        # Calculate new size (reduce dimensions proportionally)
        scale_factor = 0.7
        while True:
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            
            resized = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Save to buffer
            buffer = io.BytesIO()
            if media_type == "image/jpeg":
                resized.save(buffer, format='JPEG', quality=85)
            else:
                resized.save(buffer, format='PNG')
            
            image_bytes = buffer.getvalue()
            
            if len(image_bytes) <= max_size or scale_factor < 0.3:
                break
            scale_factor -= 0.1
    
    return base64.standard_b64encode(image_bytes).decode("utf-8"), media_type


def generate_description(client: anthropic.Anthropic, product: dict, image_path: Path) -> str:
    """Use Claude to generate a product description from the image"""
    
    brand = product.get("brand", "")
    name = product.get("name", "")
    categories = product.get("categories", [])
    price = product.get("price", 0)
    
    brand_info = BRAND_CONTEXT.get(brand, "")
    
    # Build the prompt
    prompt = f"""You are writing a product description for an upmarket homeware e-commerce site called "Home & Verse".

Product: {name}
Brand: {brand}
Categories: {', '.join(categories)}
Price: £{price:.2f}

{f"Brand context: {brand_info}" if brand_info else ""}

Look at this product image and write a compelling 2-3 sentence description that:
1. Describes the actual physical appearance (colour, material, key design features you can see)
2. Suggests how it could be used or displayed
3. Captures the mood/style (e.g. Scandinavian, festive, minimalist)

Keep it warm and inviting but not overly flowery. Be specific about what you see - don't use generic phrases.
Write for a UK audience (use British spellings like "colour" not "color").

Just return the description text, nothing else."""

    # Read and encode image (with format detection and resizing)
    image_data, media_type = get_image_data(image_path)
    
    # Call Claude
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    
    return message.content[0].text.strip()


def main():
    print("=" * 60)
    print("AI PRODUCT DESCRIPTION GENERATOR")
    print("=" * 60)
    
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Load products
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    products = data["products"]
    
    # Filter to products with images
    products_with_images = [p for p in products if p.get("has_image")]
    
    # Apply filters
    if SINGLE_SKU:
        products_with_images = [p for p in products_with_images if p["sku"] == SINGLE_SKU]
        print(f"Processing single SKU: {SINGLE_SKU}")
    elif LIMIT:
        products_with_images = products_with_images[:LIMIT]
        print(f"Processing first {LIMIT} products")
    
    print(f"Products to process: {len(products_with_images)}")
    print("-" * 60)
    
    updated = 0
    errors = 0
    skipped = 0
    
    for i, product in enumerate(products_with_images):
        sku = product["sku"]
        name = product["name"]
        
        # Check if already has good description (unless --force)
        current_desc = product.get("description", "")
        name_lower = name.lower()
        
        has_poor_desc = (
            not current_desc or
            current_desc.lower() == name_lower or
            current_desc.lower() == f"{product['brand'].lower()} {name_lower}".strip() or
            current_desc.lower().startswith("this charming ceramic") or  # Our old template
            len(current_desc) < 50
        )
        
        if not has_poor_desc and not FORCE:
            skipped += 1
            continue
        
        # Find image (try both .jpg and .png)
        safe_sku = "".join(c if c.isalnum() or c in "-_" else "_" for c in sku)
        image_path = IMAGES_DIR / f"{safe_sku}.jpg"
        
        if not image_path.exists():
            # Try PNG
            image_path = IMAGES_DIR / f"{safe_sku}.png"
            
        if not image_path.exists():
            print(f"  [{sku}] No image found")
            errors += 1
            continue
        
        print(f"[{i+1}/{len(products_with_images)}] {sku}: {name[:40]}...", end=" ", flush=True)
        
        try:
            description = generate_description(client, product, image_path)
            
            # Update in main products list
            for p in products:
                if p["sku"] == sku:
                    p["description"] = description
                    break
            
            print("✓")
            print(f"    → {description[:80]}...")
            updated += 1
            
            # Rate limiting - be gentle with API
            time.sleep(0.5)
            
        except Exception as e:
            print(f"✗ Error: {e}")
            errors += 1
    
    # Save updated products
    print("\n" + "-" * 60)
    print("Saving...")
    
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\nComplete!")
    print(f"  Updated: {updated}")
    print(f"  Skipped (already has description): {skipped}")
    print(f"  Errors: {errors}")


if __name__ == "__main__":
    main()
