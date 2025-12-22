#!/usr/bin/env python3
"""Generate email previews"""
from email_service import preview_confirmation_email, preview_dispatch_email

# Sample order data
order_data = {
    "order_number": "SO-04794",
    "customer_name": "Matt Langford",
    "customer_email": "matt@example.com",
    "items": [
        {"name": "Relaxound Zwitscherbox Oak", "quantity": 3, "price": 59.95},
    ],
    "subtotal": 179.85,
    "shipping": 0,
    "total": 179.85,
    "address": {
        "address": "123 Test Street",
        "city": "Ross-on-Wye",
        "zip": "HR9 5AA",
        "country": "United Kingdom"
    }
}

# Save confirmation email preview
html = preview_confirmation_email(order_data)
with open('/Users/matt/Desktop/home-and-verse/email-preview-confirmation.html', 'w') as f:
    f.write(html)
print("Saved: email-preview-confirmation.html")

# Dispatch email with tracking
order_data["tracking_number"] = "RR123456789GB"
order_data["tracking_url"] = "https://www.royalmail.com/track-your-item#/tracking-results/RR123456789GB"
order_data["carrier"] = "Royal Mail"

html = preview_dispatch_email(order_data)
with open('/Users/matt/Desktop/home-and-verse/email-preview-dispatch.html', 'w') as f:
    f.write(html)
print("Saved: email-preview-dispatch.html")
