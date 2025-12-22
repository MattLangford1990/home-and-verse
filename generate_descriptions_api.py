#!/usr/bin/env python3
"""
Generate product descriptions using Claude API - test batch
"""

import json
import anthropic

# Load products
with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json') as f:
    data = json.load(f)

# Get 20 diverse Räder products
rader = [p for p in data['products'] if p.get('brand') == 'Räder']

# Pick a diverse sample
sample = []
seen_types = set()
for p in rader:
    name_lower = p['name'].lower()
    # Try to get variety
    ptype = None
    for t in ['lichthaus', 'light house', 'teelicht', 'vase', 'figur', 'teller', 'schale', 'kette', 'ornament', 'napkin', 'mug', 'cup', 'bowl', 'candle']:
        if t in name_lower:
            ptype = t
            break
    
    if ptype and ptype not in seen_types:
        sample.append(p)
        seen_types.add(ptype)
    elif len(sample) < 20 and ptype is None:
        sample.append(p)
    
    if len(sample) >= 20:
        break

# If we don't have 20 yet, add more
if len(sample) < 20:
    for p in rader:
        if p not in sample:
            sample.append(p)
        if len(sample) >= 20:
            break

print(f"Selected {len(sample)} Räder products for test batch\n")

# Build the prompt
products_text = ""
for i, p in enumerate(sample):
    products_text += f"""
Product {i+1}:
- SKU: {p['sku']}
- Name: {p['name']}
- Category: {p.get('category', p.get('categories', [''])[0] if p.get('categories') else '')}
"""

prompt = f"""Generate unique, compelling product descriptions for these Räder homeware products. 

Räder is a German design company known for poetic, minimalist homeware with Scandinavian-inspired aesthetics. Their products feature delicate details, atmospheric lighting, and nature-inspired motifs.

For each product, write a 2-3 sentence description that:
1. Describes what the product actually IS and what it's used for
2. Highlights specific features visible in the product name (dimensions, materials, designs)
3. Uses warm, inviting language without being overly flowery
4. Does NOT mention "Räder" or "German" - the brand is already shown separately
5. Ends with a subtle suggestion of use or gifting

{products_text}

Return your response as a JSON object with SKU as key and description as value. Example:
{{"12345": "A delicate porcelain tealight holder featuring an intricate star cutout design. The warm candlelight creates beautiful shadow patterns on surrounding surfaces. Perfect for cosy evenings or as a thoughtful gift."}}

Return ONLY the JSON object, no other text."""

# Call Claude API
client = anthropic.Anthropic()

print("Calling Claude API...")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

response_text = message.content[0].text
print(f"\nTokens used - Input: {message.usage.input_tokens}, Output: {message.usage.output_tokens}")
print(f"Total tokens: {message.usage.input_tokens + message.usage.output_tokens}\n")

# Parse response
try:
    descriptions = json.loads(response_text)
except json.JSONDecodeError:
    # Try to extract JSON from response
    import re
    match = re.search(r'\{[\s\S]*\}', response_text)
    if match:
        descriptions = json.loads(match.group())
    else:
        print("Failed to parse response:")
        print(response_text)
        exit(1)

# Display results
print("=" * 70)
print("GENERATED DESCRIPTIONS")
print("=" * 70)

for p in sample:
    sku = p['sku']
    if sku in descriptions:
        print(f"\n{sku}: {p['name'][:50]}")
        print(f"  OLD: {p.get('description', '')[:100]}...")
        print(f"  NEW: {descriptions[sku]}")

print("\n" + "=" * 70)
print(f"Generated {len(descriptions)} descriptions")
print("=" * 70)

# Save for review
with open('/Users/matt/Desktop/home-and-verse/test_descriptions.json', 'w') as f:
    json.dump(descriptions, f, indent=2)
print("\nSaved to test_descriptions.json for review")
