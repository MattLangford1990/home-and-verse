"""
Zoho Inventory Integration for Orders
======================================
Creates Sales Orders, manages customers, and syncs with Zoho.
"""

import httpx
import os
from datetime import datetime
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
        # Note: Custom fields removed - add back if configured in Zoho
        # "custom_fields": [{"label": "Sales Channel", "value": "Home & Verse Website"}]
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


async def get_item_by_sku(sku: str):
    """Get item details from Zoho by SKU"""
    response = await zoho_request("GET", "items", params={"sku": sku})
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if items:
            return items[0]
    
    return None


async def create_order_from_cart(cart_items: list, customer_info: dict, 
                                  shipping_method: str = "standard",
                                  shipping_charge: float = 0,
                                  payment_intent_id: str = None):
    """
    Full order creation flow:
    1. Find or create customer
    2. Look up item IDs from SKUs
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
        # 1. Find or create customer
        customer_id, customer = await find_or_create_customer(
            email=customer_info["email"],
            name=customer_info["name"],
            phone=customer_info.get("phone"),
            billing_address=customer_info.get("address"),
            shipping_address=customer_info.get("shipping_address", customer_info.get("address"))
        )
        
        # 2. Build line items with Zoho item IDs
        line_items = []
        for cart_item in cart_items:
            # Look up item in Zoho
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
        
        # 3. Create sales order
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
    """Test Zoho connection"""
    try:
        token = await get_access_token()
        response = await zoho_request("GET", "organizations")
        
        if response.status_code == 200:
            data = response.json()
            orgs = data.get("organizations", [])
            if orgs:
                return {
                    "success": True,
                    "organization": orgs[0].get("name"),
                    "org_id": orgs[0].get("organization_id")
                }
        
        return {"success": False, "error": "No organizations found"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
