"""
Home & Verse - Best Sellers Generator
======================================
Fetches top selling items from Zoho Inventory based on sales orders
from the last 3 months across all channels.

Usage:
    cd /Users/matt/Desktop/home-and-verse/backend
    python3 generate_bestsellers.py
"""

import asyncio
import httpx
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

# Paths
DATA_DIR = Path("data")
BESTSELLERS_FILE = DATA_DIR / "bestsellers.json"
PRODUCTS_FILE = DATA_DIR / "products.json"

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
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"https://www.zohoapis.eu/inventory/v1/{endpoint}",
            headers={"Authorization": f"Zoho-oauthtoken {token}"},
            params=params
        )
        response.raise_for_status()
        return response.json()


async def fetch_sales_orders(start_date: str, end_date: str):
    """Fetch all sales orders within date range"""
    all_orders = []
    page = 1
    
    while True:
        print(f"  Fetching sales orders page {page}...", end=" ", flush=True)
        
        try:
            result = await zoho_get("salesorders", {
                "page": page,
                "per_page": 200,
                "date_start": start_date,
                "date_end": end_date,
                "sort_column": "date",
                "sort_order": "D"  # Descending
            })
            
            orders = result.get("salesorders", [])
            all_orders.extend(orders)
            print(f"({len(all_orders)} total)")
            
            if not result.get("page_context", {}).get("has_more_page", False):
                break
            
            page += 1
            await asyncio.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"\n  Error fetching orders: {e}")
            break
    
    return all_orders


async def fetch_order_details(salesorder_id: str):
    """Fetch detailed order with line items"""
    try:
        result = await zoho_get(f"salesorders/{salesorder_id}")
        return result.get("salesorder", {})
    except Exception as e:
        print(f"  Error fetching order {salesorder_id}: {e}")
        return None


def load_products():
    """Load products to get additional info"""
    if not PRODUCTS_FILE.exists():
        return {}
    
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    
    # Create lookup by SKU
    return {p.get("sku"): p for p in data.get("products", [])}


async def generate_bestsellers():
    """Main function to generate best sellers list"""
    print("=" * 60)
    print("HOME & VERSE - BEST SELLERS GENERATOR")
    print("=" * 60)
    
    # Check credentials
    if not all([ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN, ZOHO_ORG_ID]):
        print("\nERROR: Missing Zoho credentials in .env file")
        return
    
    # Calculate date range (last 3 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print(f"\nDate range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Fetch sales orders
    print("\n1. FETCHING SALES ORDERS")
    print("-" * 40)
    
    orders = await fetch_sales_orders(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    
    print(f"   Total orders found: {len(orders)}")
    
    if not orders:
        print("   No orders found in date range!")
        return
    
    # Aggregate sales by item
    print("\n2. AGGREGATING ITEM SALES")
    print("-" * 40)
    
    item_sales = defaultdict(lambda: {
        "quantity_sold": 0,
        "revenue": 0,
        "order_count": 0,
        "name": "",
        "sku": "",
        "item_id": ""
    })
    
    orders_processed = 0
    
    for i, order in enumerate(orders):
        # Only count confirmed/fulfilled orders
        status = order.get("order_status", "").lower()
        if status in ["draft", "void", "cancelled"]:
            continue
        
        # Fetch full order details to get line items
        order_id = order.get("salesorder_id")
        if not order_id:
            continue
        
        # Progress indicator
        if (i + 1) % 50 == 0:
            print(f"   Processing order {i + 1}/{len(orders)}...")
        
        full_order = await fetch_order_details(order_id)
        if not full_order:
            continue
        
        orders_processed += 1
        
        # Process line items
        line_items = full_order.get("line_items", [])
        for item in line_items:
            sku = item.get("sku", "")
            if not sku:
                continue
            
            quantity = float(item.get("quantity", 0))
            item_total = float(item.get("item_total", 0))
            
            item_sales[sku]["quantity_sold"] += quantity
            item_sales[sku]["revenue"] += item_total
            item_sales[sku]["order_count"] += 1
            item_sales[sku]["name"] = item.get("name", "")
            item_sales[sku]["sku"] = sku
            item_sales[sku]["item_id"] = item.get("item_id", "")
        
        await asyncio.sleep(0.15)  # Rate limiting
    
    print(f"   Orders processed: {orders_processed}")
    print(f"   Unique items sold: {len(item_sales)}")
    
    # Load product data for enrichment
    print("\n3. ENRICHING WITH PRODUCT DATA")
    print("-" * 40)
    
    products = load_products()
    print(f"   Products in catalog: {len(products)}")
    
    # Create bestsellers list
    print("\n4. GENERATING TOP 50 BESTSELLERS")
    print("-" * 40)
    
    # Sort by quantity sold
    sorted_items = sorted(
        item_sales.items(),
        key=lambda x: x[1]["quantity_sold"],
        reverse=True
    )
    
    bestsellers = []
    
    for sku, sales_data in sorted_items[:50]:
        product = products.get(sku, {})
        
        bestseller = {
            "sku": sku,
            "name": sales_data["name"] or product.get("name", "Unknown"),
            "quantity_sold": int(sales_data["quantity_sold"]),
            "revenue": round(sales_data["revenue"], 2),
            "order_count": sales_data["order_count"],
            "brand": product.get("brand", ""),
            "price": product.get("price", 0),
            "categories": product.get("categories", []),
            "has_image": product.get("has_image", False),
            "image_url": product.get("image_url"),
            "in_stock": product.get("in_stock", False),
            "in_catalog": sku in products
        }
        
        bestsellers.append(bestseller)
    
    # Filter to only items in our catalog with images
    catalog_bestsellers = [b for b in bestsellers if b["in_catalog"] and b["has_image"]]
    
    print(f"   Top 50 by quantity sold:")
    print(f"   - In our catalog with images: {len(catalog_bestsellers)}")
    print(f"   - Not in catalog/no images: {len(bestsellers) - len(catalog_bestsellers)}")
    
    # Save results
    print("\n5. SAVING DATA")
    print("-" * 40)
    
    output = {
        "bestsellers": catalog_bestsellers,
        "generated_at": datetime.now().isoformat(),
        "date_range": {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "days": 90
        },
        "stats": {
            "orders_processed": orders_processed,
            "unique_items_sold": len(item_sales),
            "bestsellers_count": len(catalog_bestsellers)
        }
    }
    
    DATA_DIR.mkdir(exist_ok=True)
    with open(BESTSELLERS_FILE, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"   Saved to: {BESTSELLERS_FILE}")
    
    # Summary
    print("\n" + "=" * 60)
    print("BEST SELLERS GENERATED")
    print("=" * 60)
    
    print(f"\nTop 10 Best Sellers:")
    for i, item in enumerate(catalog_bestsellers[:10], 1):
        stock_status = "✓" if item["in_stock"] else "✗"
        print(f"  {i:2}. {item['sku']}: {item['name'][:35]}")
        print(f"      Sold: {item['quantity_sold']} | Revenue: £{item['revenue']:.2f} | Stock: {stock_status}")
    
    print(f"\nBy Brand:")
    brand_counts = defaultdict(int)
    for item in catalog_bestsellers:
        brand_counts[item["brand"]] += 1
    for brand, count in sorted(brand_counts.items(), key=lambda x: -x[1]):
        print(f"  {brand}: {count}")


if __name__ == "__main__":
    asyncio.run(generate_bestsellers())
