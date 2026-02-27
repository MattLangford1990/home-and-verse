#!/usr/bin/env python3
"""
Home & Verse - Full Site Audit for Google Merchant Center Compliance
====================================================================
Checks EVERY page and EVERY product URL against Google's requirements.
Run from: cd ~/Desktop/home-and-verse && python3 audit_site.py
"""

import requests
import json
import csv
import re
import sys
import time
import xml.etree.ElementTree as ET
from io import StringIO
from urllib.parse import urlparse, parse_qs, quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# CONFIGURATION
# ============================================================
SITE_URL = "https://homeandverse.co.uk"
API_BASE = f"{SITE_URL}/api"
CDN_BASE = "https://cdn.appdmbrands.com"

# Expected business info (must match everywhere)
EXPECTED_BUSINESS = {
    "name": "Home & Verse",
    "legal_name": "DM Brands Ltd",
    "street": "79 Waterworks Road",
    "city": "Worcester",
    "postcode": "WR1 3EZ",
    "country": "GB",
    "phone": "+441905616006",
    "phone_display": "01905 616006",
    "email": "hello@homeandverse.co.uk",
    "company_number": "07517652",
}

# All policy/static pages that must exist and work
POLICY_PAGES = [
    "/about",
    "/delivery",
    "/returns",
    "/privacy",
    "/terms",
    "/cookies",
    "/contact",
    "/faqs",
    "/sustainability",
]

# All static assets that must exist
REQUIRED_ASSETS = [
    "/robots.txt",
    "/sitemap.xml",
    "/manifest.json",
    "/favicon.svg",
    "/logo.png",
    "/og-image.png",
    "/icon-192.png",
    "/google-products.csv",
]

SOCIAL_URLS = [
    "https://www.instagram.com/homeandverse",
    "https://www.facebook.com/homeandverse",
    "https://uk.pinterest.com/homeandverse",
]

# ============================================================
# RESULTS TRACKING
# ============================================================
results = {
    "critical": [],
    "warning": [],
    "info": [],
    "pass": [],
}

total_checks = 0
passed_checks = 0


def critical(msg):
    global total_checks
    total_checks += 1
    results["critical"].append(msg)
    print(f"  ❌ CRITICAL: {msg}")


def warning(msg):
    global total_checks
    total_checks += 1
    results["warning"].append(msg)
    print(f"  ⚠️  WARNING: {msg}")


def info(msg):
    global total_checks
    total_checks += 1
    results["info"].append(msg)


def passed(msg):
    global total_checks, passed_checks
    total_checks += 1
    passed_checks += 1
    results["pass"].append(msg)


def progress(current, total, label=""):
    bar_len = 40
    filled = int(bar_len * current / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)
    pct = (current / total * 100) if total > 0 else 0
    sys.stdout.write(f"\r  [{bar}] {pct:5.1f}% ({current}/{total}) {label[:40]:<40}")
    sys.stdout.flush()


def check_url(url, method="GET", timeout=15):
    """Check a URL and return (status_code, headers, body_or_None)"""
    try:
        if method == "HEAD":
            r = requests.head(url, timeout=timeout, allow_redirects=True)
            return r.status_code, dict(r.headers), None
        else:
            r = requests.get(url, timeout=timeout, allow_redirects=True)
            return r.status_code, dict(r.headers), r.text
    except requests.Timeout:
        return -1, {}, None
    except requests.ConnectionError:
        return -2, {}, None
    except Exception as e:
        return -3, {}, str(e)


def check_url_head(url, timeout=10):
    """Quick HEAD check, returns status code"""
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True)
        return r.status_code
    except:
        return -1


# ============================================================
# AUDIT SECTIONS
# ============================================================

def audit_ssl_and_redirects():
    print("\n" + "=" * 60)
    print("1. SSL & REDIRECTS")
    print("=" * 60)

    status, headers, body = check_url(SITE_URL)
    if status == 200:
        passed("Homepage returns 200 OK via HTTPS")
    else:
        critical(f"Homepage returns {status} (expected 200)")

    try:
        r = requests.get(SITE_URL.replace("https://", "http://"), allow_redirects=False, timeout=10)
        if r.status_code in (301, 302, 308):
            location = r.headers.get("Location", "")
            if "https://" in location:
                passed("HTTP redirects to HTTPS")
            else:
                warning(f"HTTP redirects to {location} (not HTTPS)")
        else:
            warning(f"HTTP returns {r.status_code} instead of redirecting to HTTPS")
    except:
        warning("Could not test HTTP→HTTPS redirect")

    try:
        r = requests.get("https://www.homeandverse.co.uk/", allow_redirects=False, timeout=10)
        if r.status_code in (301, 302, 308):
            passed("www redirects to non-www")
        elif r.status_code == 200:
            warning("www.homeandverse.co.uk returns 200 instead of redirecting — potential duplicate content")
        else:
            info(f"www returns {r.status_code}")
    except:
        info("Could not test www redirect")


