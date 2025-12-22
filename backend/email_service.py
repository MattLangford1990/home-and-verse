"""
Home & Verse - Email Service
=============================
Sends transactional emails for order confirmation and dispatch.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "orders@homeandverse.com")
FROM_NAME = os.getenv("FROM_NAME", "Home & Verse")


def get_base_template(content: str, preview_text: str = "") -> str:
    """Wrap content in base email template"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home & Verse</title>
    <!--[if mso]>
    <style type="text/css">
        body, table, td {{font-family: Arial, sans-serif !important;}}
    </style>
    <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #f7f7f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    <!-- Preview text -->
    <div style="display: none; max-height: 0; overflow: hidden;">
        {preview_text}
    </div>
    
    <!-- Email container -->
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 30px; text-align: center; border-bottom: 1px solid #eee;">
                            <h1 style="margin: 0; font-size: 24px; font-weight: 400; letter-spacing: 2px; color: #222;">HOME & VERSE</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            {content}
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; background: #fafafa; border-top: 1px solid #eee;">
                            <p style="margin: 0 0 10px; font-size: 13px; color: #666; text-align: center;">
                                Questions? Reply to this email or contact us at <a href="mailto:hello@homeandverse.com" style="color: #222;">hello@homeandverse.com</a>
                            </p>
                            <p style="margin: 0; font-size: 12px; color: #999; text-align: center;">
                                Home & Verse · Luxury European Homeware<br>
                                Ross-on-Wye, United Kingdom
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''


def format_order_items(items: list) -> str:
    """Format order items as HTML table rows"""
    rows = ""
    for item in items:
        qty = item.get('quantity', 1)
        price = item.get('price', 0) * qty
        rows += f'''
        <tr>
            <td style="padding: 12px 0; border-bottom: 1px solid #eee;">
                <p style="margin: 0; font-size: 14px; color: #222;">{item.get('name', item.get('sku', 'Product'))}</p>
                <p style="margin: 4px 0 0; font-size: 13px; color: #666;">Qty: {qty}</p>
            </td>
            <td style="padding: 12px 0; border-bottom: 1px solid #eee; text-align: right; font-size: 14px; color: #222;">
                £{price:.2f}
            </td>
        </tr>'''
    return rows


