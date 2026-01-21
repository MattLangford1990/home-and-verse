"""
Admin Dashboard Routes for Home & Verse
========================================
Provides statistics and order management endpoints.
Tracks only website orders (not trade Stripe payments).
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from pathlib import Path
import json
import os

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Simple admin auth - in production use proper auth
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "hv-admin-2024")

# Orders storage
DATA_DIR = Path(__file__).parent / "data"
ORDERS_FILE = DATA_DIR / "orders.json"


def verify_admin(secret: str) -> bool:
    """Simple admin verification"""
    return secret == ADMIN_SECRET


def load_orders() -> list:
    """Load orders from local JSON file"""
    if not ORDERS_FILE.exists():
        return []
    try:
        with open(ORDERS_FILE) as f:
            data = json.load(f)
        return data.get("orders", [])
    except Exception as e:
        print(f"Error loading orders: {e}")
        return []


def save_order(order: dict):
    """Save a new order to the orders file"""
    orders = load_orders()
    orders.append(order)
    
    # Keep orders file manageable - retain last 1000 orders
    if len(orders) > 1000:
        orders = orders[-1000:]
    
    DATA_DIR.mkdir(exist_ok=True)
    with open(ORDERS_FILE, "w") as f:
        json.dump({"orders": orders, "updated_at": datetime.utcnow().isoformat()}, f, indent=2)


@router.get("/stats")
async def get_admin_stats(secret: str, days: int = 7):
    """
    Get admin dashboard statistics from local orders.
    Only tracks orders placed through the website checkout.
    Requires admin secret for access.
    """
    if not verify_admin(secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        orders = load_orders()
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        previous_start = start_date - timedelta(days=days)
        
        # Filter orders by date
        current_orders = []
        previous_orders = []
        
        for order in orders:
            try:
                order_date = datetime.fromisoformat(order.get("created_at", "").replace("Z", "+00:00"))
                # Convert to naive datetime for comparison
                order_date = order_date.replace(tzinfo=None)
                
                if start_date <= order_date <= end_date:
                    current_orders.append(order)
                elif previous_start <= order_date < start_date:
                    previous_orders.append(order)
            except (ValueError, TypeError):
                continue
        
        # Calculate current period stats
        current_revenue = sum(order.get("total", 0) for order in current_orders)
        current_count = len(current_orders)
        
        # Calculate previous period stats
        previous_revenue = sum(order.get("total", 0) for order in previous_orders)
        previous_count = len(previous_orders)
        
        # Calculate changes
        revenue_change = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
        orders_change = ((current_count - previous_count) / previous_count * 100) if previous_count > 0 else 0
        
        avg_order = current_revenue / current_count if current_count > 0 else 0
        prev_avg_order = previous_revenue / previous_count if previous_count > 0 else 0
        avg_order_change = ((avg_order - prev_avg_order) / prev_avg_order * 100) if prev_avg_order > 0 else 0
        
        # Get recent orders (most recent first)
        sorted_current = sorted(current_orders, key=lambda x: x.get("created_at", ""), reverse=True)
        recent_orders = []
        for order in sorted_current[:10]:
            recent_orders.append({
                "id": order.get("order_number", order.get("zoho_order_id", "N/A")),
                "customer": order.get("customer_name", "Unknown"),
                "email": order.get("customer_email", "Unknown"),
                "total": order.get("total", 0),
                "status": order.get("status", "completed"),
                "date": order.get("created_at", "")[:16].replace("T", " "),
                "items": order.get("item_count", 1)
            })
        
        # Daily revenue for chart
        daily_revenue = {}
        for order in current_orders:
            try:
                order_date = datetime.fromisoformat(order.get("created_at", "").replace("Z", "+00:00"))
                day = order_date.strftime("%a")
                daily_revenue[day] = daily_revenue.get(day, 0) + order.get("total", 0)
            except (ValueError, TypeError):
                continue
        
        # Ensure all days of week are present
        days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        revenue_chart = [
            {"day": day, "value": round(daily_revenue.get(day, 0), 2)}
            for day in days_order
        ]
        
        return {
            "period": f"Last {days} days",
            "revenue": {
                "value": round(current_revenue, 2),
                "change": round(revenue_change, 1)
            },
            "orders": {
                "value": current_count,
                "change": round(orders_change, 1)
            },
            "avg_order": {
                "value": round(avg_order, 2),
                "change": round(avg_order_change, 1)
            },
            "recent_orders": recent_orders,
            "revenue_chart": revenue_chart
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading stats: {str(e)}")


@router.get("/analytics")
async def get_admin_analytics(secret: str, days: int = 7):
    """
    Get visitor analytics for the admin dashboard.
    Requires admin secret for access.
    """
    if not verify_admin(secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        from analytics import get_analytics_summary
        return get_analytics_summary(days)
    except Exception as e:
        # Return empty data if analytics not available
        return {
            "period": f"Last {days} days",
            "visitors": {"value": 0, "change": 0},
            "pageviews": {"value": 0, "change": 0},
            "daily": [],
            "top_pages": [],
            "error": str(e)
        }


@router.get("/orders")
async def get_admin_orders(secret: str, limit: int = 50, status: str = None):
    """Get list of orders from local storage"""
    if not verify_admin(secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        orders = load_orders()
        
        # Sort by date (newest first)
        orders = sorted(orders, key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Filter by status if specified
        if status:
            orders = [o for o in orders if o.get("status") == status]
        
        # Apply limit
        orders = orders[:limit]
        
        # Format for response
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                "id": order.get("order_number", order.get("zoho_order_id", "N/A")),
                "zoho_id": order.get("zoho_order_id"),
                "stripe_id": order.get("payment_intent_id"),
                "customer": order.get("customer_name", "Unknown"),
                "email": order.get("customer_email", "Unknown"),
                "total": order.get("total", 0),
                "status": order.get("status", "completed"),
                "date": order.get("created_at", "")[:16].replace("T", " "),
                "items": order.get("item_count", 1)
            })
        
        return {"orders": formatted_orders, "count": len(formatted_orders)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading orders: {str(e)}")