def audit_head_requests():
    print("\n" + "=" * 60)
    print("2. HEAD REQUEST SUPPORT (Critical for Google crawling)")
    print("=" * 60)

    test_urls = [
        SITE_URL + "/",
        SITE_URL + "/about",
        SITE_URL + "/privacy",
        SITE_URL + "/delivery",
        SITE_URL + "/returns",
        SITE_URL + "/terms",
        SITE_URL + "/?product=AD5",
    ]

    for url in test_urls:
        status = check_url_head(url)
        short = url.replace(SITE_URL, "")
        if status == 200:
            passed(f"HEAD {short} → 200")
        elif status == 405:
            critical(f"HEAD {short} → 405 Method Not Allowed — Google crawler will fail!")
        else:
            warning(f"HEAD {short} → {status}")


def audit_required_assets():
    print("\n" + "=" * 60)
    print("3. REQUIRED ASSETS & FILES")
    print("=" * 60)

    for asset in REQUIRED_ASSETS:
        url = SITE_URL + asset
        status = check_url_head(url)
        if status == 200:
            passed(f"{asset} exists (200)")
        else:
            critical(f"{asset} returns {status} — must exist!")


def audit_robots_txt():
    print("\n" + "=" * 60)
    print("4. ROBOTS.TXT")
    print("=" * 60)

    status, _, body = check_url(SITE_URL + "/robots.txt")
    if status != 200:
        critical("robots.txt not accessible")
        return

    if "Disallow: /" in body and "Allow:" not in body:
        critical("robots.txt blocks all crawling!")

    if "Sitemap:" in body:
        passed("robots.txt includes Sitemap directive")
        sitemap_url = [l.split("Sitemap:")[1].strip() for l in body.split("\n") if "Sitemap:" in l]
        if sitemap_url:
            if SITE_URL in sitemap_url[0]:
                passed(f"Sitemap URL uses correct domain: {sitemap_url[0]}")
            else:
                warning(f"Sitemap URL may use wrong domain: {sitemap_url[0]}")
    else:
        warning("robots.txt missing Sitemap directive")

    if "Disallow: /api/" in body:
        passed("API routes blocked from crawling")
    else:
        info("Consider blocking /api/ in robots.txt")

    if "Disallow: /admin" in body:
        passed("Admin routes blocked from crawling")
    else:
        warning("Admin routes not blocked in robots.txt")


def audit_sitemap():
    print("\n" + "=" * 60)
    print("5. SITEMAP.XML")
    print("=" * 60)

    status, _, body = check_url(SITE_URL + "/sitemap.xml")
    if status != 200:
        critical("sitemap.xml not accessible")
        return

    try:
        root = ET.fromstring(body)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = root.findall(".//sm:url", ns)
        locs = [u.find("sm:loc", ns).text for u in urls]
        lastmods = [u.find("sm:lastmod", ns).text for u in urls if u.find("sm:lastmod", ns) is not None]

        passed(f"Sitemap has {len(locs)} URLs")

        from datetime import datetime, timedelta
        today = datetime.now()
        stale_count = 0
        for d in lastmods:
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                if (today - dt).days > 30:
                    stale_count += 1
            except:
                pass
        if stale_count > 0:
            warning(f"{stale_count}/{len(lastmods)} sitemap URLs have lastmod dates older than 30 days")
        else:
            passed("All sitemap dates are recent")

        policy_in_sitemap = 0
        for page in POLICY_PAGES:
            full_url = SITE_URL + page
            query_url = SITE_URL + "/?view=" + page.lstrip("/")
            if full_url in locs or query_url in locs:
                policy_in_sitemap += 1
            else:
                warning(f"Policy page {page} missing from sitemap")
        if policy_in_sitemap == len(POLICY_PAGES):
            passed("All policy pages included in sitemap")

        wrong_domain = [l for l in locs if not l.startswith(SITE_URL)]
        if wrong_domain:
            critical(f"{len(wrong_domain)} sitemap URLs use wrong domain: {wrong_domain[0]}")
        else:
            passed("All sitemap URLs use correct domain")

    except ET.ParseError:
        critical("sitemap.xml is not valid XML")


