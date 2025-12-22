"""
Home & Verse - Zoho Product Import
===================================
Downloads all products and images from Zoho for the 5 consumer brands.

Usage:
    cd /Users/matt/Desktop/home-and-verse/backend
    python3 import_from_zoho.py

Options:
    --in-stock-only    Only import products with stock > 0
    --skip-images      Skip downloading images (faster for testing)
"""

import asyncio
import httpx
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

# Command line options
IN_STOCK_ONLY = "--in-stock-only" in sys.argv
SKIP_IMAGES = "--skip-images" in sys.argv

# Brand mapping (based on actual Zoho data)
BRAND_MAP = {
    "räder": "Räder",
    "rader": "Räder",
    "rader gmbh": "Räder",
    "my flame lifestyle": "My Flame",
    "my flame": "My Flame",
    "remember": "Remember",
    "relaxound": "Relaxound",
    "ideas 4 seasons": "Ideas4Seasons",
    "ideas4seasons": "Ideas4Seasons",
    "elvang": "Elvang",
}

# Category keywords - products can match multiple categories
# New structure: Christmas, Candles & Fragrance, Lighting, Tableware, Home Décor, Gifts
CATEGORY_KEYWORDS = {
    # ==========================================
    # CHRISTMAS - seasonal festive items
    # ==========================================
    "christmas": ["Christmas"],
    "xmas": ["Christmas"],
    "advent": ["Christmas"],
    "santa": ["Christmas"],
    "snowman": ["Christmas"],
    "angel": ["Christmas", "Home Décor"],
    "star": ["Christmas", "Home Décor"],
    "bauble": ["Christmas"],
    "reindeer": ["Christmas"],
    "deer": ["Christmas", "Home Décor"],
    "elk": ["Christmas"],
    "sleigh": ["Christmas"],
    "snow": ["Christmas"],
    "frost": ["Christmas"],
    "winter": ["Christmas"],
    "gingerbread": ["Christmas"],
    "nutcracker": ["Christmas"],
    "holly": ["Christmas"],
    "mistletoe": ["Christmas"],
    "fir tree": ["Christmas"],
    "fir light": ["Christmas", "Lighting"],
    "festive": ["Christmas"],
    "holiday": ["Christmas"],
    "noel": ["Christmas"],
    "wreath": ["Christmas", "Home Décor"],
    "garland": ["Christmas"],
    "king's light": ["Christmas", "Lighting"],
    "nativity": ["Christmas"],
    
    # ==========================================
    # CANDLES & FRAGRANCE
    # ==========================================
    "candle": ["Candles & Fragrance"],
    "duftkerze": ["Candles & Fragrance"],
    "kerze": ["Candles & Fragrance"],
    "tealight": ["Candles & Fragrance"],
    "tea light": ["Candles & Fragrance"],
    "wax": ["Candles & Fragrance"],
    "scented": ["Candles & Fragrance"],
    "fragrance": ["Candles & Fragrance"],
    "aroma": ["Candles & Fragrance"],
    "diffuser": ["Candles & Fragrance", "Gifts"],
    "reed diffuser": ["Candles & Fragrance", "Gifts"],
    "room spray": ["Candles & Fragrance", "Gifts"],
    "matches": ["Candles & Fragrance", "Gifts"],
    "dinner candle": ["Candles & Fragrance"],
    "candlestick": ["Candles & Fragrance", "Home Décor"],
    "candle holder": ["Candles & Fragrance", "Home Décor"],
    
    # ==========================================
    # LIGHTING - lamps, lanterns, light houses
    # ==========================================
    "light house": ["Lighting"],
    "lighthouse": ["Lighting"],
    "lichthaus": ["Lighting"],
    "lamp": ["Lighting"],
    "lantern": ["Lighting"],
    "laterne": ["Lighting"],
    "led light": ["Lighting"],
    "led mini": ["Lighting"],
    "nightlight": ["Lighting"],
    "uri": ["Lighting"],  # URI lamps
    "glossy light": ["Lighting"],
    "light object": ["Lighting"],
    "light landscape": ["Lighting"],
    
    # ==========================================
    # TABLEWARE - dining and kitchen items
    # ==========================================
    "mug": ["Tableware", "Gifts"],
    "cup": ["Tableware"],
    "becher": ["Tableware"],
    "bowl": ["Tableware", "Home Décor"],
    "plate": ["Tableware"],
    "dish": ["Tableware"],
    "tray": ["Tableware", "Home Décor"],
    "etagere": ["Tableware", "Home Décor"],
    "napkin": ["Tableware"],
    "serviette": ["Tableware"],
    "coaster": ["Tableware"],
    "glass": ["Tableware"],
    "carafe": ["Tableware"],
    "jug": ["Tableware"],
    "espresso": ["Tableware", "Gifts"],
    "egg cup": ["Tableware"],
    "cutting board": ["Tableware"],
    "cruet": ["Tableware"],
    "wine cooler": ["Tableware"],
    "bottle opener": ["Tableware", "Gifts"],
    "spoon": ["Tableware"],
    "jar": ["Tableware", "Home Décor"],
    
    # ==========================================
    # HOME DÉCOR - decorative items, textiles, storage
    # ==========================================
    # Elvang textiles
    "throw": ["Home Décor"],
    "scarf": ["Home Décor", "Gifts"],
    "shawl": ["Home Décor", "Gifts"],
    "alpaca": ["Home Décor"],
    "duvet": ["Home Décor"],
    "bedcover": ["Home Décor"],
    "bed linen": ["Home Décor"],
    
    "vase": ["Home Décor"],
    "figure": ["Home Décor"],
    "figurine": ["Home Décor"],
    "sculpture": ["Home Décor"],
    "ornament": ["Home Décor"],
    "decoration": ["Home Décor"],
    "cushion": ["Home Décor"],
    "pillow": ["Home Décor"],
    "blanket": ["Home Décor"],
    "throw": ["Home Décor"],
    "rug": ["Home Décor"],
    "towel": ["Home Décor"],
    "basket": ["Home Décor"],
    "storage": ["Home Décor"],
    "box": ["Home Décor", "Gifts"],
    "tin": ["Home Décor", "Gifts"],
    "mirror": ["Home Décor"],
    "frame": ["Home Décor", "Gifts"],
    "hook": ["Home Décor"],
    "hanger": ["Home Décor"],
    "pot": ["Home Décor"],
    "planter": ["Home Décor"],
    "bird": ["Home Décor"],
    "flower carrier": ["Home Décor"],
    "ball": ["Home Décor"],
    
    # ==========================================
    # GIFTS - gift sets, bath & body, cards, soundboxes
    # ==========================================
    "gift": ["Gifts"],
    "present": ["Gifts"],
    "giftbox": ["Gifts"],
    "gift set": ["Gifts"],
    "zwitscherbox": ["Gifts", "Home Décor"],
    "birdybox": ["Gifts", "Home Décor"],
    "lakeside": ["Gifts", "Home Décor"],
    "soundbox": ["Gifts", "Home Décor"],
    "relaxound": ["Gifts", "Home Décor"],
    "bath bomb": ["Gifts"],
    "bath salt": ["Gifts"],
    "soap": ["Gifts"],
    "hand cream": ["Gifts"],
    "lip balm": ["Gifts"],
    "body wash": ["Gifts"],
    "massage": ["Gifts"],
    "spa": ["Gifts"],
    "card": ["Gifts"],
    "keychain": ["Gifts"],
    "keyring": ["Gifts"],
    "key ring": ["Gifts"],
    "puzzle": ["Gifts"],
    "game": ["Gifts"],
    "notebook": ["Gifts"],
    "guestbook": ["Gifts"],
    "calendar": ["Gifts"],
    "money box": ["Gifts", "Home Décor"],
    "lucky": ["Gifts"],
    "guardian angel": ["Gifts"],
    "apron": ["Gifts", "Home Décor"],
    "bag": ["Gifts"],
    "fan": ["Gifts"],
    "boccia": ["Gifts"],
    "kubb": ["Gifts"],
    "curling": ["Gifts"],
}

