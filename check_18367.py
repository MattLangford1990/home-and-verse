#!/usr/bin/env python3
import json
from pathlib import Path

# Check manifest
with open('/Users/matt/Desktop/home-and-verse/backend/data/image_extras.json') as f:
    extras = json.load(f)

print('18367 in manifest:', '18367' in extras)
print('Entry:', extras.get('18367', 'NOT FOUND'))

# Check all uploaded files for 18367
for pfile in [
    '/Users/matt/Desktop/home-and-verse/processed-rader-images/upload_progress.json', 
    '/Users/matt/Desktop/home-and-verse/processed-rader-images/upload_progress_v2.json'
]:
    with open(pfile) as f:
        data = json.load(f)
    matches = [f for f in data.get('uploaded', []) if '18367' in f]
    if matches:
        print(f'From {Path(pfile).name}:')
        for m in matches:
            print(f'  {m}')

# Also check what actually exists in Cloudinary
print('\nChecking Cloudinary directly...')
import urllib.request
for suffix in ['', '_1', '_2', '_3', '_4', '_5']:
    url = f'https://res.cloudinary.com/dcfbgveei/image/upload/w_100/products/18367{suffix}.jpg'
    try:
        req = urllib.request.Request(url, method='HEAD')
        resp = urllib.request.urlopen(req)
        print(f'  18367{suffix}.jpg: EXISTS')
    except:
        print(f'  18367{suffix}.jpg: not found')