def audit_homepage_html():
    print("\n" + "=" * 60)
    print("6. HOMEPAGE HTML & META TAGS")
    print("=" * 60)

    status, headers, body = check_url(SITE_URL)
    if status != 200 or not body:
        critical("Cannot load homepage")
        return

    ct = headers.get("Content-Type", headers.get("content-type", ""))
    if "text/html" in ct:
        passed("Content-Type is text/html")
    else:
        critical(f"Content-Type is '{ct}' — must be text/html")

    title_match = re.search(r"<title>(.*?)</title>", body)
    if title_match:
        title = title_match.group(1)
        if len(title) > 10:
            passed(f"Title tag present: {title[:60]}")
        else:
            warning(f"Title tag too short: {title}")
    else:
        critical("No <title> tag found")

    desc_match = re.search(r'<meta name="description" content="(.*?)"', body)
    if desc_match:
        desc = desc_match.group(1)
        if len(desc) > 50:
            passed(f"Meta description present ({len(desc)} chars)")
        else:
            warning(f"Meta description too short: {len(desc)} chars")
    else:
        critical("No meta description found")

    canon_match = re.search(r'<link rel="canonical" href="(.*?)"', body)
    if canon_match:
        canon = canon_match.group(1)
        if canon.startswith(SITE_URL):
            passed(f"Canonical URL correct: {canon}")
        else:
            critical(f"Canonical URL wrong: {canon} (expected {SITE_URL})")
    else:
        warning("No canonical URL found")

    og_checks = {
        "og:title": r'property="og:title" content="(.*?)"',
        "og:description": r'property="og:description" content="(.*?)"',
        "og:image": r'property="og:image" content="(.*?)"',
        "og:url": r'property="og:url" content="(.*?)"',
    }
    for name, pattern in og_checks.items():
        match = re.search(pattern, body)
        if match:
            passed(f"{name} present: {match.group(1)[:60]}")
        else:
            warning(f"{name} missing")

    og_img_match = re.search(r'property="og:image" content="(.*?)"', body)
    if og_img_match:
        og_img_url = og_img_match.group(1)
        og_status = check_url_head(og_img_url)
        if og_status == 200:
            passed("OG image loads correctly")
        else:
            critical(f"OG image returns {og_status}: {og_img_url}")

    ld_json_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.DOTALL)
    if ld_json_blocks:
        passed(f"Found {len(ld_json_blocks)} structured data blocks")
        for i, block in enumerate(ld_json_blocks):
            try:
                data = json.loads(block)
                sd_type = data.get("@type", "unknown")
                passed(f"  Structured data block {i+1}: {sd_type} (valid JSON)")

                if sd_type == "HomeGoodsStore":
                    addr = data.get("address", {})
                    if addr.get("streetAddress") == EXPECTED_BUSINESS["street"]:
                        passed("  Structured data address matches expected")
                    else:
                        critical(f"  Structured data address MISMATCH: '{addr.get('streetAddress')}' vs expected '{EXPECTED_BUSINESS['street']}'")

                    if addr.get("postalCode") == EXPECTED_BUSINESS["postcode"]:
                        passed("  Structured data postcode matches")
                    else:
                        critical(f"  Structured data postcode MISMATCH: '{addr.get('postalCode')}' vs '{EXPECTED_BUSINESS['postcode']}'")

                    cp = data.get("contactPoint", {})
                    if cp.get("telephone") == EXPECTED_BUSINESS["phone"]:
                        passed("  Structured data phone matches")
                    else:
                        critical(f"  Structured data phone MISMATCH: '{cp.get('telephone')}' vs '{EXPECTED_BUSINESS['phone']}'")

                    if cp.get("email") == EXPECTED_BUSINESS["email"]:
                        passed("  Structured data email matches")
                    else:
                        critical(f"  Structured data email MISMATCH: '{cp.get('email')}' vs '{EXPECTED_BUSINESS['email']}'")

                    legal = data.get("legalName", "")
                    if legal == EXPECTED_BUSINESS["legal_name"]:
                        passed("  Structured data legal name matches")
                    else:
                        critical(f"  Structured data legal name MISMATCH: '{legal}' vs '{EXPECTED_BUSINESS['legal_name']}'")

                    same_as = data.get("sameAs", [])
                    for social in SOCIAL_URLS:
                        if social in same_as:
                            passed(f"  Social link present: {social}")
                        else:
                            warning(f"  Social link missing from sameAs: {social}")

                    logo_url = data.get("logo", "")
                    if logo_url:
                        logo_status = check_url_head(logo_url)
                        if logo_status == 200:
                            passed("  Structured data logo URL loads")
                        else:
                            critical(f"  Structured data logo returns {logo_status}: {logo_url}")

            except json.JSONDecodeError:
                critical(f"  Structured data block {i+1}: INVALID JSON!")
    else:
        critical("No structured data (JSON-LD) found")

    root_match = re.search(r'<div id="root">(.*?)</div>', body, re.DOTALL)
    if root_match:
        inner = root_match.group(1).strip()
        if len(inner) < 10:
            info("Empty <div id='root'> — SPA has no server-side content (inherent to SPA architecture)")
        else:
            passed("Root div has pre-rendered content")

    if "gtag" in body or "googletagmanager" in body or "analytics" in body.lower():
        passed("Google Analytics/GTM detected")
    else:
        info("No Google Analytics detected")