# Paths
DATA_DIR = Path("data")
IMAGES_DIR = DATA_DIR / "images"
PRODUCTS_FILE = DATA_DIR / "products.json"
STOCK_FILE = DATA_DIR / "stock.json"

# Token cache
_access_token = None
_token_expires = None


async def get_access_token():
    """Get or refresh Zoho access token"""
    global _access_token, _token_expires
    
    if _access_token and _token_expires and datetime.now().timestamp() < _token_expires:
        return _access_token
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://accounts.zoho.eu/oauth/v2/token",
            params={
                "refresh_token": ZOHO_REFRESH_TOKEN,
                "client_id": ZOHO_CLIENT_ID,
                "client_secret": ZOHO_CLIENT_SECRET,
                "grant_type": "refresh_token"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        _access_token = data["access_token"]
        _token_expires = datetime.now().timestamp() + data.get("expires_in", 3600) - 60
        
        return _access_token


async def zoho_get(endpoint: str, params: dict = None):
    """Make authenticated GET request to Zoho"""
    token = await get_access_token()
    
    if params is None:
        params = {}
    params["organization_id"] = ZOHO_ORG_ID
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"https://www.zohoapis.eu/inventory/v1/{endpoint}",
            headers={"Authorization": f"Zoho-oauthtoken {token}"},
            params=params
        )
        response.raise_for_status()
        return response.json()


