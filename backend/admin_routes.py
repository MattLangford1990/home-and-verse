"""
Admin Dashboard Routes for Home & Verse
========================================
Provides statistics and order management endpoints.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import stripe
import os

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Simple admin auth - in production use proper auth
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "hv-admin-2024")


def verify_admin(secret: str) -> bool:
    """Simple admin verification"""
    return secret == ADMIN_SECRET


@router.get("/stats")
async def get_admin_stats(secret: str, days: int = 7):
    """
    Get admin dashboard statistics from Stripe.
    Requires admin secret for access.
    """
    if not verify_admin(secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        previous_start = start_date - timedelta(days=days)
        
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        previous_start_timestamp = int(previous_start.timestamp())
        
        # Get current period payments
        current_payments = stripe.PaymentIntent.list(
            created={"gte": start_timestamp, "lte": end_timestamp},
            limit=100
        )
        
        # Get previous period for comparison
        previous_payments = stripe.PaymentIntent.list(
            created={"gte": previous_start_timestamp, "lt": start_timestamp},
            limit=100
        )
        
        # Calculate current period stats
        current_revenue = sum(
            p.amount_received / 100 
            for p in current_payments.data 
            if p.status == "succeeded"
        )
        current_orders = sum(
            1 for p in current_payments.data 
            if p.status == "succeeded"
        )
        
        # Calculate previous period stats
        previous_revenue = sum(
            p.amount_received / 100 
            for p in previous_payments.data 
            if p.status == "succeeded"
        )
        previous_orders = sum(
            1 for p in previous_payments.data 
            if p.status == "succeeded"
        )
        
        # Calculate changes
        revenue_change = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
        orders_change = ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0
        
        avg_order = current_revenue / current_orders if current_orders > 0 else 0
        prev_avg_order = previous_revenue / previous_orders if previous_orders > 0 else 0
        avg_order_change = ((avg_order - prev_avg_order) / prev_avg_order * 100) if prev_avg_order > 0 else 0
        
        # Get recent orders with details
        recent_orders = []
        for payment in current_payments.data[:10]:
            if payment.status == "succeeded":
                customer_email = payment.receipt_email or "Unknown"
                customer_name = payment.metadata.get("customer_name", customer_email.split("@")[0].title())
                
                recent_orders.append({
                    "id": payment.metadata.get("order_number", payment.id[:12].upper()),
                    "customer": customer_name,
                    "email": customer_email,
                    "total": payment.amount_received / 100,
                    "status": "completed",
                    "date": datetime.fromtimestamp(payment.created).strftime("%Y-%m-%d %H:%M"),
                    "items": int(payment.metadata.get("item_count", 1))
                })
        
        # Daily revenue for chart
        daily_revenue = {}
        for payment in current_payments.data:
            if payment.status == "succeeded":
                day = datetime.fromtimestamp(payment.created).strftime("%a")
                daily_revenue[day] = daily_revenue.get(day, 0) + payment.amount_received / 100
        
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
                "value": current_orders,
                "change": round(orders_change, 1)
            },
            "avg_order": {
                "value": round(avg_order, 2),
                "change": round(avg_order_change, 1)
            },
            "recent_orders": recent_orders,
            "revenue_chart": revenue_chart
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")


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
    """Get list of orders from Stripe"""
    if not verify_admin(secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        payments = stripe.PaymentIntent.list(limit=limit)
        
        orders = []
        for payment in payments.data:
            order_status = "completed" if payment.status == "succeeded" else payment.status
            
            if status and order_status != status:
                continue
            
            customer_email = payment.receipt_email or "Unknown"
            customer_name = payment.metadata.get("customer_name", customer_email.split("@")[0].title())
            
            orders.append({
                "id": payment.metadata.get("order_number", payment.id[:12].upper()),
                "stripe_id": payment.id,
                "customer": customer_name,
                "email": customer_email,
                "total": payment.amount_received / 100 if payment.status == "succeeded" else payment.amount / 100,
                "status": order_status,
                "date": datetime.fromtimestamp(payment.created).strftime("%Y-%m-%d %H:%M"),
                "items": int(payment.metadata.get("item_count", 1))
            })
        
        return {"orders": orders, "count": len(orders)}
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