def audit_policy_pages():
    print("\n" + "=" * 60)
    print("7. POLICY PAGES (GET + HEAD)")
    print("=" * 60)

    for i, page in enumerate(POLICY_PAGES):
        url = SITE_URL + page
        progress(i + 1, len(POLICY_PAGES), page)

        status, headers, body = check_url(url)
        if status == 200:
            passed(f"GET {page} → 200")
        else:
            critical(f"GET {page} → {status}")

        head_status = check_url_head(url)
        if head_status == 200:
            passed(f"HEAD {page} → 200")
        elif head_status == 405:
            critical(f"HEAD {page} → 405 — Google crawler will fail!")
        else:
            warning(f"HEAD {page} → {head_status}")

        ct = headers.get("Content-Type", headers.get("content-type", ""))
        if "text/html" in ct:
            passed(f"{page} Content-Type is text/html")
        elif "application/json" in ct:
            critical(f"{page} returns JSON instead of HTML!")
        else:
            warning(f"{page} Content-Type: {ct}")

    print()


def audit_social_profiles():
    print("\n" + "=" * 60)
    print("8. SOCIAL MEDIA PROFILES")
    print("=" * 60)

    for url in SOCIAL_URLS:
        status = check_url_head(url)
        if status == 200:
            passed(f"{url} exists")
        elif status in (301, 302, 308):
            warning(f"{url} redirects ({status}) — update to final URL")
        else:
            warning(f"{url} returns {status}")


