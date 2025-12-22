"""Quick check of Zoho brands and product data"""
import asyncio
import httpx
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

async def get_token():
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
        return response.json()["access_token"]

async def check_brands():
    token = await get_token()
    
    all_items = []
    page = 1
    
    print("Fetching all items from Zoho...")
    while True:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://www.zohoapis.eu/inventory/v1/items",
                headers={"Authorization": f"Zoho-oauthtoken {token}"},
                params={"organization_id": ZOHO_ORG_ID, "page": page, "per_page": 200}
            )
            data = response.json()
            items = data.get("items", [])
            all_items.extend(items)
            print(f"  Page {page}: {len(items)} items (total: {len(all_items)})")
            
            if not data.get("page_context", {}).get("has_more_page", False):
                break
            page += 1
            await asyncio.sleep(0.3)
    
    print(f"\n{'='*60}")
    print(f"TOTAL ITEMS: {len(all_items)}")
    print(f"{'='*60}")
    
    # Check brand field
    brands = Counter()
    manufacturers = Counter()
    no_brand = []
    
    for item in all_items:
        brand = item.get("brand", "")
        manufacturer = item.get("manufacturer", "")
        
        if brand:
            brands[brand] += 1
        if manufacturer:
            manufacturers[manufacturer] += 1
        
        if not brand and not manufacturer:
            no_brand.append(item.get("sku") or item.get("name"))
    
    print(f"\n--- BRAND FIELD VALUES ---")
    for brand, count in brands.most_common(30):
        print(f"  '{brand}': {count}")
    
    print(f"\n--- MANUFACTURER FIELD VALUES ---")
    for mfr, count in manufacturers.most_common(30):
        print(f"  '{mfr}': {count}")
    
    print(f"\n--- ITEMS WITH NO BRAND/MANUFACTURER: {len(no_brand)} ---")
    if no_brand[:10]:
        for sku in no_brand[:10]:
            print(f"  {sku}")
        if len(no_brand) > 10:
            print(f"  ... and {len(no_brand) - 10} more")
    
    # Check for consumer brands
    print(f"\n{'='*60}")
    print("CONSUMER BRAND DETECTION")
    print(f"{'='*60}")
    
    consumer_keywords = ["rader", "räder", "my flame", "remember", "relaxound", "ideas4seasons", "ideas 4 seasons"]
    
    found = {k: [] for k in ["Räder", "My Flame", "Remember", "Relaxound", "Ideas4Seasons", "Other/Unknown"]}
    
    for item in all_items:
        if item.get("status") != "active":
            continue
            
        brand = (item.get("brand") or "").lower()
        mfr = (item.get("manufacturer") or "").lower()
        combined = f"{brand} {mfr}"
        
        if "rader" in combined or "räder" in combined:
            found["Räder"].append(item)
        elif "my flame" in combined or "myflame" in combined:
            found["My Flame"].append(item)
        elif "remember" in combined:
            found["Remember"].append(item)
        elif "relaxound" in combined:
            found["Relaxound"].append(item)
        elif "ideas4seasons" in combined or "ideas 4 seasons" in combined:
            found["Ideas4Seasons"].append(item)
    
    for brand, items in found.items():
        if brand != "Other/Unknown":
            print(f"\n{brand}: {len(items)} items")
            if items:
                # Show sample
                for item in items[:3]:
                    sku = item.get("sku", "?")
                    name = item.get("name", "?")[:40]
                    has_img = "✓" if item.get("image_document_id") else "✗"
                    price = item.get("rate", 0)
                    stock = item.get("stock_on_hand", 0)
                    print(f"    {sku}: {name}... £{price:.2f} (stock: {stock}) [img:{has_img}]")
    
    # Show what fields are available
    print(f"\n{'='*60}")
    print("SAMPLE ITEM FIELDS")
    print(f"{'='*60}")
    if all_items:
        sample = all_items[0]
        for key in sorted(sample.keys()):
            val = sample[key]
            if isinstance(val, str) and len(val) > 50:
                val = val[:50] + "..."
            print(f"  {key}: {val}")

asyncio.run(check_brands())