async def download_image(item_id: str, sku: str) -> bool:
    """Download product image from Zoho"""
    if SKIP_IMAGES:
        return False
    
    # Clean SKU for filename
    safe_sku = "".join(c if c.isalnum() or c in "-_" else "_" for c in sku)
    image_path = IMAGES_DIR / f"{safe_sku}.jpg"
    
    # Skip if already downloaded
    if image_path.exists() and image_path.stat().st_size > 100:
        return True
    
    token = await get_access_token()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://www.zohoapis.eu/inventory/v1/items/{item_id}/image",
                headers={"Authorization": f"Zoho-oauthtoken {token}"},
                params={"organization_id": ZOHO_ORG_ID}
            )
            
            if response.status_code == 200 and len(response.content) > 100:
                with open(image_path, "wb") as f:
                    f.write(response.content)
                return True
            else:
                return False
    except Exception as e:
        return False


def get_display_brand(brand_raw: str) -> str:
    """Normalize brand name to display version"""
    if not brand_raw:
        return None
    
    brand_lower = brand_raw.lower().strip()
    
    for key, display in BRAND_MAP.items():
        if key in brand_lower:
            return display
    
    return None


def guess_categories(name: str, brand: str) -> list:
    """Guess product categories from name and brand - returns list of categories"""
    name_lower = name.lower()
    categories = set()
    
    # Brand-specific defaults
    if brand == "My Flame":
        categories.add("Candles & Fragrance")
    if brand == "Relaxound":
        categories.add("Home Décor")
        categories.add("Gifts")
    if brand == "Elvang":
        categories.add("Home Décor")
    
    # Check keywords - collect ALL matching categories
    for keyword, cats in CATEGORY_KEYWORDS.items():
        if keyword in name_lower:
            for cat in cats:
                categories.add(cat)
    
    # Default to Home Décor if no categories found
    if not categories:
        categories.add("Home Décor")
    
    return sorted(list(categories))


def should_filter_product(item: dict, display_brand: str) -> tuple[bool, str]:
    """
    Check if product should be filtered from consumer site.
    Returns (should_filter, reason)
    """
    name = (item.get("name") or "").lower()
    sku = (item.get("sku") or "").lower()
    trade_price = float(item.get("rate", 0))
    
    # Zero or missing price
    if trade_price <= 0:
        return True, "zero_price"
    
    # Display items
    if "display" in name or "display" in sku or ".disp" in sku:
        return True, "display_item"
    
    # Bulk tray packs (tray.24, tray_24, etc)
    if re.search(r'tray[\._]\d+', sku):
        return True, "bulk_tray"
    
    # Wholesale multi-packs (12+ units)
    # Matches: "72 Stk", "16 pcs", "24 pieces", etc
    match = re.search(r'(\d+)\s*(stk|pcs|pieces|units)', name)
    if match and int(match.group(1)) >= 12:
        return True, "wholesale_multipack"
    
    return False, ""


def clean_product_name(name: str) -> str:
    """Clean up product name for display"""
    # Remove common annotations
    patterns = [
        r'\*\*[^*]+\*\*',  # **LAST CHANGE** etc
        r'\s*-\s*$',       # Trailing dash
        r'\s+',            # Multiple spaces
    ]
    
    cleaned = name
    for pattern in patterns:
        cleaned = re.sub(pattern, ' ', cleaned)
    
    return cleaned.strip()