def audit_merchant_feed():
    print("\n" + "=" * 60)
    print("9. GOOGLE MERCHANT FEED AUDIT")
    print("=" * 60)

    status, _, body = check_url(SITE_URL + "/google-products.csv")
    if status != 200 or not body:
        critical("Cannot load merchant feed CSV")
        return

    reader = csv.DictReader(StringIO(body))
    products = list(reader)
    print(f"  Feed contains {len(products)} products")

    if len(products) == 0:
        critical("Merchant feed is empty!")
        return

    # Required fields check
    required_fields = ["id", "title", "description", "link", "image_link", "availability", "price", "brand", "condition"]
    recommended_fields = ["gtin", "google_product_category", "product_type", "color", "shipping_weight"]

    headers_found = list(products[0].keys()) if products else []
    for field in required_fields:
        if field in headers_found:
            passed(f"Required field '{field}' present in feed")
        else:
            critical(f"Required field '{field}' MISSING from feed")

    for field in recommended_fields:
        if field in headers_found:
            passed(f"Recommended field '{field}' present in feed")
        else:
            warning(f"Recommended field '{field}' missing from feed")

    missing_title = 0
    missing_desc = 0
    missing_image = 0
    missing_price = 0
    missing_gtin = 0
    wrong_domain_links = 0
    bad_availability = 0
    short_titles = 0
    short_descs = 0
    long_titles = 0
    bad_price_format = 0
    bad_gtin_format = 0
    duplicate_ids = set()
    seen_ids = set()

    for p in products:
        pid = p.get("id", "")
        if pid in seen_ids:
            duplicate_ids.add(pid)
        seen_ids.add(pid)

        if not p.get("title", "").strip():
            missing_title += 1
        elif len(p.get("title", "")) < 20:
            short_titles += 1
        elif len(p.get("title", "")) > 150:
            long_titles += 1

        if not p.get("description", "").strip():
            missing_desc += 1
        elif len(p.get("description", "")) < 50:
            short_descs += 1

        if not p.get("image_link", "").strip():
            missing_image += 1
        if not p.get("price", "").strip():
            missing_price += 1
        else:
            price_str = p.get("price", "")
            if not re.match(r'^\d+\.\d{2}\s+GBP$', price_str):
                bad_price_format += 1

        gtin = p.get("gtin", "").strip()
        if p.get("identifier_exists") == "yes" and not gtin:
            missing_gtin += 1
        elif gtin and not re.match(r'^\d{8,14}$', gtin):
            bad_gtin_format += 1

        link = p.get("link", "")
        if link and not link.startswith(SITE_URL) and not link.startswith(SITE_URL.replace('https://', 'https://www.')):
            wrong_domain_links += 1
        avail = p.get("availability", "")
        if avail not in ("in_stock", "out_of_stock", "preorder", "backorder"):
            bad_availability += 1

    if missing_title: critical(f"{missing_title} products missing title")
    else: passed("All products have titles")
    if short_titles: warning(f"{short_titles} products have very short titles (<20 chars)")
    if long_titles: warning(f"{long_titles} products have titles exceeding 150 chars (Google truncates)")
    if missing_desc: critical(f"{missing_desc} products missing description")
    else: passed("All products have descriptions")
    if short_descs: warning(f"{short_descs} products have short descriptions (<50 chars)")
    if missing_image: critical(f"{missing_image} products missing image")
    else: passed("All products have image links")
    if missing_price: critical(f"{missing_price} products missing price")
    else: passed("All products have prices")
    if bad_price_format: warning(f"{bad_price_format} products have non-standard price format (expected '12.34 GBP')")
    else: passed("All prices use correct format (XX.XX GBP)")
    if missing_gtin: warning(f"{missing_gtin} products have identifier_exists=yes but no GTIN")
    if bad_gtin_format: warning(f"{bad_gtin_format} products have invalid GTIN format (should be 8-14 digits)")
    else: passed("All GTINs are valid format")
    if duplicate_ids:
        critical(f"{len(duplicate_ids)} duplicate product IDs in feed: {', '.join(list(duplicate_ids)[:5])}")
    else:
        passed("No duplicate product IDs")
    if wrong_domain_links: critical(f"{wrong_domain_links} product links don't use {SITE_URL}")
    else: passed("All product links use correct domain")
    if bad_availability: warning(f"{bad_availability} products have non-standard availability values")
    else: passed("All availability values are valid")

    return products


def audit_product_urls(feed_products):
    print("\n" + "=" * 60)
    print("10. PRODUCT URL CHECKS (HEAD requests on ALL product links)")
    print("=" * 60)

    if not feed_products:
        critical("No feed products to check")
        return

    total = len(feed_products)
    errors_405 = []
    errors_other = []
    ok_count = 0

    def check_product(idx_product):
        idx, product = idx_product
        link = product.get("link", "")
        if not link:
            return ("no_link", product.get("id", "?"), link)
        try:
            r = requests.head(link, timeout=10, allow_redirects=True)
            return (r.status_code, product.get("id", "?"), link)
        except:
            return ("error", product.get("id", "?"), link)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_product, (i, p)): i for i, p in enumerate(feed_products)}
        done = 0
        for future in as_completed(futures):
            done += 1
            progress(done, total, "Checking product URLs...")
            result = future.result()
            status_code, pid, link = result
            if status_code == 200:
                ok_count += 1
            elif status_code == 405:
                errors_405.append((pid, link))
            else:
                errors_other.append((status_code, pid, link))

    print()

    if ok_count == total:
        passed(f"All {total} product URLs return 200")
    else:
        if errors_405:
            critical(f"{len(errors_405)} product URLs return 405 (HEAD request fails)")
            for pid, link in errors_405[:5]:
                print(f"    → {pid}: {link}")
            if len(errors_405) > 5:
                print(f"    ... and {len(errors_405) - 5} more")
        if errors_other:
            warning(f"{len(errors_other)} product URLs return non-200 status")
            for status, pid, link in errors_other[:5]:
                print(f"    → {pid}: {status} {link}")
            if len(errors_other) > 5:
                print(f"    ... and {len(errors_other) - 5} more")
        if ok_count > 0:
            passed(f"{ok_count}/{total} product URLs return 200")


