"""
Pre-render routes for Google/crawler detection.
When a search engine crawler visits any page, they get real HTML content
instead of the empty React shell. Normal users still get the React SPA.
"""

from fastapi import Request
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"

CRAWLER_AGENTS = [
    "googlebot", "google-inspectiontool", "bingbot", "slurp", "duckduckbot",
    "baiduspider", "yandexbot", "facebookexternalhit", "twitterbot",
    "linkedinbot", "whatsapp", "telegrambot", "applebot", "ia_archiver",
    "ahrefsbot", "semrushbot", "mj12bot"
]


def is_crawler(request: Request) -> bool:
    ua = request.headers.get("user-agent", "").lower()
    return any(bot in ua for bot in CRAWLER_AGENTS)


def load_products_data():
    if not PRODUCTS_FILE.exists():
        return []
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return data.get("products", [])


def base_html(title: str, description: str, canonical: str, body_content: str, extra_schema: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://homeandverse.co.uk/og-image.png">
  <meta property="og:locale" content="en_GB">
  <meta property="og:site_name" content="Home &amp; Verse">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HomeGoodsStore",
    "name": "Home & Verse",
    "legalName": "DM Brands Ltd",
    "url": "https://homeandverse.co.uk",
    "logo": "https://homeandverse.co.uk/logo.png",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "79 Waterworks Road",
      "addressLocality": "Worcester",
      "postalCode": "WR1 3EZ",
      "addressCountry": "GB"
    }},
    "contactPoint": {{
      "@type": "ContactPoint",
      "telephone": "+441905616006",
      "email": "hello@homeandverse.co.uk",
      "contactType": "customer service"
    }}
  }}
  </script>
  {extra_schema}
  <style>
    body {{ font-family: Georgia, serif; margin: 0; padding: 0; color: #2c2c2c; background: #faf9f7; }}
    header {{ background: #2c2c2c; color: white; padding: 16px 32px; display: flex; align-items: center; justify-content: space-between; }}
    header a {{ color: white; text-decoration: none; font-size: 1.4em; letter-spacing: 2px; }}
    nav a {{ color: white; text-decoration: none; margin-left: 20px; font-size: 0.9em; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px; }}
    footer {{ background: #2c2c2c; color: #ccc; padding: 40px 32px; margin-top: 60px; font-size: 0.85em; }}
    footer a {{ color: #ccc; text-decoration: none; }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; max-width: 1200px; margin: 0 auto; }}
    h1 {{ font-size: 2em; font-weight: 300; margin-bottom: 8px; }}
    h2 {{ font-size: 1.4em; font-weight: 400; margin: 32px 0 16px; }}
    p {{ line-height: 1.7; }}
    .product-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 24px; margin-top: 32px; }}
    .product-card {{ background: white; border-radius: 4px; overflow: hidden; text-decoration: none; color: inherit; display: block; }}
    .product-card img {{ width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }}
    .product-card .info {{ padding: 12px; }}
    .product-card .name {{ font-size: 0.9em; margin: 0 0 4px; }}
    .product-card .brand {{ font-size: 0.8em; color: #777; margin: 0; }}
    .product-card .price {{ font-size: 1em; font-weight: 600; margin: 4px 0 0; }}
    .product-detail {{ display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: start; }}
    .product-detail img {{ width: 100%; border-radius: 4px; }}
    .breadcrumb {{ font-size: 0.85em; color: #777; margin-bottom: 24px; }}
    .breadcrumb a {{ color: #777; text-decoration: none; }}
    .price-large {{ font-size: 1.8em; font-weight: 300; margin: 16px 0; }}
    .brand-tag {{ display: inline-block; background: #f0ede8; padding: 4px 12px; border-radius: 2px; font-size: 0.8em; margin-bottom: 12px; }}
    .in-stock {{ color: #4a7c59; font-size: 0.9em; }}
    .out-stock {{ color: #c0392b; font-size: 0.9em; }}
    .cta-btn {{ display: inline-block; background: #2c2c2c; color: white; padding: 14px 32px; text-decoration: none; font-size: 0.95em; letter-spacing: 1px; margin-top: 16px; cursor: pointer; border: none; width: 100%; text-align: center; }}
    .brands-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; margin-top: 24px; }}
    .brand-card {{ background: white; padding: 24px; text-align: center; text-decoration: none; color: #2c2c2c; border-radius: 4px; }}
    .trust-badges {{ display: flex; gap: 24px; flex-wrap: wrap; margin: 40px 0; padding: 24px; background: white; border-radius: 4px; }}
    .trust-badge {{ display: flex; align-items: center; gap: 8px; font-size: 0.9em; }}
  </style>
</head>
<body>
  <header>
    <a href="/">HOME &amp; VERSE</a>
    <nav>
      <a href="/shop">Shop All</a>
      <a href="/brands">Brands</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>
  {body_content}
  <footer>
    <div class="footer-grid">
      <div>
        <strong style="color:white">Home &amp; Verse</strong>
        <p>Luxury European homeware, officially distributed in the UK by DM Brands Ltd.</p>
        <p>79 Waterworks Road, Worcester, WR1 3EZ<br>
        Tel: 01905 616006<br>
        Email: <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a></p>
        <p>Company No: 05706441 | VAT: GB 874 5395 38</p>
      </div>
      <div>
        <strong style="color:white">Our Brands</strong>
        <p><a href="/brands/rader">Räder</a><br>
        <a href="/brands/remember">Remember</a><br>
        <a href="/brands/elvang">Elvang Denmark</a><br>
        <a href="/brands/relaxound">Relaxound</a><br>
        <a href="/brands/my-flame">My Flame Lifestyle</a><br>
        <a href="/brands/ideas4seasons">Ideas4Seasons</a></p>
      </div>
      <div>
        <strong style="color:white">Customer Service</strong>
        <p><a href="/shipping">Delivery &amp; Shipping</a><br>
        <a href="/returns">Returns &amp; Refunds</a><br>
        <a href="/contact">Contact Us</a><br>
        <a href="/faq">FAQs</a></p>
        <strong style="color:white;display:block;margin-top:16px">Legal</strong>
        <p><a href="/privacy">Privacy Policy</a><br>
        <a href="/terms">Terms &amp; Conditions</a><br>
        <a href="/cookies">Cookie Policy</a></p>
      </div>
    </div>
    <p style="text-align:center;margin-top:32px;border-top:1px solid #444;padding-top:24px">&copy; 2025 DM Brands Ltd. All rights reserved. Registered in England &amp; Wales.</p>
  </footer>
</body>
</html>"""


def render_homepage() -> HTMLResponse:
    products = load_products_data()
    featured = [p for p in products if p.get("has_image") and p.get("in_stock")][:12]

    product_cards = ""
    for p in featured:
        img = f"https://cdn.appdmbrands.com{p['image_url']}" if p.get("image_url", "").startswith("/images/") else p.get("image_url", "")
        product_cards += f"""
        <a class="product-card" href="/product/{p['sku']}">
          <img src="{img}" alt="{p['name']}" loading="lazy">
          <div class="info">
            <p class="brand">{p.get('brand','')}</p>
            <p class="name">{p['name']}</p>
            <p class="price">£{p['price']:.2f}</p>
          </div>
        </a>"""

    body = f"""
    <div class="container">
      <h1>Luxury European Homeware</h1>
      <p style="font-size:1.1em;color:#666;max-width:600px">Beautiful homeware and gifts from Europe's finest brands — Räder, Remember, Elvang Denmark, Relaxound, My Flame Lifestyle and Ideas4Seasons. Official UK distributor.</p>

      <div class="trust-badges">
        <div class="trust-badge">🇬🇧 Official UK Distributor</div>
        <div class="trust-badge">🚚 Free Delivery Over £30</div>
        <div class="trust-badge">↩️ 30-Day Returns</div>
        <div class="trust-badge">🔒 Secure Checkout</div>
      </div>

      <h2>Featured Products</h2>
      <div class="product-grid">{product_cards}</div>

      <h2>Our Brands</h2>
      <div class="brands-grid">
        <a class="brand-card" href="/brands/rader"><strong>Räder</strong><br><small>German Porcelain &amp; Gifts</small></a>
        <a class="brand-card" href="/brands/remember"><strong>Remember</strong><br><small>German Design</small></a>
        <a class="brand-card" href="/brands/elvang"><strong>Elvang Denmark</strong><br><small>Danish Throws &amp; Textiles</small></a>
        <a class="brand-card" href="/brands/relaxound"><strong>Relaxound</strong><br><small>Nature Soundboxes</small></a>
        <a class="brand-card" href="/brands/my-flame"><strong>My Flame</strong><br><small>Dutch Lifestyle Candles</small></a>
        <a class="brand-card" href="/brands/ideas4seasons"><strong>Ideas4Seasons</strong><br><small>Seasonal Gifts</small></a>
      </div>
    </div>"""

    html = base_html(
        title="Home & Verse | Luxury European Homeware & Scandi Gifts UK",
        description="Shop luxury European homeware from Räder, Remember, My Flame, Relaxound, Ideas4Seasons & Elvang. German porcelain, Danish throws & Dutch candles. Free UK delivery over £30.",
        canonical="https://homeandverse.co.uk/",
        body_content=body
    )
    return HTMLResponse(content=html)


def render_product_page(sku: str):
    products = load_products_data()
    product = next((p for p in products if p.get("sku") == sku), None)
    if not product:
        return None

    img_url = product.get("image_url", "")
    if img_url.startswith("/images/"):
        img_url = f"https://cdn.appdmbrands.com{img_url}"

    stock_label = '<span class="in-stock">✓ In Stock</span>' if product.get("in_stock") else '<span class="out-stock">Currently Out of Stock</span>'
    cats = ", ".join(product.get("categories", [product.get("category", "")]))

    product_schema = f"""<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{product['name']}",
    "description": "{product.get('description','').replace('"', '&quot;')}",
    "sku": "{sku}",
    "brand": {{"@type": "Brand", "name": "{product.get('brand','')}"}},
    "offers": {{
      "@type": "Offer",
      "url": "https://homeandverse.co.uk/product/{sku}",
      "priceCurrency": "GBP",
      "price": "{product['price']:.2f}",
      "availability": "{'https://schema.org/InStock' if product.get('in_stock') else 'https://schema.org/OutOfStock'}",
      "seller": {{"@type": "Organization", "name": "Home & Verse"}}
    }},
    "image": "{img_url}"
  }}
  </script>"""

    body = f"""
    <div class="container">
      <p class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/shop">Shop</a> &rsaquo; {product['name']}</p>
      <div class="product-detail">
        <div>
          <img src="{img_url}" alt="{product['name']}">
        </div>
        <div>
          <span class="brand-tag">{product.get('brand','')}</span>
          <h1>{product['name']}</h1>
          <p style="color:#777;font-size:0.85em">SKU: {sku} | Category: {cats}</p>
          <div class="price-large">£{product['price']:.2f}</div>
          {stock_label}
          <p style="margin-top:16px;line-height:1.8">{product.get('description','')}</p>
          <a href="https://homeandverse.co.uk/?product={sku}" class="cta-btn">View &amp; Buy</a>
          <div class="trust-badges" style="margin-top:24px;padding:16px">
            <div class="trust-badge">🚚 Free delivery over £30</div>
            <div class="trust-badge">↩️ 30-day returns</div>
            <div class="trust-badge">🔒 Secure payment</div>
          </div>
        </div>
      </div>
    </div>"""

    html = base_html(
        title=f"{product['name']} | Home & Verse",
        description=f"Buy {product['name']} by {product.get('brand','')}. {product.get('description','')[:120]}. Free UK delivery over £30.",
        canonical=f"https://homeandverse.co.uk/product/{sku}",
        body_content=body,
        extra_schema=product_schema
    )
    return HTMLResponse(content=html)


def render_shop_page() -> HTMLResponse:
    products = load_products_data()
    visible = [p for p in products if p.get("has_image")]

    product_cards = ""
    for p in visible[:60]:
        img = f"https://cdn.appdmbrands.com{p['image_url']}" if p.get("image_url", "").startswith("/images/") else p.get("image_url", "")
        product_cards += f"""
        <a class="product-card" href="/product/{p['sku']}">
          <img src="{img}" alt="{p['name']}" loading="lazy">
          <div class="info">
            <p class="brand">{p.get('brand','')}</p>
            <p class="name">{p['name']}</p>
            <p class="price">£{p['price']:.2f}</p>
          </div>
        </a>"""

    body = f"""
    <div class="container">
      <h1>Shop All Homeware</h1>
      <p>Browse our full collection of luxury European homeware and gifts. {len(visible)} products available.</p>
      <div class="product-grid">{product_cards}</div>
    </div>"""

    html = base_html(
        title="Shop All | Home & Verse | Luxury European Homeware",
        description=f"Browse {len(visible)} luxury European homeware products from Räder, Remember, Elvang, Relaxound, My Flame and Ideas4Seasons. Free UK delivery over £30.",
        canonical="https://homeandverse.co.uk/shop",
        body_content=body
    )
    return HTMLResponse(content=html)


POLICY_PAGES = {
    "shipping": {
        "title": "Delivery & Shipping | Home & Verse",
        "description": "UK delivery information for Home & Verse. Free standard delivery on orders over £30. Next day and standard options available.",
        "h1": "Delivery & Shipping",
        "content": """
        <p>We deliver across the United Kingdom using Royal Mail and UPS.</p>
        <h2>Delivery Options</h2>
        <table style="width:100%;border-collapse:collapse;margin:16px 0">
          <tr style="background:#f0ede8"><th style="padding:12px;text-align:left">Service</th><th style="padding:12px;text-align:left">Estimated Delivery</th><th style="padding:12px;text-align:left">Cost</th></tr>
          <tr><td style="padding:12px;border-bottom:1px solid #eee">Standard (Royal Mail 2nd Class)</td><td style="padding:12px;border-bottom:1px solid #eee">3–5 working days</td><td style="padding:12px;border-bottom:1px solid #eee">£4.99 (FREE over £30)</td></tr>
          <tr><td style="padding:12px">Express (Royal Mail / UPS 1st Class)</td><td style="padding:12px">1–2 working days</td><td style="padding:12px">£7.99 (FREE over £30)</td></tr>
        </table>
        <h2>Free Delivery</h2>
        <p>Standard delivery is FREE on all orders over £30.</p>
        <h2>Order Processing</h2>
        <p>Orders placed before 2pm Monday–Friday are dispatched the same day. Orders placed after 2pm or on weekends are dispatched the next working day.</p>
        <h2>Delivery Address</h2>
        <p>We can deliver to any UK address including PO Boxes. We currently deliver to mainland UK only.</p>
        <h2>Tracking</h2>
        <p>You will receive a dispatch confirmation email with tracking information once your order has been sent.</p>
        """
    },
    "returns": {
        "title": "Returns & Refunds | Home & Verse",
        "description": "30-day returns policy for Home & Verse. We offer a full refund on all unused items returned within 30 days of purchase.",
        "h1": "Returns & Refunds",
        "content": """
        <p>We want you to be completely happy with your purchase. If you're not satisfied for any reason, we offer a straightforward returns policy.</p>
        <h2>Our Returns Policy</h2>
        <p>You have <strong>30 days</strong> from the date of delivery to return any item for a full refund. Items must be:</p>
        <ul style="line-height:2">
          <li>Unused and in their original condition</li>
          <li>In original packaging where possible</li>
          <li>Accompanied by your order number</li>
        </ul>
        <h2>How to Return</h2>
        <p>To initiate a return, please contact us at <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a> or call 01905 616006 with your order number and reason for return. We'll provide a return address and instructions.</p>
        <h2>Refunds</h2>
        <p>Refunds are processed within 5–10 working days of receiving the returned item, back to the original payment method.</p>
        <h2>Damaged or Faulty Items</h2>
        <p>If your item arrives damaged or faulty, please contact us within 48 hours with photos. We will arrange a replacement or full refund at no extra cost to you.</p>
        <h2>Contact</h2>
        <p>Email: <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a><br>
        Phone: 01905 616006<br>
        Address: 79 Waterworks Road, Worcester, WR1 3EZ</p>
        """
    },
    "contact": {
        "title": "Contact Us | Home & Verse",
        "description": "Contact Home & Verse. Call 01905 616006 or email hello@homeandverse.co.uk. Based in Worcester, UK.",
        "h1": "Contact Us",
        "content": """
        <p>We'd love to hear from you. Get in touch using any of the methods below.</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:32px">
          <div>
            <h2>Get in Touch</h2>
            <p><strong>Email:</strong> <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a></p>
            <p><strong>Phone:</strong> <a href="tel:+441905616006">01905 616006</a></p>
            <p><strong>Hours:</strong> Monday–Friday, 9am–5pm</p>
            <h2>Address</h2>
            <address style="font-style:normal;line-height:2">
              DM Brands Ltd<br>
              79 Waterworks Road<br>
              Worcester<br>
              WR1 3EZ<br>
              United Kingdom
            </address>
          </div>
          <div>
            <h2>About Us</h2>
            <p>Home &amp; Verse is operated by DM Brands Ltd, the official UK distributor for Räder, Remember, Elvang Denmark, Relaxound, My Flame Lifestyle and Ideas4Seasons.</p>
            <p>We are a UK-registered company (Company No: 05706441) based in Worcester, England.</p>
          </div>
        </div>
        """
    },
    "privacy": {
        "title": "Privacy Policy | Home & Verse",
        "description": "Privacy policy for Home & Verse, operated by DM Brands Ltd. How we collect, use and protect your personal data.",
        "h1": "Privacy Policy",
        "content": """
        <p><em>Last updated: January 2025</em></p>
        <p>Home &amp; Verse is operated by DM Brands Ltd (Company No: 05706441), 79 Waterworks Road, Worcester, WR1 3EZ. We are committed to protecting your personal data.</p>
        <h2>What Data We Collect</h2>
        <p>When you place an order, we collect your name, email address, delivery address, and phone number. We use this to process and deliver your order.</p>
        <h2>How We Use Your Data</h2>
        <p>Your data is used solely to fulfil your order and provide customer service. We do not sell your data to third parties.</p>
        <h2>Your Rights</h2>
        <p>You have the right to access, correct or delete your personal data. Contact us at <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a>.</p>
        <h2>Contact</h2>
        <p>DM Brands Ltd, 79 Waterworks Road, Worcester, WR1 3EZ. Email: <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a></p>
        """
    },
    "terms": {
        "title": "Terms & Conditions | Home & Verse",
        "description": "Terms and conditions for Home & Verse, operated by DM Brands Ltd. UK company registered in England and Wales.",
        "h1": "Terms & Conditions",
        "content": """
        <p><em>Last updated: January 2025</em></p>
        <p>These terms govern your use of homeandverse.co.uk, operated by DM Brands Ltd (Company No: 05706441), 79 Waterworks Road, Worcester, WR1 3EZ.</p>
        <h2>Orders</h2>
        <p>By placing an order you confirm you are over 18 and that all details provided are accurate. We reserve the right to refuse any order.</p>
        <h2>Pricing</h2>
        <p>All prices are in GBP and include VAT where applicable. We reserve the right to change prices at any time without notice.</p>
        <h2>Delivery</h2>
        <p>See our <a href="/shipping">Delivery & Shipping</a> page for full details.</p>
        <h2>Returns</h2>
        <p>See our <a href="/returns">Returns & Refunds</a> page for full details.</p>
        <h2>Governing Law</h2>
        <p>These terms are governed by the laws of England and Wales.</p>
        <h2>Contact</h2>
        <p>Email: <a href="mailto:hello@homeandverse.co.uk">hello@homeandverse.co.uk</a> | Tel: 01905 616006</p>
        """
    },
}


def render_policy_page(page_key: str):
    page = POLICY_PAGES.get(page_key)
    if not page:
        return None

    body = f"""
    <div class="container">
      <h1>{page['h1']}</h1>
      {page['content']}
    </div>"""

    html = base_html(
        title=page["title"],
        description=page["description"],
        canonical=f"https://homeandverse.co.uk/{page_key}",
        body_content=body
    )
    return HTMLResponse(content=html)
