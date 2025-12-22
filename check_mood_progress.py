#!/usr/bin/env python3
import json
with open('/Users/matt/Desktop/home-and-verse/processed-rader-mood/upload_progress.json') as f:
    d = json.load(f)
print(f"Files processed: {len(d.get('uploaded', []))}")
print(f"SKUs with mood images: {len(d.get('sku_mood_count', {}))}")
print(f"Failed: {len(d.get('failed', []))}")