def calculate_retail_price(trade_price: float) -> float:
    """Calculate retail price from trade price"""
    if trade_price <= 0:
        return 0
    
    # 2.4x markup
    retail = trade_price * 2.4
    
    # Round to .95 pricing
    rounded = round(retail)
    return rounded - 0.05 if rounded - 0.05 > 0 else rounded + 0.95


async def fetch_all_items():
    """Fetch all items from Zoho with pagination"""
    all_items = []
    page = 1
    
    while True:
        print(f"  Fetching page {page}...", end=" ", flush=True)
        result = await zoho_get("items", {"page": page, "per_page": 200})
        items = result.get("items", [])
        all_items.extend(items)
        print(f"({len(all_items)} total)")
        
        if not result.get("page_context", {}).get("has_more_page", False):
            break
        
        page += 1
        await asyncio.sleep(0.3)
    
    return all_items


async def import_products():
    """Main import function"""
    print("=" * 60)
    print("HOME & VERSE - ZOHO PRODUCT IMPORT")
    print("=" * 60)
    
    if IN_STOCK_ONLY:
        print("Mode: IN-STOCK ONLY")
    if SKIP_IMAGES:
        print("Mode: SKIPPING IMAGES")
    
    # Check credentials
    if not all([ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN, ZOHO_ORG_ID]):
        print("\nERROR: Missing Zoho credentials in .env file")
        return
    
    # Create directories
    DATA_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)
    
    # Fetch all items
    print("\n1. FETCHING FROM ZOHO")
    print("-" * 40)
    all_items = await fetch_all_items()
    print(f"   Total items: {len(all_items)}")
    
    # Filter to consumer brands
    print("\n2. FILTERING CONSUMER BRANDS")
    print("-" * 40)
    
    consumer_items = []
    brand_counts = {}
    skipped_inactive = 0
    skipped_no_stock = 0
    skipped_filtered = {}
    
    for item in all_items:
        # Must be active
        if item.get("status") != "active":
            skipped_inactive += 1
            continue
        
        # Check brand
        brand_raw = item.get("brand") or item.get("manufacturer") or ""
        display_brand = get_display_brand(brand_raw)
        
        if not display_brand:
            continue
        
        # Check stock if in-stock-only mode
        stock = int(item.get("stock_on_hand", 0))
        if IN_STOCK_ONLY and stock <= 0:
            skipped_no_stock += 1
            continue
        
        # Check if product should be filtered (display items, bulk packs, etc)
        should_filter, filter_reason = should_filter_product(item, display_brand)
        if should_filter:
            skipped_filtered[filter_reason] = skipped_filtered.get(filter_reason, 0) + 1
            continue
        
        consumer_items.append({
            "item": item,
            "brand": display_brand
        })
        brand_counts[display_brand] = brand_counts.get(display_brand, 0) + 1
    
    print(f"   Consumer products found: {len(consumer_items)}")
    print(f"   Skipped (inactive): {skipped_inactive}")
    if IN_STOCK_ONLY:
        print(f"   Skipped (no stock): {skipped_no_stock}")
    
    if skipped_filtered:
        print(f"\n   Filtered out (not for consumer site):")
        for reason, count in sorted(skipped_filtered.items()):
            reason_display = reason.replace('_', ' ').title()
            print(f"     {reason_display}: {count}")
        print(f"     Total filtered: {sum(skipped_filtered.values())}")
    
    print("\n   By brand:")
    for brand, count in sorted(brand_counts.items()):
        print(f"     {brand}: {count}")
    
    # Process items
    print("\n3. PROCESSING PRODUCTS")
    print("-" * 40)
    
    products = []
    stock_data = {}
    images_downloaded = 0
    images_existed = 0
    images_missing = 0
    
    for i, item_data in enumerate(consumer_items):
        item = item_data["item"]
        brand = item_data["brand"]
        
        sku = item.get("sku") or str(item.get("item_id"))
        name = item.get("name", sku)
        
        # Progress
        if (i + 1) % 100 == 0:
            print(f"   Processed {i + 1}/{len(consumer_items)}...")
        
        # Download image
        has_image = False
        doc_id = item.get("image_document_id")
        if doc_id:
            safe_sku = "".join(c if c.isalnum() or c in "-_" else "_" for c in sku)
            image_path = IMAGES_DIR / f"{safe_sku}.jpg"
            
            if image_path.exists() and image_path.stat().st_size > 100:
                has_image = True
                images_existed += 1
            else:
                has_image = await download_image(item["item_id"], sku)
                if has_image:
                    images_downloaded += 1
                else:
                    images_missing += 1
                await asyncio.sleep(0.15)  # Rate limiting
        else:
            images_missing += 1
        
        # Calculate retail price
        trade_price = float(item.get("rate", 0))
        retail_price = calculate_retail_price(trade_price)
        
        # Clean SKU for image path
        safe_sku = "".join(c if c.isalnum() or c in "-_" else "_" for c in sku)
        
        # Get stock
        stock = max(0, int(item.get("stock_on_hand", 0)))  # No negative stock
        
        # Build product record
        product = {
            "id": item["item_id"],
            "sku": sku,
            "name": clean_product_name(name),
            "brand": brand,
            "description": item.get("description", ""),
            "price": retail_price,
            "trade_price": trade_price,
            "categories": guess_categories(name, brand),
            "ean": item.get("ean") or item.get("upc") or "",
            "has_image": has_image,
            "image_url": f"/images/{safe_sku}.jpg" if has_image else None,
            "in_stock": stock > 0,
            "stock": stock,
        }
        products.append(product)
        
        # Track stock separately
        stock_data[sku] = {
            "zoho_item_id": item["item_id"],
            "stock": stock,
            "updated_at": datetime.now().isoformat()
        }
    
    print(f"   Processed: {len(products)} products")
    
    # Save products
    print("\n4. SAVING DATA")
    print("-" * 40)
    
    with open(PRODUCTS_FILE, "w") as f:
        json.dump({
            "products": products,
            "imported_at": datetime.now().isoformat(),
            "count": len(products)
        }, f, indent=2)
    print(f"   {PRODUCTS_FILE}: {len(products)} products")
    
    with open(STOCK_FILE, "w") as f:
        json.dump({
            "stock": stock_data,
            "updated_at": datetime.now().isoformat()
        }, f, indent=2)
    print(f"   {STOCK_FILE}: {len(stock_data)} entries")
    
    # Summary
    print("\n" + "=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)
    
    print(f"\nProducts by brand:")
    by_brand = {}
    for p in products:
        by_brand[p["brand"]] = by_brand.get(p["brand"], 0) + 1
    for brand, count in sorted(by_brand.items()):
        print(f"  {brand}: {count}")
    
    print(f"\nProducts by category (products can appear in multiple):")
    by_cat = {}
    for p in products:
        for cat in p["categories"]:
            by_cat[cat] = by_cat.get(cat, 0) + 1
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # Count products with multiple categories
    multi_cat = sum(1 for p in products if len(p["categories"]) > 1)
    print(f"\n  Products in multiple categories: {multi_cat}")
    print(f"  Products in single category: {len(products) - multi_cat}")
    
    in_stock = sum(1 for p in products if p["in_stock"])
    print(f"\nStock status:")
    print(f"  In stock: {in_stock}")
    print(f"  Out of stock: {len(products) - in_stock}")
    
    print(f"\nImages:")
    print(f"  Already had: {images_existed}")
    print(f"  Downloaded: {images_downloaded}")
    print(f"  Missing: {images_missing}")
    
    print(f"\nFiles saved to: {DATA_DIR.absolute()}")
    
    # Filtered product summary
    if skipped_filtered:
        print(f"\nFiltered out:")
        for reason, count in sorted(skipped_filtered.items()):
            reason_display = reason.replace('_', ' ').title()
            print(f"  {reason_display}: {count}")
    
    # Sample products
    print(f"\nSample products:")
    for p in products[:5]:
        img = "✓" if p["has_image"] else "✗"
        stock_str = f"({p['stock']})" if p["in_stock"] else "(OUT)"
        cats = ", ".join(p["categories"])
        print(f"  {p['sku']}: {p['name'][:30]}... £{p['price']:.2f} {stock_str} [{cats}]")
    
    # Show some multi-category products
    multi_cat_products = [p for p in products if len(p["categories"]) > 1][:5]
    if multi_cat_products:
        print(f"\nSample multi-category products:")
        for p in multi_cat_products:
            cats = ", ".join(p["categories"])
            print(f"  {p['sku']}: {p['name'][:30]}... [{cats}]")


if __name__ == "__main__":
    asyncio.run(import_products())
