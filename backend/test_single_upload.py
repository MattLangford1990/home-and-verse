#!/usr/bin/env python3
"""Test single image upload to Zoho"""

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv("/Users/matt/Desktop/dm-sales-app/backend/.env")

response = requests.post(
    "https://accounts.zoho.eu/oauth/v2/token",
    data={
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token"
    }
)
token = response.json().get("access_token")
print(f"Got token: {bool(token)}")

headers = {
    "Authorization": f"Zoho-oauthtoken {token}",
    "X-com-zoho-inventory-organizationid": os.getenv("ZOHO_ORG_ID")
}

img_path = Path("/Users/matt/Desktop/home-and-verse/backend/data/images/11ZBX0101018_2.jpg")
item_id = "310656000001756729"

print(f"Uploading {img_path.name} to item {item_id}...")

with open(img_path, "rb") as img_file:
    files = {"image": (img_path.name, img_file, "image/jpeg")}
    r = requests.post(
        f"https://www.zohoapis.eu/inventory/v1/items/{item_id}/image",
        headers=headers,
        files=files
    )

print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