def audit_product_images(feed_products):
    print("\n" + "=" * 60)
    print("11. PRODUCT IMAGE CHECKS (ALL images in feed)")
    print("=" * 60)

    if not feed_products:
        critical("No feed products to check")
        return

    image_urls = set()
    for p in feed_products:
        main_img = p.get("image_link", "").strip()
        if main_img:
            image_urls.add(main_img)
        additional = p.get("additional_image_link", "").strip()
        if additional:
            for img in additional.split(","):
                img = img.strip()
                if img:
                    image_urls.add(img)

    total = len(image_urls)
    print(f"  Found {total} unique image URLs to check")

    broken = []
    ok_count = 0

    def check_image(url):
        try:
            r = requests.head(url, timeout=10, allow_redirects=True)
            return (r.status_code, url)
        except:
            return ("error", url)

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(check_image, url): url for url in image_urls}
        done = 0
        for future in as_completed(futures):
            done += 1
            progress(done, total, "Checking images...")
            status, url = future.result()
            if status == 200:
                ok_count += 1
            else:
                broken.append((status, url))

    print()

    if ok_count == total:
        passed(f"All {total} product images load correctly")
    else:
        critical(f"{len(broken)} broken images in merchant feed!")
        for status, url in broken[:10]:
            print(f"    → {status}: {url}")
        if len(broken) > 10:
            print(f"    ... and {len(broken) - 10} more")
        passed(f"{ok_count}/{total} images load correctly")


def audit_price_consistency(feed_products):
    print("\n" + "=" * 60)
    print("12. PRICE & AVAILABILITY CONSISTENCY (Feed vs API)")
    print("=" * 60)

    if not feed_products:
        critical("No feed products to check")
        return

    try:
        r = requests.get(f"{API_BASE}/products?with_images_only=false", timeout=30)
        api_data = r.json()
        api_products = {p["sku"]: p for p in api_data.get("products", [])}
    except Exception as e:
        critical(f"Cannot load API products: {e}")
        return

    total = len(feed_products)
    price_mismatches = []
    stock_mismatches = []
    not_in_api = []

    for i, fp in enumerate(feed_products):
        progress(i + 1, total, "Checking prices...")
        feed_id = fp.get("id", "")
        feed_price = fp.get("price", "").replace(" GBP", "").strip()
        feed_avail = fp.get("availability", "")

        api_product = api_products.get(feed_id)
        if not api_product:
            not_in_api.append(feed_id)
            continue

        api_price = str(api_product.get("price", ""))
        api_in_stock = api_product.get("in_stock", False)
        api_avail = "in_stock" if api_in_stock else "out_of_stock"

        try:
            if abs(float(feed_price) - float(api_price)) > 0.01:
                price_mismatches.append((feed_id, feed_price, api_price))
        except (ValueError, TypeError):
            pass

        if feed_avail != api_avail:
            stock_mismatches.append((feed_id, feed_avail, api_avail))

    print()

    if not price_mismatches:
        passed("All prices match between feed and API")
    else:
        critical(f"{len(price_mismatches)} price mismatches between feed and API!")
        for pid, fp, ap in price_mismatches[:5]:
            print(f"    → {pid}: feed={fp} vs api={ap}")

    if not stock_mismatches:
        passed("All availability matches between feed and API")
    else:
        warning(f"{len(stock_mismatches)} availability mismatches between feed and API")
        for pid, fa, aa in stock_mismatches[:5]:
            print(f"    → {pid}: feed={fa} vs api={aa}")

    if not_in_api:
        warning(f"{len(not_in_api)} feed products not found in API")


def audit_soft_404s(feed_products):
    print("\n" + "=" * 60)
    print("13. SOFT 404 CHECK (pages that return 200 but wrong content)")
    print("=" * 60)

    if not feed_products:
        critical("No feed products to check")
        return

    # Sample 20 products to check content matches
    import random
    sample_size = min(20, len(feed_products))
    sample = random.sample(feed_products, sample_size)
    
    soft_404s = []
    content_mismatches = []

    for i, fp in enumerate(sample):
        progress(i + 1, sample_size, "Checking page content...")
        link = fp.get("link", "")
        feed_title = fp.get("title", "")
        feed_price = fp.get("price", "").replace(" GBP", "").strip()
        pid = fp.get("id", "")

        try:
            r = requests.get(link, timeout=15)
            if r.status_code != 200:
                continue

            body = r.text

            # Check if the page returns generic homepage content instead of product
            # A soft 404 would be: 200 status but no product-specific content
            # Since this is an SPA, the HTML will always be the same shell.
            # We check the API instead to make sure the product actually exists.
            api_url = f"{API_BASE}/products/{pid}"
            api_r = requests.get(api_url, timeout=10)
            if api_r.status_code != 200:
                soft_404s.append((pid, link, f"API returns {api_r.status_code}"))
                continue

            api_data = api_r.json()
            api_price = str(api_data.get("price", ""))
            api_name = api_data.get("name", "")

            # Price match check
            try:
                if abs(float(feed_price) - float(api_price)) > 0.01:
                    content_mismatches.append((pid, f"Feed price {feed_price} vs page price {api_price}"))
            except:
                pass

            # Check product is in stock on API
            if not api_data.get("in_stock", False):
                content_mismatches.append((pid, f"Feed says in_stock but API says out of stock"))

        except Exception as e:
            soft_404s.append((pid, link, str(e)))

    print()

    if not soft_404s:
        passed(f"No soft 404s found (checked {sample_size} products)")
    else:
        critical(f"{len(soft_404s)} soft 404s detected — product page exists but product missing!")
        for pid, link, reason in soft_404s[:5]:
            print(f"    → {pid}: {reason}")

    if not content_mismatches:
        passed(f"Feed data matches live site data (checked {sample_size} products)")
    else:
        critical(f"{len(content_mismatches)} content mismatches between feed and live site!")
        for pid, desc in content_mismatches[:5]:
            print(f"    → {pid}: {desc}")