def order_confirmation_email(order_data: dict) -> tuple[str, str, str]:
    """
    Generate order confirmation email
    Returns: (subject, html_body, plain_text)
    """
    order_number = order_data.get('order_number', 'N/A')
    customer_name = order_data.get('customer_name', 'Customer')
    customer_email = order_data.get('customer_email', '')
    items = order_data.get('items', [])
    subtotal = order_data.get('subtotal', 0)
    shipping = order_data.get('shipping', 0)
    total = order_data.get('total', 0)
    address = order_data.get('address', {})
    
    subject = f"Order Confirmed - {order_number}"
    preview = f"Thank you for your order! Your order {order_number} has been received."
    
    # Format address
    address_html = f"""
        {address.get('address', '')}<br>
        {address.get('city', '')}<br>
        {address.get('zip', '')}<br>
        {address.get('country', 'United Kingdom')}
    """
    
    content = f'''
        <h2 style="margin: 0 0 20px; font-size: 20px; font-weight: 500; color: #222;">Thank you for your order!</h2>
        
        <p style="margin: 0 0 30px; font-size: 15px; color: #444; line-height: 1.6;">
            Hi {customer_name.split()[0] if customer_name else 'there'},<br><br>
            We've received your order and are getting it ready. We'll send you another email when it's on its way.
        </p>
        
        <!-- Order number box -->
        <div style="background: #f8f8f8; padding: 20px; margin-bottom: 30px; text-align: center;">
            <p style="margin: 0 0 5px; font-size: 13px; color: #666; text-transform: uppercase; letter-spacing: 1px;">Order Reference</p>
            <p style="margin: 0; font-size: 20px; font-weight: 500; color: #222;">{order_number}</p>
        </div>
        
        <!-- Order items -->
        <h3 style="margin: 0 0 15px; font-size: 14px; font-weight: 500; color: #222; text-transform: uppercase; letter-spacing: 1px;">Order Summary</h3>
        
        <table role="presentation" style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            {format_order_items(items)}
            <tr>
                <td style="padding: 12px 0; font-size: 14px; color: #666;">Subtotal</td>
                <td style="padding: 12px 0; text-align: right; font-size: 14px; color: #222;">£{subtotal:.2f}</td>
            </tr>
            <tr>
                <td style="padding: 12px 0; font-size: 14px; color: #666;">Delivery</td>
                <td style="padding: 12px 0; text-align: right; font-size: 14px; color: #222;">{"FREE" if shipping == 0 else f"£{shipping:.2f}"}</td>
            </tr>
            <tr>
                <td style="padding: 15px 0 0; font-size: 16px; font-weight: 500; color: #222; border-top: 2px solid #222;">Total</td>
                <td style="padding: 15px 0 0; text-align: right; font-size: 16px; font-weight: 500; color: #222; border-top: 2px solid #222;">£{total:.2f}</td>
            </tr>
        </table>
        
        <!-- Delivery address -->
        <h3 style="margin: 30px 0 15px; font-size: 14px; font-weight: 500; color: #222; text-transform: uppercase; letter-spacing: 1px;">Delivery Address</h3>
        <p style="margin: 0; font-size: 14px; color: #444; line-height: 1.6;">
            {customer_name}<br>
            {address_html}
        </p>
        
        <!-- What's next -->
        <div style="margin-top: 40px; padding-top: 30px; border-top: 1px solid #eee;">
            <h3 style="margin: 0 0 15px; font-size: 14px; font-weight: 500; color: #222;">What happens next?</h3>
            <p style="margin: 0; font-size: 14px; color: #666; line-height: 1.6;">
                We're preparing your order now. Most orders are dispatched within 1-2 business days. 
                You'll receive a shipping confirmation email with tracking details once your order is on its way.
            </p>
        </div>
    '''
    
    html_body = get_base_template(content, preview)
    
    # Plain text version
    plain_text = f"""
Thank you for your order!

Hi {customer_name.split()[0] if customer_name else 'there'},

We've received your order and are getting it ready. We'll send you another email when it's on its way.

Order Reference: {order_number}

ORDER SUMMARY
{chr(10).join([f"- {item.get('name', 'Product')} x{item.get('quantity', 1)} - £{item.get('price', 0) * item.get('quantity', 1):.2f}" for item in items])}

Subtotal: £{subtotal:.2f}
Delivery: {"FREE" if shipping == 0 else f"£{shipping:.2f}"}
Total: £{total:.2f}

DELIVERY ADDRESS
{customer_name}
{address.get('address', '')}
{address.get('city', '')}
{address.get('zip', '')}
{address.get('country', 'United Kingdom')}

What happens next?
We're preparing your order now. Most orders are dispatched within 1-2 business days. 
You'll receive a shipping confirmation email with tracking details once your order is on its way.

Questions? Reply to this email or contact us at hello@homeandverse.com

Home & Verse
Luxury European Homeware
"""
    
    return subject, html_body, plain_text


