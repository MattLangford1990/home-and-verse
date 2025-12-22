"""
Popularity Rankings Generator
=============================
Run this script to update product popularity scores.
Should be scheduled to run every 2 days via cron.

Cron example (runs at 3am every 2 days):
0 3 */2 * * cd /path/to/backend && python3 update_rankings.py

Current algorithm (mock - replace with real data):
- Base score from price proximity to category median
- Räder boost in Christmas category
- Stock availability boost
- Random variance for freshness

Future: Replace with real sales/view data from Zoho/analytics
"""

import json
import random
from pathlib import Path
from datetime import datetime
from statistics import median

DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"
RANKINGS_FILE = DATA_DIR / "rankings.json"

# Brand boosts by category (brand: {category: boost})
BRAND_CATEGORY_BOOSTS = {
    "Räder": {"Christmas": 50, "Home Décor": 20, "Gifts": 15},
    "GEFU": {"Kitchen": 30},
    "My Flame Lifestyle": {"Candles": 40, "Gifts": 20},
    "Relaxound": {"Home Décor": 25, "Gifts": 20},
}

# Target price points by category (products near these get boosted)
TARGET_PRICES = {
    "Christmas": 20,
    "Home Décor": 25,
    "Candles": 18,
    "Lighting": 30,
    "Gifts": 20,
    "Kitchen": 25,
}

DEFAULT_TARGET_PRICE = 20


def load_products():
    """Load products from JSON"""
    if not PRODUCTS_FILE.exists():
        return []
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return data.get("products", [])


def calculate_popularity_score(product, category_medians):
    """
    Calculate popularity score for a product.
    
    Factors:
    - Price proximity to target (closer = higher score)
    - Brand boost for specific categories
    - Stock availability
    - Random variance (5-15 points)
    
    Returns score 0-100
    """
    score = 50  # Base score
    
    price = product.get("price", 0)
    categories = product.get("categories", [product.get("category", "Other")])
    brand = product.get("brand", "")
    in_stock = product.get("in_stock", False)
    has_image = product.get("has_image", False)
    
    # No image = no ranking (won't be shown anyway)
    if not has_image:
        return 0
    
    # Stock boost
    if in_stock:
        score += 10
    else:
        score -= 20
    
    # Price proximity score for each category
    price_scores = []
    for cat in categories:
        target = TARGET_PRICES.get(cat, DEFAULT_TARGET_PRICE)
        # Score based on how close to target price (max 20 points)
        price_diff = abs(price - target)
        if price_diff <= 5:
            price_scores.append(20)
        elif price_diff <= 10:
            price_scores.append(15)
        elif price_diff <= 20:
            price_scores.append(10)
        elif price_diff <= 40:
            price_scores.append(5)
        else:
            price_scores.append(0)
    
    if price_scores:
        score += max(price_scores)
    
    # Brand category boosts
    if brand in BRAND_CATEGORY_BOOSTS:
        for cat in categories:
            boost = BRAND_CATEGORY_BOOSTS[brand].get(cat, 0)
            score += boost
    
    # Random variance for freshness (so rankings aren't static)
    score += random.randint(5, 15)
    
    # Clamp to 0-100
    return max(0, min(100, score))


def generate_rankings():
    """Generate popularity rankings for all products"""
    products = load_products()
    
    if not products:
        print("No products found")
        return
    
    # Calculate category medians (for reference)
    category_prices = {}
    for p in products:
        for cat in p.get("categories", [p.get("category", "Other")]):
            if cat not in category_prices:
                category_prices[cat] = []
            category_prices[cat].append(p.get("price", 0))
    
    category_medians = {
        cat: median(prices) if prices else 20
        for cat, prices in category_prices.items()
    }
    
    # Calculate scores
    rankings = {}
    for product in products:
        sku = product.get("sku")
        if sku:
            score = calculate_popularity_score(product, category_medians)
            rankings[sku] = {
                "score": score,
                "brand": product.get("brand", ""),
                "price": product.get("price", 0),
            }
    
    # Save rankings
    output = {
        "rankings": rankings,
        "generated_at": datetime.now().isoformat(),
        "product_count": len(rankings),
        "category_medians": category_medians,
        "algorithm_version": "1.0-mock",
        "notes": "Mock rankings based on price proximity and brand boosts. Replace with real sales data."
    }
    
    with open(RANKINGS_FILE, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated rankings for {len(rankings)} products")
    print(f"Saved to {RANKINGS_FILE}")
    
    # Show top 10 overall
    top_10 = sorted(rankings.items(), key=lambda x: x[1]["score"], reverse=True)[:10]
    print("\nTop 10 products:")
    for sku, data in top_10:
        print(f"  {sku}: {data['score']} ({data['brand']} - £{data['price']})")


if __name__ == "__main__":
    generate_rankings()