def audit_product_structured_data():
    print("\n" + "=" * 60)
    print("14. PRODUCT PAGE STRUCTURED DATA (sample check)")
    print("=" * 60)

    # Check a few product pages for Product schema
    test_skus = ["AD5", "KU2", "SC20"]
    
    for sku in test_skus:
        api_url = f"{API_BASE}/products/{sku}"
        try:
            r = requests.get(api_url, timeout=10)
            if r.status_code != 200:
                warning(f"Cannot load product {sku} from API")
                continue
            api_data = r.json()
            
            # Check the product page HTML for structured data
            page_url = f"{SITE_URL}/?product={sku}"
            status, _, body = check_url(page_url)
            if status != 200:
                warning(f"Product page for {sku} returns {status}")
                continue

            # Look for Product structured data in HTML
            # Since this is an SPA, structured data might be injected by JS
            # We check the static HTML first
            ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.DOTALL)
            has_product_schema = False
            for block in ld_blocks:
                try:
                    data = json.loads(block)
                    # Check for Product type in @graph or directly
                    if data.get("@type") == "Product":
                        has_product_schema = True
                    graph = data.get("@graph", [])
                    for item in graph:
                        if item.get("@type") == "Product":
                            has_product_schema = True
                            # Check required fields
                            if "name" in item:
                                passed(f"  {sku}: Product schema has name")
                            else:
                                warning(f"  {sku}: Product schema missing name")
                            if "offers" in item:
                                offers = item["offers"]
                                if "price" in offers:
                                    passed(f"  {sku}: Product schema has price")
                                else:
                                    warning(f"  {sku}: Product schema missing price")
                                if "availability" in offers:
                                    passed(f"  {sku}: Product schema has availability")
                                else:
                                    warning(f"  {sku}: Product schema missing availability")
                            else:
                                warning(f"  {sku}: Product schema missing offers")
                except json.JSONDecodeError:
                    pass

            if has_product_schema:
                passed(f"Product {sku} has Product structured data")
            else:
                info(f"Product {sku} has no Product structured data in static HTML (may be injected by JS)")

        except Exception as e:
            warning(f"Error checking product {sku}: {e}")


def audit_checkout_endpoint():
    print("\n" + "=" * 60)
    print("15. CHECKOUT ENDPOINT")
    print("=" * 60)

    # Check that the Stripe checkout API endpoint exists and responds
    # We can't do a full checkout test but we can check the endpoint doesn't 404
    checkout_url = f"{API_BASE}/checkout/create-payment-intent"
    try:
        # POST with empty body — should get an error response, not a 404 or 500
        r = requests.post(checkout_url, json={}, timeout=10)
        if r.status_code == 404:
            critical("Checkout endpoint /api/create-checkout-session returns 404 — checkout broken!")
        elif r.status_code == 405:
            critical("Checkout endpoint returns 405 Method Not Allowed")
        elif r.status_code == 500:
            warning("Checkout endpoint returns 500 — may indicate a server error")
        elif r.status_code in (400, 422):
            passed(f"Checkout endpoint exists and validates input (returns {r.status_code} for empty request)")
        elif r.status_code == 200:
            passed("Checkout endpoint exists and responds")
        else:
            info(f"Checkout endpoint returns {r.status_code}")
    except Exception as e:
        critical(f"Cannot reach checkout endpoint: {e}")