def dispatch_email(order_data: dict) -> tuple[str, str, str]:
    """
    Generate dispatch/shipping notification email
    Returns: (subject, html_body, plain_text)
    """
    order_number = order_data.get('order_number', 'N/A')
    customer_name = order_data.get('customer_name', 'Customer')
    items = order_data.get('items', [])
    tracking_number = order_data.get('tracking_number', '')
    tracking_url = order_data.get('tracking_url', '')
    carrier = order_data.get('carrier', 'Royal Mail')
    address = order_data.get('address', {})
    
    subject = f"Your order is on its way! - {order_number}"
    preview = f"Great news! Your order {order_number} has been dispatched."
    
    # Tracking section
    tracking_html = ""
    if tracking_number:
        tracking_html = f'''
        <div style="background: #f8f8f8; padding: 20px; margin: 20px 0; text-align: center;">
            <p style="margin: 0 0 5px; font-size: 13px; color: #666; text-transform: uppercase; letter-spacing: 1px;">Tracking Number</p>
            <p style="margin: 0 0 15px; font-size: 18px; font-weight: 500; color: #222;">{tracking_number}</p>
            <p style="margin: 0; font-size: 13px; color: #666;">Carrier: {carrier}</p>
            {f'<a href="{tracking_url}" style="display: inline-block; margin-top: 15px; padding: 12px 24px; background: #222; color: #fff; text-decoration: none; font-size: 13px; letter-spacing: 0.5px;">TRACK YOUR ORDER</a>' if tracking_url else ''}
        </div>
        '''
    
    # Format address
    address_html = f"""
        {address.get('address', '')}<br>
        {address.get('city', '')}<br>
        {address.get('zip', '')}<br>
        {address.get('country', 'United Kingdom')}
    """
    
    content = f'''
        <h2 style="margin: 0 0 20px; font-size: 20px; font-weight: 500; color: #222;">Your order is on its way! 📦</h2>
        
        <p style="margin: 0 0 30px; font-size: 15px; color: #444; line-height: 1.6;">
            Hi {customer_name.split()[0] if customer_name else 'there'},<br><br>
            Great news! Your order has been dispatched and is on its way to you.
        </p>
        
        <!-- Order number -->
        <div style="background: #f8f8f8; padding: 15px 20px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 13px; color: #666;">
                Order Reference: <strong style="color: #222;">{order_number}</strong>
            </p>
        </div>
        
        {tracking_html}
        
        <!-- Items shipped -->
        <h3 style="margin: 30px 0 15px; font-size: 14px; font-weight: 500; color: #222; text-transform: uppercase; letter-spacing: 1px;">Items Shipped</h3>
        
        <table role="presentation" style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            {format_order_items(items)}
        </table>
        
        <!-- Delivery address -->
        <h3 style="margin: 30px 0 15px; font-size: 14px; font-weight: 500; color: #222; text-transform: uppercase; letter-spacing: 1px;">Delivering To</h3>
        <p style="margin: 0; font-size: 14px; color: #444; line-height: 1.6;">
            {customer_name}<br>
            {address_html}
        </p>
        
        <!-- Delivery info -->
        <div style="margin-top: 40px; padding: 20px; background: #fff8e6; border-left: 3px solid #f5a623;">
            <h3 style="margin: 0 0 10px; font-size: 14px; font-weight: 500; color: #222;">Delivery Information</h3>
            <p style="margin: 0; font-size: 14px; color: #666; line-height: 1.6;">
                Standard delivery typically takes 2-3 working days. If you're not in when delivery is attempted, 
                the carrier will leave a card with collection/redelivery options.
            </p>
        </div>
    '''
    
    html_body = get_base_template(content, preview)
    
    # Plain text version
    plain_text = f"""
Your order is on its way!

Hi {customer_name.split()[0] if customer_name else 'there'},

Great news! Your order has been dispatched and is on its way to you.

Order Reference: {order_number}
{f"Tracking Number: {tracking_number}" if tracking_number else ""}
{f"Carrier: {carrier}" if tracking_number else ""}
{f"Track your order: {tracking_url}" if tracking_url else ""}

ITEMS SHIPPED
{chr(10).join([f"- {item.get('name', 'Product')} x{item.get('quantity', 1)}" for item in items])}

DELIVERING TO
{customer_name}
{address.get('address', '')}
{address.get('city', '')}
{address.get('zip', '')}
{address.get('country', 'United Kingdom')}

DELIVERY INFORMATION
Standard delivery typically takes 2-3 working days. If you're not in when delivery is attempted, 
the carrier will leave a card with collection/redelivery options.

Questions? Reply to this email or contact us at hello@homeandverse.com

Home & Verse
Luxury European Homeware
"""
    
    return subject, html_body, plain_text


async def send_email(to_email: str, subject: str, html_body: str, plain_text: str = "") -> dict:
    """Send an email via SMTP"""
    
    if not SMTP_USER or not SMTP_PASSWORD:
        return {"success": False, "error": "Email not configured - SMTP credentials missing"}
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Reply-To'] = FROM_EMAIL
        
        # Attach plain text and HTML versions
        if plain_text:
            msg.attach(MIMEText(plain_text, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return {"success": True, "message": f"Email sent to {to_email}"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


async def send_order_confirmation(order_data: dict) -> dict:
    """Send order confirmation email to customer"""
    customer_email = order_data.get('customer_email')
    if not customer_email:
        return {"success": False, "error": "No customer email provided"}
    
    subject, html_body, plain_text = order_confirmation_email(order_data)
    return await send_email(customer_email, subject, html_body, plain_text)


async def send_dispatch_notification(order_data: dict) -> dict:
    """Send dispatch notification email to customer"""
    customer_email = order_data.get('customer_email')
    if not customer_email:
        return {"success": False, "error": "No customer email provided"}
    
    subject, html_body, plain_text = dispatch_email(order_data)
    return await send_email(customer_email, subject, html_body, plain_text)


# Preview functions for testing
def preview_confirmation_email(order_data: dict) -> str:
    """Return HTML preview of confirmation email"""
    _, html, _ = order_confirmation_email(order_data)
    return html


def preview_dispatch_email(order_data: dict) -> str:
    """Return HTML preview of dispatch email"""
    _, html, _ = dispatch_email(order_data)
    return html
