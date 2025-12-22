# Home & Verse - E-Commerce Website Project
## Handoff Note for Claude Continuation
**Created:** 10 December 2025
**Project Location:** `/Users/matt/Desktop/home-and-verse/`

---

## PROJECT OVERVIEW

Building a luxury homeware e-commerce website for DM Brands with design inspiration from:
- **Nordic Nest** (nordicnest.com) - Clean Scandinavian aesthetic
- **Royal Design** (royaldesign.co.uk) - Category-led navigation, minimal styling
- **Heal's** (heals.com) - Premium positioning

**Branding:** "Home & Verse" (working name - not brand-focused, category-led)

---

## WHAT'S BEEN COMPLETED ✅

### Backend (FastAPI) - WORKING
Location: `backend/`

- **main.py** - Full API with endpoints:
  - `GET /api/products` - Filter by brand, category, search, in_stock
  - `GET /api/products/{sku}` - Single product
  - `GET /api/brands` - Brand list with counts
  - `GET /api/categories` - Category list with counts
  - `GET /api/stats` - Dashboard stats
  - Static image serving from `/images/`

- **Data files:**
  - `data/products.json` - **1,276 products** imported from Zoho
  - `data/stock.json` - Stock levels
  - `data/images/` - **2,900+ product images** (SKU-named .jpg files)

- **Supporting files:**
  - `import_from_zoho.py` - Script to refresh product data
  - `requirements.txt` - FastAPI, uvicorn dependencies
  - `.env` - Zoho API credentials

### Frontend (React) - FUNCTIONAL ✅
Location: `preview.html`

**Complete:**
- Full React SPA with Babel compilation
- **Homepage** with hero section, category cards, new arrivals grid, trust bar
- **Products page** with sidebar filtering (category, price range), sorting, breadcrumbs
- **Product detail page** (full page, not modal) with add to bag
- **Shopping cart drawer** with quantity controls, free shipping progress bar
- **Full checkout page** with contact, address, payment forms, order summary
- Category navigation with product counts
- Search functionality
- Nordic Nest/Royal Design-inspired minimal styling (Inter font, clean whites, elegant spacing)
- API integration to backend
- Order confirmation screen

---

## WHAT STILL NEEDS DOING ❌

### Frontend Enhancements
1. **Mega-menu navigation** - Match Royal Design's dropdown style with subcategories/images
2. **Responsive design** - Mobile menu, mobile-friendly grids (currently desktop-only)
3. **Multiple product images** - Currently single image per product
4. **Related products section** - On product detail page
5. **Wishlist functionality** - Save for later
6. **Brand filtering** - Add brand selector in sidebar
7. **Lifestyle imagery** - Replace placeholder hero with actual lifestyle photos

### Backend (Lower Priority)
1. **Real payment integration** - Connect to Stripe (currently simulated)
2. **Order submission** - POST endpoint to save orders
3. **Zoho integration** - Submit orders back to Zoho
4. **Stock sync** - Regular stock level updates
5. **Email confirmations** - Order confirmation emails

### General
1. **Final brand name** - "Home & Verse" is placeholder
2. **Logo/branding assets** - None yet
3. **Hosting setup** - TBD

---

## HOW TO RUN

### Start Backend
```bash
cd /Users/matt/Desktop/home-and-verse/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### View Frontend
Open `preview.html` in browser (with backend running)

Or serve it:
```bash
cd /Users/matt/Desktop/home-and-verse
python -m http.server 3000
# Then visit http://localhost:3000/preview.html
```

---

## KEY DESIGN REFERENCES

When continuing, keep these design principles from Nordic Nest/Royal Design:

1. **Typography:** Clean sans-serif (Inter), generous letter-spacing on headings
2. **Whitespace:** Lots of breathing room, don't crowd elements
3. **Product grid:** 4 columns desktop, clean cards, subtle hover lift
4. **Navigation:** Category-first (not brand-first), slim header
5. **Colours:** Neutral palette - whites, light greys, black text
6. **No clutter:** Minimal badges, no excessive promotions

---

## FILE STRUCTURE

```
home-and-verse/
├── preview.html          # Main frontend (React SPA)
├── HANDOFF_NOTE.md       # This file
└── backend/
    ├── main.py           # FastAPI server
    ├── requirements.txt  # Python dependencies
    ├── .env              # API credentials
    ├── import_from_zoho.py
    └── data/
        ├── products.json # 1,276 products
        ├── stock.json    # Stock levels
        └── images/       # 2,900+ product images
```

---

## RESUME INSTRUCTIONS

To continue this project in a new chat:

1. Say: *"Continue the Home & Verse e-commerce website project - check the HANDOFF_NOTE.md at `/Users/matt/Desktop/home-and-verse/`"*

2. Claude should read this file first, then check `preview.html` current state

3. Pick up from the "What Still Needs Doing" section above

---

## PREVIOUS CHAT REFERENCE

Original chat: "E-commerce website design inspiration"
Link: https://claude.ai/chat/cd443f45-3c88-4928-9ebe-5d29938635c7

---

*Last updated: 10 December 2025*
