"""
Zoho Inventory Integration for Orders
======================================
Creates Sales Orders, manages customers, and syncs with Zoho.
Uses shared database cache for item lookups to minimize API calls.
"""

import httpx
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")

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


async def zoho_request(method: str, endpoint: str, data: dict = None, params: dict = None):
    """Make authenticated request to Zoho"""
    token = await get_access_token()
    
    if params is None:
        params = {}
    params["organization_id"] = ZOHO_ORG_ID
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        if method == "GET":
            response = await client.get(
                f"https://www.zohoapis.eu/inventory/v1/{endpoint}",
                headers={"Authorization": f"Zoho-oauthtoken {token}"},
                params=params
            )
        elif method == "POST":
            response = await client.post(
                f"https://www.zohoapis.eu/inventory/v1/{endpoint}",
                headers={
                    "Authorization": f"Zoho-oauthtoken {token}",
                    "Content-Type": "application/json"
                },
                params=params,
                json=data
            )
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response


# ============ SHARED CACHE (from dm-sales-app database) ============

_items_cache = None
_items_cache_loaded_at = None
CACHE_TTL = timedelta(hours=1)  # Refresh from DB hourly


def _load_items_from_db():
    """Load items from shared database cache, or fall back to local products.json"""
    global _items_cache, _items_cache_loaded_at
    
    # Try database first (shared with dm-sales-app)
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if DATABASE_URL:
        try:
            from database import SessionLocal, ProductCache
            db = SessionLocal()
            try:
                cache = db.query(ProductCache).filter(ProductCache.id == "main").first()
                if cache and cache.items_json:
                    _items_cache = json.loads(cache.items_json)
                    _items_cache_loaded_at = datetime.utcnow()
                    print(f"CACHE: Loaded {len(_items_cache)} items from shared database")
                    return _items_cache
            finally:
                db.close()
        except Exception as e:
            print(f"CACHE: Database error: {e}")
    
    # Fallback: Load from local products.json (has SKU + Zoho item_id)
    try:
        from pathlib import Path
        products_file = Path(__file__).parent / "data" / "products.json"
        if products_file.exists():
            with open(products_file) as f:
                data = json.load(f)
            products = data.get("products", [])
            # Convert to Zoho-like format - 'id' field is the Zoho item_id
            _items_cache = [
                {"sku": p.get("sku"), "item_id": p.get("id"), "name": p.get("name")}
                for p in products if p.get("sku") and p.get("id")
            ]
            _items_cache_loaded_at = datetime.utcnow()
            print(f"CACHE: Loaded {len(_items_cache)} items from local products.json")
            return _items_cache
    except Exception as e:
        print(f"CACHE: Error loading from products.json: {e}")
    
    return None


def _get_cached_items():
    """Get items from cache, refreshing from DB if needed"""
    global _items_cache, _items_cache_loaded_at
    
    now = datetime.utcnow()
    
    # Check if cache is valid
    if _items_cache and _items_cache_loaded_at:
        age = now - _items_cache_loaded_at
        if age < CACHE_TTL:
            return _items_cache
    
    # Load from database
    return _load_items_from_db()


async def get_item_by_sku(sku: str):
    """
    Get item details by SKU - uses shared database cache ONLY.
    No Zoho API fallback - if cache unavailable, returns None.
    """
    items = _get_cached_items()
    if items:
        for item in items:
            if item.get("sku") == sku:
                return item
        # SKU not found in cache
        print(f"CACHE: SKU {sku} not found in {len(items)} cached items")
        return None
    
    # No fallback to Zoho API - cache is required
    print(f"CACHE: Database cache unavailable - cannot look up SKU {sku}")
    return None


# ============ CUSTOMER OPERATIONS (still use Zoho API) ============

async def find_or_create_customer(email: str, name: str, phone: str = None, 
                                   billing_address: dict = None, shipping_address: dict = None):
    """Find existing customer by email or create new one"""
    
    # Search for existing customer
    response = await zoho_request("GET", "contacts", params={"email": email})
    
    if response.status_code == 200:
        data = response.json()
        contacts = data.get("contacts", [])
        if contacts:
            # Return existing customer
            return contacts[0]["contact_id"], contacts[0]
    
    # Create new customer
    customer_data = {
        "contact_name": name,
        "contact_type": "customer",
        "email": email,
        "phone": phone or "",
        "billing_address": billing_address or {},
        "shipping_address": shipping_address or billing_address or {},
        "notes": "Created via Home & Verse website"
    }
    
    response = await zoho_request("POST", "contacts", data=customer_data)
    
    if response.status_code in [200, 201]:
        data = response.json()
        contact = data.get("contact", {})
        return contact.get("contact_id"), contact
    else:
        error_msg = response.json().get("message", response.text)
        raise Exception(f"Failed to create customer: {error_msg}")