def audit_shipping_info(feed_products):
    print("\n" + "=" * 60)
    print("16. SHIPPING INFO IN FEED")
    print("=" * 60)

    if not feed_products:
        return

    missing_weight = 0
    for p in feed_products:
        weight = p.get("shipping_weight", "").strip()
        if not weight:
            missing_weight += 1

    if missing_weight == 0:
        passed("All products have shipping weight")
    elif missing_weight < len(feed_products) * 0.1:
        warning(f"{missing_weight} products missing shipping weight")
    else:
        warning(f"{missing_weight}/{len(feed_products)} products missing shipping weight")


def audit_google_index():
    print("\n" + "=" * 60)
    print("17. GOOGLE INDEX STATUS")
    print("=" * 60)

    info("Cannot check Google index programmatically — check manually:")
    info(f"  Search: site:homeandverse.co.uk")
    info(f"  Or use Google Search Console URL Inspection tool")
    info(f"  If zero results, the site is NOT indexed — critical for Merchant Center")


def audit_response_times():
    print("\n" + "=" * 60)
    print("18. RESPONSE TIMES")
    print("=" * 60)

    test_urls = [
        ("/", "Homepage"),
        ("/about", "About page"),
        ("/api/products?limit=1", "API - single product"),
        ("/api/products", "API - all products"),
    ]

    for path, label in test_urls:
        url = SITE_URL + path
        start = time.time()
        status, _, _ = check_url(url)
        elapsed = time.time() - start
        if elapsed < 2:
            passed(f"{label}: {elapsed:.2f}s")
        elif elapsed < 5:
            warning(f"{label}: {elapsed:.2f}s (slow — Google may timeout)")
        else:
            critical(f"{label}: {elapsed:.2f}s (very slow — Google will likely timeout!)")


# ============================================================
# MAIN
# ============================================================

def main():
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║  HOME & VERSE — FULL SITE AUDIT                        ║")
    print("║  Google Merchant Center Compliance Check                ║")
    print("╚" + "═" * 58 + "╝")
    print(f"\n  Target: {SITE_URL}")
    print(f"  Time:   {time.strftime('%Y-%m-%d %H:%M:%S')}")

    audit_ssl_and_redirects()
    audit_head_requests()
    audit_required_assets()
    audit_robots_txt()
    audit_sitemap()
    audit_homepage_html()
    audit_policy_pages()
    audit_social_profiles()
    feed_products = audit_merchant_feed()
    audit_product_urls(feed_products)
    audit_product_images(feed_products)
    audit_price_consistency(feed_products)
    audit_soft_404s(feed_products)
    audit_product_structured_data()
    audit_checkout_endpoint()
    audit_shipping_info(feed_products)
    audit_google_index()
    audit_response_times()

    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║  AUDIT SUMMARY                                         ║")
    print("╚" + "═" * 58 + "╝")

    print(f"\n  Total checks:  {total_checks}")
    print(f"  ✅ Passed:     {len(results['pass'])}")
    print(f"  ❌ Critical:   {len(results['critical'])}")
    print(f"  ⚠️  Warnings:   {len(results['warning'])}")
    print(f"  ℹ️  Info:       {len(results['info'])}")

    if results["critical"]:
        print(f"\n  {'─' * 55}")
        print("  ❌ CRITICAL ISSUES (must fix before requesting review):")
        print(f"  {'─' * 55}")
        for i, msg in enumerate(results["critical"], 1):
            print(f"  {i:3}. {msg}")

    if results["warning"]:
        print(f"\n  {'─' * 55}")
        print("  ⚠️  WARNINGS (strongly recommended to fix):")
        print(f"  {'─' * 55}")
        for i, msg in enumerate(results["warning"], 1):
            print(f"  {i:3}. {msg}")

    if results["info"]:
        print(f"\n  {'─' * 55}")
        print("  ℹ️  INFO:")
        print(f"  {'─' * 55}")
        for i, msg in enumerate(results["info"], 1):
            print(f"  {i:3}. {msg}")

    print(f"\n  {'═' * 55}")
    if len(results["critical"]) == 0 and len(results["warning"]) == 0:
        print("  ✅ SITE LOOKS READY FOR GOOGLE MERCHANT CENTER REVIEW")
    elif len(results["critical"]) == 0:
        print("  ⚠️  FIX WARNINGS BEFORE REQUESTING REVIEW")
    else:
        print("  ❌ DO NOT REQUEST REVIEW — CRITICAL ISSUES FOUND")
    print(f"  {'═' * 55}\n")


if __name__ == "__main__":
    main()
