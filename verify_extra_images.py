#!/usr/bin/env python3
"""
Verify which extra images actually exist on the CDN.
Reads image_extras.json, checks each URL, and outputs verified_image_extras.json
with only the images that return HTTP 200.

Also updates products.json to include an 'extra_images' field on each product.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

CDN_BASE = "https://cdn.appdmbrands.com/products"
DATA_DIR = Path(__file__).parent / "backend" / "data"
EXTRAS_FILE = DATA_DIR / "image_extras.json"
PRODUCTS_FILE = DATA_DIR / "products.json"
OUTPUT_FILE = DATA_DIR / "verified_image_extras.json"


def get_image_url(sku, suffix, brand=""):
    """Build the full CDN URL for an extra image"""
    if brand.lower() == "elvang":
        return f"{CDN_BASE}/elvang/{suffix}.jpg"
    return f"{CDN_BASE}/{suffix}.jpg"


def check_url(url):
    """Check if a URL returns 200 using curl (urllib gets blocked by CDN)"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "10", url],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip() == "200"
    except:
        return False


def main():
    # Load data
    with open(EXTRAS_FILE) as f:
        extras = json.load(f)

    with open(PRODUCTS_FILE) as f:
        products_data = json.load(f)

    products = products_data.get("products", products_data)

    # Build brand lookup
    brand_map = {}
    for p in products:
        brand_map[p.get("sku", "")] = p.get("brand", "")

    # Count total URLs to check
    total_urls = sum(len(v) for v in extras.values())
    print(f"\n🔍 Checking {total_urls} extra images across {len(extras)} products...\n")

    verified = {}
    checked = 0
    found = 0
    not_found = 0
    start_time = time.time()

    for sku, suffixes in extras.items():
        brand = brand_map.get(sku, "")
        valid_for_sku = []

        for suffix in suffixes:
            checked += 1
            url = get_image_url(sku, suffix, brand)
            exists = check_url(url)

            if exists:
                valid_for_sku.append(suffix)
                found += 1
                status = "✅"
            else:
                not_found += 1
                status = "❌"

            # Progress counter
            elapsed = time.time() - start_time
            rate = checked / elapsed if elapsed > 0 else 0
            remaining = (total_urls - checked) / rate if rate > 0 else 0

            sys.stdout.write(
                f"\r  [{checked}/{total_urls}] {status} {suffix}.jpg  "
                f"|  ✅ {found}  ❌ {not_found}  |  ~{remaining:.0f}s remaining   "
            )
            sys.stdout.flush()

        if valid_for_sku:
            verified[sku] = valid_for_sku

    elapsed = time.time() - start_time

    print(f"\n\n{'='*60}")
    print(f"📊 Results:")
    print(f"   Total checked:    {checked}")
    print(f"   Found (200):      {found}")
    print(f"   Not found (404):  {not_found}")
    print(f"   Products with extras: {len(verified)}")
    print(f"   Time taken:       {elapsed:.1f}s")
    print(f"{'='*60}\n")

    # Save verified extras
    with open(OUTPUT_FILE, "w") as f:
        json.dump(verified, f, indent=2)
    print(f"✅ Saved verified extras to: {OUTPUT_FILE}")

    # Now update products.json to include extra_images field
    print(f"\n📝 Updating products.json with extra_images field...")

    updated_count = 0
    for product in products:
        sku = product.get("sku", "")
        brand = product.get("brand", "")

        if sku in verified:
            extra_urls = []
            for suffix in verified[sku]:
                if brand.lower() == "elvang":
                    extra_urls.append(f"/products/elvang/{suffix}.jpg")
                else:
                    extra_urls.append(f"/products/{suffix}.jpg")

            product["extra_images"] = extra_urls
            updated_count += 1
        else:
            product.pop("extra_images", None)

    # Save updated products
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(
            {"products": products} if isinstance(products_data, dict) else products,
            f,
            indent=2,
        )

    print(f"✅ Updated {updated_count} products with extra_images in products.json")

    # Show some examples
    print(f"\n📸 Sample products with extras:")
    count = 0
    for product in products:
        if product.get("extra_images") and count < 10:
            sku = product.get("sku", "")
            name = product.get("name", "")[:40]
            extras_list = product.get("extra_images", [])
            print(f"  {sku} - {name}: {len(extras_list)} extra image(s)")
            for img in extras_list:
                print(f"    {img}")
            count += 1

    print(f"\n🎉 Done! Now rebuild and deploy:")
    print(f"   cd ~/Desktop/home-and-verse")
    print(f"   npm run build && git add -A && git commit -m 'Add verified extra images to products' && git push")


if __name__ == "__main__":
    main()
