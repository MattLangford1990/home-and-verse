"""
Home & Verse - Backend API
===========================
Serves products from local JSON files (fast, no API calls for browsing).
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
import stripe
from pathlib import Path
from dotenv import load_dotenv


# Cache control middleware
class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        path = request.url.path
        
        # Vite assets have hashed filenames - cache forever
        if path.startswith('/assets/'):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        # Product images - cache for 1 day
        elif path.startswith('/images/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'
        # Static files (icons, manifest) - cache for 1 hour
        elif any(path.endswith(ext) for ext in ['.png', '.ico', '.svg', '.json', '.xml', '.txt']):
            response.headers['Cache-Control'] = 'public, max-age=3600'
        # HTML - no cache
        elif path == '/' or path.endswith('.html'):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        return response

# Load environment variables
load_dotenv()

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Project root (parent of backend/)
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = Path("data")
STATIC_DIR = Path("static")
PRODUCTS_FILE = DATA_DIR / "products.json"
STOCK_FILE = DATA_DIR / "stock.json"
RANKINGS_FILE = DATA_DIR / "rankings.json"
BESTSELLERS_FILE = DATA_DIR / "bestsellers.json"

app = FastAPI(title="Home & Verse API", version="1.0")

# Add cache control middleware
app.add_middleware(CacheControlMiddleware)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve product images
if (DATA_DIR / "images").exists():
    app.mount("/images", StaticFiles(directory=DATA_DIR / "images"), name="images")

# Serve Vite dist folder (frontend)
DIST_DIR = Path(__file__).parent.parent / "dist"
PUBLIC_DIR = Path(__file__).parent.parent / "public"

# Mount Vite assets folder
if (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

# Serve static files from public folder and dist
@app.get("/manifest.json")
async def get_manifest():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "manifest.json").exists():
            return FileResponse(dir / "manifest.json", media_type="application/manifest+json")
    raise HTTPException(status_code=404)

@app.get("/sw.js")
async def get_service_worker():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "sw.js").exists():
            return FileResponse(dir / "sw.js", media_type="application/javascript")
    raise HTTPException(status_code=404)

@app.get("/favicon.svg")
async def get_favicon_svg():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "favicon.svg").exists():
            return FileResponse(dir / "favicon.svg", media_type="image/svg+xml")
    raise HTTPException(status_code=404)

@app.get("/icon-192.png")
async def get_icon_192():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "icon-192.png").exists():
            return FileResponse(dir / "icon-192.png", media_type="image/png")
    raise HTTPException(status_code=404)

@app.get("/icon-512.png")
async def get_icon_512():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "icon-512.png").exists():
            return FileResponse(dir / "icon-512.png", media_type="image/png")
    raise HTTPException(status_code=404)

@app.get("/og-image.png")
async def get_og_image():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "og-image.png").exists():
            return FileResponse(dir / "og-image.png", media_type="image/png")
    raise HTTPException(status_code=404)

@app.get("/logo.png")
async def get_logo():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "logo.png").exists():
            return FileResponse(dir / "logo.png", media_type="image/png")
    raise HTTPException(status_code=404)

@app.get("/robots.txt")
async def get_robots():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "robots.txt").exists():
            return FileResponse(dir / "robots.txt", media_type="text/plain")
    raise HTTPException(status_code=404)

@app.get("/sitemap.xml")
async def get_sitemap():
    for dir in [DIST_DIR, PUBLIC_DIR]:
        if (dir / "sitemap.xml").exists():
            return FileResponse(dir / "sitemap.xml", media_type="application/xml")
    raise HTTPException(status_code=404)


def load_products() -> list[dict]:
    """Load products from local JSON file"""
    if not PRODUCTS_FILE.exists():
        return []
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return data.get("products", [])


def load_stock() -> dict:
    """Load stock levels from local JSON file"""
    if not STOCK_FILE.exists():
        return {}
    with open(STOCK_FILE) as f:
        data = json.load(f)
    return data.get("stock", {})


def load_rankings() -> dict:
    """Load popularity rankings from local JSON file"""
    if not RANKINGS_FILE.exists():
        return {}
    with open(RANKINGS_FILE) as f:
        data = json.load(f)
    return data.get("rankings", {})


def load_bestsellers() -> dict:
    """Load bestsellers from local JSON file"""
    if not BESTSELLERS_FILE.exists():
        return {"bestsellers": [], "generated_at": None}
    with open(BESTSELLERS_FILE) as f:
        return json.load(f)


@app.get("/")
async def serve_frontend():
    """Serve the main frontend from Vite dist"""
    # Try dist/index.html first (production build)
    dist_html = PROJECT_ROOT / "dist" / "index.html"
    if dist_html.exists():
        return FileResponse(dist_html, media_type="text/html")
    # Fallback to preview.html for legacy
    preview_html = PROJECT_ROOT / "preview.html"
    if preview_html.exists():
        return FileResponse(preview_html, media_type="text/html")
    return {"status": "ok", "service": "Home & Verse API", "note": "No frontend found - run npm run build"}





@app.get("/api/products")
async def get_products(
    brand: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    in_stock_only: bool = False,
    with_images_only: bool = True,  # Default to only showing products with images
    sort: Optional[str] = None  # popularity, price-asc, price-desc, name
):
    """Get all products with optional filtering"""
    products = load_products()
    rankings = load_rankings()
    
    # Filter out products without images (default behavior)
    if with_images_only:
        products = [p for p in products if p.get("has_image", False)]
    
    if brand:
        products = [p for p in products if p.get("brand", "").lower() == brand.lower()]
    
    if category:
        # Support both old single category and new categories array
        products = [
            p for p in products 
            if category.lower() in [c.lower() for c in p.get("categories", [p.get("category", "")])] 
        ]
    
    if search:
        search_lower = search.lower()
        products = [
            p for p in products
            if search_lower in p.get("name", "").lower()
            or search_lower in p.get("description", "").lower()
            or search_lower in p.get("sku", "").lower()
        ]
    
    if in_stock_only:
        products = [p for p in products if p.get("in_stock", False)]
    
    # Add popularity score to each product
    for product in products:
        sku = product.get("sku", "")
        if sku in rankings:
            product["popularity_score"] = rankings[sku].get("score", 50)
        else:
            product["popularity_score"] = 50  # Default score
    
    # Apply sorting
    if sort == "popularity":
        # For Christmas category, interleave by keyword for variety
        if category and category.lower() == "christmas":
            keyword_groups = {
                'light': [], 'house': [], 'santa': [], 'christmas': [],
                'candle': [], 'star': [], 'angel': [], 'tree': [], 'other': []
            }
            
            for p in products:
                name = (p.get('name') or '').lower()
                placed = False
                for keyword in ['light', 'house', 'santa', 'christmas', 'candle', 'star', 'angel', 'tree']:
                    if keyword in name and not placed:
                        keyword_groups[keyword].append(p)
                        placed = True
                        break
                if not placed:
                    keyword_groups['other'].append(p)
            
            # Sort each group by popularity
            for key in keyword_groups:
                keyword_groups[key].sort(key=lambda p: -p.get('popularity_score', 50))
            
            # Interleave for variety
            result = []
            group_keys = ['light', 'house', 'santa', 'christmas', 'candle', 'star', 'angel', 'tree', 'other']
            max_len = max(len(keyword_groups[k]) for k in group_keys) if keyword_groups else 0
            
            for i in range(max_len):
                for key in group_keys:
                    if i < len(keyword_groups[key]):
                        result.append(keyword_groups[key][i])
            
            products = result
        else:
            products.sort(key=lambda p: -p.get("popularity_score", 50))
    elif sort == "price-asc":
        products.sort(key=lambda p: p.get("price", 0))
    elif sort == "price-desc":
        products.sort(key=lambda p: -p.get("price", 0))
    elif sort == "name":
        products.sort(key=lambda p: p.get("name", "").lower())
    # Default sort (no sort param): by popularity for categories, by name otherwise
    elif category:
        if category.lower() == "christmas":
            # Same interleaved variety sort as above
            keyword_groups = {
                'light': [], 'house': [], 'santa': [], 'christmas': [],
                'candle': [], 'star': [], 'angel': [], 'tree': [], 'other': []
            }
            
            for p in products:
                name = (p.get('name') or '').lower()
                placed = False
                for keyword in ['light', 'house', 'santa', 'christmas', 'candle', 'star', 'angel', 'tree']:
                    if keyword in name and not placed:
                        keyword_groups[keyword].append(p)
                        placed = True
                        break
                if not placed:
                    keyword_groups['other'].append(p)
            
            for key in keyword_groups:
                keyword_groups[key].sort(key=lambda p: -p.get('popularity_score', 50))
            
            result = []
            group_keys = ['light', 'house', 'santa', 'christmas', 'candle', 'star', 'angel', 'tree', 'other']
            max_len = max(len(keyword_groups[k]) for k in group_keys) if keyword_groups else 0
            
            for i in range(max_len):
                for key in group_keys:
                    if i < len(keyword_groups[key]):
                        result.append(keyword_groups[key][i])
            
            products = result
        else:
            products.sort(key=lambda p: -p.get("popularity_score", 50))
    
    return {"products": products, "count": len(products)}


@app.get("/api/products/{sku}")
async def get_product(sku: str):
    """Get single product by SKU"""
    products = load_products()
    rankings = load_rankings()
    
    for product in products:
        if product.get("sku") == sku:
            # Add popularity score
            if sku in rankings:
                product["popularity_score"] = rankings[sku].get("score", 50)
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/api/brands")
async def get_brands():
    """Get list of available brands with counts (only products with images)"""
    products = load_products()
    # Only count products with images
    products = [p for p in products if p.get("has_image", False)]
    
    brand_counts = {}
    for product in products:
        brand = product.get("brand", "Other")
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    return {
        "brands": [
            {"name": brand, "count": count}
            for brand, count in sorted(brand_counts.items())
        ]
    }


@app.get("/api/categories")
async def get_categories():
    """Get list of available categories with counts (only products with images)"""
    products = load_products()
    # Only count products with images
    products = [p for p in products if p.get("has_image", False)]
    
    category_counts = {}
    for product in products:
        cats = product.get("categories", [product.get("category", "Other")])
        for category in cats:
            category_counts[category] = category_counts.get(category, 0) + 1
    
    return {
        "categories": [
            {"name": cat, "count": count}
            for cat, count in sorted(category_counts.items())
        ],
        "total_products": len(products)
    }


@app.get("/api/stats")
async def get_stats():
    """Get basic stats"""
    products = load_products()
    
    in_stock = sum(1 for p in products if p.get("in_stock", False))
    with_images = sum(1 for p in products if p.get("has_image", False))
    multi_category = sum(1 for p in products if len(p.get("categories", [])) > 1)
    
    brands = {}
    categories = {}
    for p in products:
        # Only count products with images
        if not p.get("has_image", False):
            continue
        brands[p.get("brand", "Other")] = brands.get(p.get("brand", "Other"), 0) + 1
        for cat in p.get("categories", [p.get("category", "Other")]):
            categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_products": len(products),
        "displayable_products": with_images,
        "in_stock": in_stock,
        "out_of_stock": len(products) - in_stock,
        "with_images": with_images,
        "without_images": len(products) - with_images,
        "multi_category_products": multi_category,
        "brands": brands,
        "categories": categories
    }


@app.get("/api/rankings/info")
async def get_rankings_info():
    """Get info about current rankings"""
    if not RANKINGS_FILE.exists():
        return {"status": "not_generated", "message": "Run update_rankings.py to generate"}
    
    with open(RANKINGS_FILE) as f:
        data = json.load(f)
    
    return {
        "status": "ok",
        "generated_at": data.get("generated_at"),
        "product_count": data.get("product_count"),
        "algorithm_version": data.get("algorithm_version"),
        "notes": data.get("notes")
    }


@app.get("/api/bestsellers")
async def get_bestsellers(limit: int = 50, in_stock_only: bool = True):
    """Get best selling products based on last 3 months sales"""
    data = load_bestsellers()
    bestsellers = data.get("bestsellers", [])
    
    # Filter by stock if requested
    if in_stock_only:
        bestsellers = [b for b in bestsellers if b.get("in_stock", False)]
    
    # Apply limit
    bestsellers = bestsellers[:limit]
    
    return {
        "bestsellers": bestsellers,
        "count": len(bestsellers),
        "generated_at": data.get("generated_at"),
        "date_range": data.get("date_range")
    }


@app.get("/health")
async def health_check():
    """Health check"""
    products = load_products()
    with_images = sum(1 for p in products if p.get("has_image", False))
    return {
        "status": "healthy",
        "products_loaded": len(products),
        "displayable": with_images
    }


# Shipping configuration
SHIPPING_OPTIONS = {
    "standard": {
        "name": "Royal Mail 2nd Class",
        "description": "3-5 working days",
        "price": 4.99,
        "free_threshold": 30.00  # Free over £30
    },
    "express": {
        "name": "Royal Mail / UPS 1st Class",
        "description": "1-2 working days",
        "price": 7.99,
        "free_threshold": 30.00  # Free over £30
    }
}


class ShippingRequest(BaseModel):
    order_total: float


@app.get("/api/shipping")
async def get_shipping_options(order_total: float = 0):
    """Get available shipping options based on order total"""
    options = []
    
    for key, option in SHIPPING_OPTIONS.items():
        shipping_cost = 0 if order_total >= option["free_threshold"] else option["price"]
        options.append({
            "id": key,
            "name": option["name"],
            "description": option["description"],
            "price": shipping_cost,
            "free_threshold": option["free_threshold"],
            "is_free": shipping_cost == 0
        })
    
    return {
        "options": options,
        "order_total": order_total,
        "free_shipping_message": f"Free standard shipping on orders over £{SHIPPING_OPTIONS['standard']['free_threshold']:.0f}"
    }


# ==========================================
# CHECKOUT & ORDER ENDPOINTS
# ==========================================

from zoho_orders import create_order_from_cart, test_connection as zoho_test


class CartItem(BaseModel):
    sku: str
    quantity: int
    price: float
    name: str


class Address(BaseModel):
    address: str
    city: str
    state: str = ""
    zip: str
    country: str = "United Kingdom"


class CustomerInfo(BaseModel):
    email: str
    name: str
    phone: str = ""
    address: Address
    shipping_address: Optional[Address] = None


class CheckoutRequest(BaseModel):
    items: List[CartItem]
    customer: CustomerInfo
    shipping_method: str = "standard"
    payment_intent_id: Optional[str] = None


class PaymentIntentRequest(BaseModel):
    amount: int  # Amount in pence
    currency: str = "gbp"


@app.get("/api/zoho/test")
async def test_zoho_connection():
    """Test Zoho API connection"""
    result = await zoho_test()
    return result


@app.post("/api/checkout/create-payment-intent")
async def create_payment_intent(request: PaymentIntentRequest):
    """Create Stripe payment intent"""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency=request.currency,
            automatic_payment_methods={"enabled": True},
            metadata={"source": "home_and_verse"}
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/checkout/place-order")
async def place_order(request: CheckoutRequest):
    """
    Place an order:
    1. Validate cart items
    2. Calculate totals
    3. Create Sales Order in Zoho
    """
    
    # Validate items exist and get current prices
    products = load_products()
    product_map = {p["sku"]: p for p in products}
    
    validated_items = []
    subtotal = 0
    
    for item in request.items:
        product = product_map.get(item.sku)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product not found: {item.sku}")
        
        # Use current price from our system (not cart price for security)
        current_price = product.get("price", 0)
        
        validated_items.append({
            "sku": item.sku,
            "quantity": item.quantity,
            "price": current_price,
            "name": product.get("name", item.sku)
        })
        
        subtotal += current_price * item.quantity
    
    # Calculate shipping
    shipping_option = SHIPPING_OPTIONS.get(request.shipping_method, SHIPPING_OPTIONS["standard"])
    shipping_charge = 0 if subtotal >= shipping_option["free_threshold"] else shipping_option["price"]
    
    total = subtotal + shipping_charge
    
    # Create order in Zoho
    customer_data = {
        "email": request.customer.email,
        "name": request.customer.name,
        "phone": request.customer.phone,
        "address": request.customer.address.dict(),
        "shipping_address": request.customer.shipping_address.dict() if request.customer.shipping_address else None
    }
    
    result = await create_order_from_cart(
        cart_items=validated_items,
        customer_info=customer_data,
        shipping_method=request.shipping_method,
        shipping_charge=shipping_charge,
        payment_intent_id=request.payment_intent_id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to create order"))
    
    return {
        "success": True,
        "order_number": result.get("salesorder_number"),
        "order_id": result.get("salesorder_id"),
        "subtotal": subtotal,
        "shipping": shipping_charge,
        "total": total,
        "customer_email": request.customer.email
    }


@app.post("/api/checkout/test-order")
async def create_test_order():
    """
    Create a test order to verify Zoho integration.
    Uses a dummy product and test customer.
    """
    
    # Get a real product SKU
    products = load_products()
    test_product = None
    for p in products:
        if p.get("in_stock") and p.get("price", 0) > 0:
            test_product = p
            break
    
    if not test_product:
        raise HTTPException(status_code=400, detail="No in-stock products found for testing")
    
    # Create test order
    test_cart = [
        {
            "sku": test_product["sku"],
            "quantity": 1,
            "price": test_product["price"]
        }
    ]
    
    test_customer = {
        "email": "test@homeandverse.com",
        "name": "Test Order - DELETE ME",
        "phone": "07000000000",
        "address": {
            "address": "123 Test Street",
            "city": "London",
            "state": "Greater London",
            "zip": "SW1A 1AA",
            "country": "United Kingdom"
        }
    }
    
    result = await create_order_from_cart(
        cart_items=test_cart,
        customer_info=test_customer,
        shipping_method="standard",
        shipping_charge=4.99,
        payment_intent_id="TEST_ORDER_" + str(int(__import__("time").time()))
    )
    
    return {
        "test_order": True,
        "product_used": test_product["sku"],
        "product_name": test_product["name"],
        "result": result
    }
