# Home and Verse - Handoff Notes
> Drop this file into a new Claude chat to continue where you left off

## Project Location
`~/Desktop/home-and-verse/`

## Stack
- **Frontend**: React (preview.html)
- **Backend**: FastAPI (main.py, port 8000)
- **Data**: Products imported from Zoho → `backend/data/products.json`

## Current State (Last Updated: 10 Dec 2025)

### Working ✅
- Product display with images
- Multi-category support (Christmas, Gifts, Home Décor, etc.)
- Products without images hidden by default
- Christmas ranking: Räder boosted +100, £15-25 items get +20
- Popularity sort as default
- Category keyword mapping (removed German terms)

### In Progress / Issues 🔧
- **Shipping values missing** - got removed somewhere, need to restore
- **Need to filter out**: Display items, bulk/multi-pack items (e.g., "tray.24.miniT")
- **Rankings refresh**: Script at `backend/update_rankings.py`, cron every 2 days

### Key Files
- `backend/main.py` - API endpoints
- `backend/import_from_zoho.py` - Product import script
- `backend/update_rankings.py` - Popularity ranking generator
- `backend/data/products.json` - Product data
- `preview.html` - Frontend preview

### Commands
```bash
# Start backend
cd ~/Desktop/home-and-verse/backend
python3 -m uvicorn main:app --port 8000 --reload

# Re-import products from Zoho
python3 import_from_zoho.py --in-stock-only --skip-images

# Update rankings
python3 update_rankings.py
```

## Next Steps
1. Restore shipping values in product data
2. Filter out display items and bulk packs
3. [Add your next task here]

---
*Update this file as you work - it's your lifeline when chats hit limits*
