"""
Simple Analytics for Home & Verse
=================================
Tracks page views and visitors. Stores data in JSON files.
Uses IP hashing for privacy (no raw IPs stored).
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict

DATA_DIR = Path("data")
ANALYTICS_FILE = DATA_DIR / "analytics.json"
PAGEVIEWS_FILE = DATA_DIR / "pageviews.json"

# In-memory buffer to reduce disk writes
_pageview_buffer = []
_BUFFER_SIZE = 10  # Write to disk every 10 page views


def _hash_ip(ip: str) -> str:
    """Hash IP address for privacy - creates a daily-rotating hash"""
    # Include date so the same IP gets different hashes on different days
    daily_salt = datetime.utcnow().strftime("%Y-%m-%d")
    return hashlib.sha256(f"{ip}:{daily_salt}".encode()).hexdigest()[:16]


def _load_analytics() -> dict:
    """Load analytics data from file"""
    if not ANALYTICS_FILE.exists():
        return {
            "daily": {},  # date -> {visitors: set, pageviews: int}
            "pages": {},  # page_path -> view_count
            "updated_at": None
        }
    try:
        with open(ANALYTICS_FILE) as f:
            return json.load(f)
    except:
        return {"daily": {}, "pages": {}, "updated_at": None}


def _save_analytics(data: dict):
    """Save analytics data to file"""
    DATA_DIR.mkdir(exist_ok=True)
    data["updated_at"] = datetime.utcnow().isoformat()
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2, default=list)


def track_pageview(page_path: str, ip_address: str, user_agent: Optional[str] = None):
    """
    Track a page view.
    
    Args:
        page_path: The URL path (e.g., "/", "/product/12345")
        ip_address: Visitor's IP address (will be hashed)
        user_agent: Browser user agent string (for filtering bots)
    """
    global _pageview_buffer
    
    # Filter out obvious bots
    if user_agent:
        ua_lower = user_agent.lower()
        bot_indicators = ['bot', 'crawler', 'spider', 'slurp', 'facebook', 'twitter', 'linkedin']
        if any(bot in ua_lower for bot in bot_indicators):
            return
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    visitor_hash = _hash_ip(ip_address)
    
    # Normalize page path
    if not page_path or page_path == "":
        page_path = "/"
    
    # Clean up product URLs for aggregation
    if page_path.startswith("/product/"):
        # Keep product SKU for tracking popular products
        pass
    elif "?" in page_path:
        # Remove query params for cleaner grouping
        page_path = page_path.split("?")[0]
    
    _pageview_buffer.append({
        "date": today,
        "visitor": visitor_hash,
        "page": page_path,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Flush buffer if it's full
    if len(_pageview_buffer) >= _BUFFER_SIZE:
        _flush_buffer()


def _flush_buffer():
    """Write buffered pageviews to disk"""
    global _pageview_buffer
    
    if not _pageview_buffer:
        return
    
    data = _load_analytics()
    
    for pv in _pageview_buffer:
        date = pv["date"]
        visitor = pv["visitor"]
        page = pv["page"]
        
        # Initialize date if needed
        if date not in data["daily"]:
            data["daily"][date] = {"visitors": [], "pageviews": 0}
        
        # Track unique visitor
        if visitor not in data["daily"][date]["visitors"]:
            data["daily"][date]["visitors"].append(visitor)
        
        # Track pageview
        data["daily"][date]["pageviews"] = data["daily"][date].get("pageviews", 0) + 1
        
        # Track page popularity
        if page not in data["pages"]:
            data["pages"][page] = 0
        data["pages"][page] += 1
    
    _save_analytics(data)
    _pageview_buffer = []


def get_analytics_summary(days: int = 7) -> dict:
    """
    Get analytics summary for the admin dashboard.
    
    Args:
        days: Number of days to include
        
    Returns:
        Dictionary with visitor counts, pageview counts, and top pages
    """
    # Flush any pending pageviews
    _flush_buffer()
    
    data = _load_analytics()
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    total_visitors = set()
    total_pageviews = 0
    daily_stats = []
    
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        day_data = data["daily"].get(date_str, {"visitors": [], "pageviews": 0})
        
        visitors = day_data.get("visitors", [])
        pageviews = day_data.get("pageviews", 0)
        
        total_visitors.update(visitors)
        total_pageviews += pageviews
        
        daily_stats.append({
            "date": date_str,
            "day": current.strftime("%a"),
            "visitors": len(visitors),
            "pageviews": pageviews
        })
        
        current += timedelta(days=1)
    
    # Get top pages
    all_pages = data.get("pages", {})
    top_pages = sorted(all_pages.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Format top pages with readable names
    formatted_pages = []
    for path, views in top_pages:
        name = path
        if path == "/":
            name = "Home"
        elif path.startswith("/product/"):
            sku = path.replace("/product/", "")
            name = f"Product: {sku}"
        elif path.startswith("/?brand="):
            brand = path.replace("/?brand=", "")
            name = f"Brand: {brand}"
        elif path.startswith("/?category="):
            category = path.replace("/?category=", "")
            name = f"Category: {category}"
        else:
            # Clean up path
            name = path.strip("/").replace("-", " ").title() or "Home"
        
        formatted_pages.append({
            "path": path,
            "name": name,
            "views": views
        })
    
    # Calculate previous period for comparison
    prev_start = start_date - timedelta(days=days)
    prev_visitors = set()
    prev_pageviews = 0
    
    current = prev_start
    while current < start_date:
        date_str = current.strftime("%Y-%m-%d")
        day_data = data["daily"].get(date_str, {"visitors": [], "pageviews": 0})
        prev_visitors.update(day_data.get("visitors", []))
        prev_pageviews += day_data.get("pageviews", 0)
        current += timedelta(days=1)
    
    # Calculate changes
    visitor_change = 0
    if len(prev_visitors) > 0:
        visitor_change = ((len(total_visitors) - len(prev_visitors)) / len(prev_visitors)) * 100
    
    pageview_change = 0
    if prev_pageviews > 0:
        pageview_change = ((total_pageviews - prev_pageviews) / prev_pageviews) * 100
    
    return {
        "period": f"Last {days} days",
        "visitors": {
            "value": len(total_visitors),
            "change": round(visitor_change, 1)
        },
        "pageviews": {
            "value": total_pageviews,
            "change": round(pageview_change, 1)
        },
        "daily": daily_stats[-7:],  # Last 7 days for chart
        "top_pages": formatted_pages,
        "updated_at": data.get("updated_at")
    }


def cleanup_old_data(keep_days: int = 90):
    """Remove analytics data older than keep_days"""
    data = _load_analytics()
    
    cutoff = (datetime.utcnow() - timedelta(days=keep_days)).strftime("%Y-%m-%d")
    
    # Remove old daily data
    old_dates = [d for d in data["daily"].keys() if d < cutoff]
    for date in old_dates:
        del data["daily"][date]
    
    _save_analytics(data)
    
    return {"removed_dates": len(old_dates)}