async def create_sales_order(customer_id: str, line_items: list, 
                             shipping_charge: float = 0, 
                             shipping_method: str = "Standard",
                             notes: str = "",
                             reference_number: str = None):
    """
    Create a Sales Order in Zoho Inventory
    
    line_items format:
    [
        {"item_id": "123456", "quantity": 2, "rate": 19.99},
        ...
    ]
    """
    
    order_data = {
        "customer_id": customer_id,
        "line_items": line_items,
        "shipping_charge": shipping_charge,
        "notes": notes,
        "terms": "Payment processed via Home & Verse website",
        "is_inclusive_tax": True,  # Prices include VAT
    }
    
    if reference_number:
        order_data["reference_number"] = reference_number
    
    response = await zoho_request("POST", "salesorders", data=order_data)
    
    if response.status_code in [200, 201]:
        data = response.json()
        sales_order = data.get("salesorder", {})
        return {
            "success": True,
            "salesorder_id": sales_order.get("salesorder_id"),
            "salesorder_number": sales_order.get("salesorder_number"),
            "total": sales_order.get("total"),
            "status": sales_order.get("status")
        }
    else:
        error_data = response.json()
        return {
            "success": False,
            "error": error_data.get("message", "Unknown error"),
            "code": error_data.get("code")
        }


async def create_order_from_cart(cart_items: list, customer_info: dict, 
                                  shipping_method: str = "standard",
                                  shipping_charge: float = 0,
                                  payment_intent_id: str = None):
    """
    Full order creation flow:
    1. Find or create customer
    2. Look up item IDs from SKUs (uses cache)
    3. Create sales order
    
    cart_items format:
    [
        {"sku": "ABC123", "quantity": 2, "price": 19.99},
        ...
    ]
    
    customer_info format:
    {
        "email": "test@example.com",
        "name": "John Smith",
        "phone": "07123456789",
        "address": {
            "address": "123 Main St",
            "city": "London",
            "state": "Greater London",
            "zip": "SW1A 1AA",
            "country": "United Kingdom"
        }
    }
    """
    
    try:
        # 1. Find or create customer (uses Zoho API - necessary for customers)
        customer_id, customer = await find_or_create_customer(
            email=customer_info["email"],
            name=customer_info["name"],
            phone=customer_info.get("phone"),
            billing_address=customer_info.get("address"),
            shipping_address=customer_info.get("shipping_address", customer_info.get("address"))
        )
        
        # 2. Build line items with Zoho item IDs (uses CACHE - no API calls!)
        line_items = []
        for cart_item in cart_items:
            # Look up item in cache
            zoho_item = await get_item_by_sku(cart_item["sku"])
            
            if not zoho_item:
                return {
                    "success": False,
                    "error": f"Product not found: {cart_item['sku']}"
                }
            
            line_items.append({
                "item_id": zoho_item["item_id"],
                "quantity": cart_item["quantity"],
                "rate": cart_item["price"],  # Use cart price (retail)
                "name": zoho_item.get("name", cart_item["sku"])
            })
        
        # 3. Create sales order (uses Zoho API - necessary for orders)
        shipping_names = {
            "standard": "Royal Mail 2nd Class",
            "express": "Royal Mail 1st Class / UPS"
        }
        
        notes = f"Online order via Home & Verse website"
        if payment_intent_id:
            notes += f"\nStripe Payment: {payment_intent_id}"
        
        result = await create_sales_order(
            customer_id=customer_id,
            line_items=line_items,
            shipping_charge=shipping_charge,
            shipping_method=shipping_names.get(shipping_method, shipping_method),
            notes=notes,
            reference_number=payment_intent_id
        )
        
        if result["success"]:
            result["customer_id"] = customer_id
            result["customer_name"] = customer.get("contact_name")
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Test function
async def test_connection():
    """Test Zoho connection and cache status"""
    try:
        # Test cache
        items = _get_cached_items()
        cache_status = f"Cache: {len(items)} items" if items else "Cache: Not available"
        
        # Test Zoho connection
        token = await get_access_token()
        response = await zoho_request("GET", "organizations")
        
        if response.status_code == 200:
            data = response.json()
            orgs = data.get("organizations", [])
            if orgs:
                return {
                    "success": True,
                    "organization": orgs[0].get("name"),
                    "org_id": orgs[0].get("organization_id"),
                    "cache_status": cache_status
                }
        
        return {"success": False, "error": "No organizations found", "cache_status": cache_status}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
