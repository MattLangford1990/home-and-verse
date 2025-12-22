#!/usr/bin/env python3
"""
Generate ALL product descriptions with improved rule-based system.
Run: python3 generate_all_descriptions.py

This overwrites ALL existing descriptions with fresh, better ones.
"""

import json
import re
import random

# Load products
with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json') as f:
    data = json.load(f)

def extract_dimensions(name):
    """Extract dimensions from product name"""
    dims = {}
    # Diameter
    d_match = re.search(r'[Dd](?:ia)?\.?\s*(\d+(?:[.,]\d+)?)\s*cm', name)
    if d_match:
        dims['diameter'] = d_match.group(1).replace(',', '.')
    # Height
    h_match = re.search(r'[Hh]\.?\s*(\d+(?:[.,]\d+)?)\s*cm', name)
    if h_match:
        dims['height'] = h_match.group(1).replace(',', '.')
    # Width
    w_match = re.search(r'[Ww]\.?\s*(\d+(?:[.,]\d+)?)\s*cm', name)
    if w_match:
        dims['width'] = w_match.group(1).replace(',', '.')
    # Length
    l_match = re.search(r'[Ll]\.?\s*(\d+(?:[.,]\d+)?)\s*cm', name)
    if l_match:
        dims['length'] = l_match.group(1).replace(',', '.')
    # Generic dimensions like 10x15x20cm
    gen_match = re.search(r'(\d+(?:[.,]\d+)?)\s*x\s*(\d+(?:[.,]\d+)?)\s*(?:x\s*(\d+(?:[.,]\d+)?))?\s*cm', name)
    if gen_match:
        dims['dim1'] = gen_match.group(1).replace(',', '.')
        dims['dim2'] = gen_match.group(2).replace(',', '.')
        if gen_match.group(3):
            dims['dim3'] = gen_match.group(3).replace(',', '.')
    # Volume
    vol_match = re.search(r'(\d+(?:[.,]\d+)?)\s*[Ll](?:itre)?', name)
    if vol_match:
        dims['volume'] = vol_match.group(1).replace(',', '.')
    # ML
    ml_match = re.search(r'(\d+)\s*ml', name, re.IGNORECASE)
    if ml_match:
        dims['ml'] = ml_match.group(1)
    return dims

def extract_quantity(name):
    """Extract quantity/set size"""
    qty_patterns = [
        r'set\s*(?:of\s*)?(\d+)',
        r'(\d+)\s*(?:er\s*)?set',
        r'(\d+)\s*pieces?',
        r'(\d+)\s*(?:Stück|stück|Stck)',
        r'(\d+)\s*pcs',
        r'(\d+)er',
    ]
    for pattern in qty_patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return match.group(1)
    # Check for "X designs a Y pieces" pattern
    match = re.search(r'(\d+)\s*designs?\s*[ax]\s*(\d+)', name, re.IGNORECASE)
    if match:
        return str(int(match.group(1)) * int(match.group(2)))
    return None

def extract_color(name):
    """Extract color from name"""
    colors = {
        'gold': 'golden', 'golden': 'golden', 'silver': 'silver', 'white': 'white',
        'black': 'black', 'blue': 'blue', 'green': 'green', 'red': 'red',
        'pink': 'pink', 'rose': 'rose', 'grey': 'grey', 'gray': 'grey',
        'beige': 'beige', 'cream': 'cream', 'copper': 'copper', 'bronze': 'bronze',
        'yellow': 'yellow', 'orange': 'orange', 'purple': 'purple', 'turquoise': 'turquoise',
        'oak': 'oak', 'walnut': 'walnut', 'natural': 'natural', 'pastel': 'pastel'
    }
    name_lower = name.lower()
    for color_key, color_val in colors.items():
        if color_key in name_lower:
            return color_val
    return None

def extract_animal(name):
    """Extract animal from name"""
    animals = {
        'bird': 'bird', 'birdie': 'bird', 'birdy': 'bird', 'robin': 'robin',
        'bunny': 'bunny', 'rabbit': 'rabbit', 'hare': 'hare',
        'elephant': 'elephant', 'pig': 'pig', 'piggy': 'pig',
        'whale': 'whale', 'deer': 'deer', 'reindeer': 'reindeer', 'moose': 'moose',
        'cat': 'cat', 'dog': 'dog', 'owl': 'owl', 'fox': 'fox',
        'bear': 'bear', 'polar bear': 'polar bear', 'mouse': 'mouse',
        'squirrel': 'squirrel', 'penguin': 'penguin', 'fish': 'fish',
        'butterfly': 'butterfly', 'bee': 'bee', 'hedgehog': 'hedgehog',
        'swan': 'swan', 'dove': 'dove', 'donkey': 'donkey', 'cow': 'cow',
        'sheep': 'sheep', 'lamb': 'lamb', 'chicken': 'chicken', 'hen': 'hen',
        'duck': 'duck', 'goose': 'goose', 'frog': 'frog', 'snail': 'snail',
        'ladybug': 'ladybug', 'dragonfly': 'dragonfly', 'seahorse': 'seahorse',
        'crab': 'crab', 'starfish': 'starfish', 'turtle': 'turtle',
        'angel': 'angel', 'santa': 'Santa', 'snowman': 'snowman',
    }
    name_lower = name.lower()
    for animal_key, animal_val in animals.items():
        if animal_key in name_lower:
            return animal_val
    return None

def extract_theme(name):
    """Extract theme/occasion from name"""
    themes = {
        'christmas': 'Christmas', 'xmas': 'Christmas', 'weihnacht': 'Christmas',
        'advent': 'Advent', 'easter': 'Easter', 'ostern': 'Easter',
        'spring': 'spring', 'winter': 'winter', 'winterland': 'winter',
        'summer': 'summer', 'autumn': 'autumn', 'fall': 'autumn', 'herbst': 'autumn',
        'birthday': 'birthday', 'geburtstag': 'birthday',
        'wedding': 'wedding', 'hochzeit': 'wedding',
        'love': 'love', 'liebe': 'love', 'heart': 'heart', 'herz': 'heart',
        'baby': 'baby', 'valentine': "Valentine's",
        'mother': "Mother's Day", 'muttertag': "Mother's Day",
        'father': "Father's Day", 'vatertag': "Father's Day",
        'halloween': 'Halloween', 'thanksgiving': 'Thanksgiving',
        'new year': 'New Year', 'silvester': 'New Year',
    }
    name_lower = name.lower()
    for theme_key, theme_val in themes.items():
        if theme_key in name_lower:
            return theme_val
    return None

def extract_material(name):
    """Extract material from name"""
    materials = {
        'porcelain': 'porcelain', 'porzellan': 'porcelain',
        'ceramic': 'ceramic', 'keramik': 'ceramic',
        'glass': 'glass', 'glas': 'glass',
        'wood': 'wooden', 'wooden': 'wooden', 'holz': 'wooden', 'oak': 'oak',
        'metal': 'metal', 'metall': 'metal',
        'cotton': 'cotton', 'baumwolle': 'cotton',
        'linen': 'linen', 'leinen': 'linen',
        'paper': 'paper', 'papier': 'paper',
        'fabric': 'fabric', 'stoff': 'fabric',
        'felt': 'felt', 'filz': 'felt',
        'brass': 'brass', 'messing': 'brass',
        'copper': 'copper', 'kupfer': 'copper',
        'bamboo': 'bamboo', 'bambus': 'bamboo',
        'rattan': 'rattan', 'wicker': 'wicker',
        'concrete': 'concrete', 'beton': 'concrete',
        'marble': 'marble', 'marmor': 'marble',
        'stoneware': 'stoneware', 'steinzeug': 'stoneware',
    }
    name_lower = name.lower()
    for mat_key, mat_val in materials.items():
        if mat_key in name_lower:
            return mat_val
    return None

def extract_design_name(name):
    """Extract named design/collection"""
    designs = ['serena', 'goldy', 'sunny', 'rosaly', 'carey', 'sleepy', 'blinky',
               'lille', 'cadiz', 'dessau', 'fiori', 'stripes', 'dots', 'cambridge',
               'garden of wonders', 'poetic space', 'poetry', 'petits bonheurs']
    name_lower = name.lower()
    for design in designs:
        if design in name_lower:
            return design.title()
    return None

def extract_flower(name):
    """Extract flower type from name"""
    flowers = {
        'rose': 'rose', 'daisy': 'daisy', 'tulip': 'tulip', 'lily': 'lily',
        'sunflower': 'sunflower', 'poppy': 'poppy', 'violet': 'violet',
        'chrysanthemum': 'chrysanthemum', 'aster': 'aster', 'marigold': 'marigold',
        'narcissus': 'narcissus', 'daffodil': 'daffodil', 'snowdrop': 'snowdrop',
        'holly': 'holly', 'delphinium': 'delphinium', 'lavender': 'lavender',
        'peony': 'peony', 'orchid': 'orchid', 'blossom': 'blossom', 'flower': 'flower',
    }
    name_lower = name.lower()
    for flower_key, flower_val in flowers.items():
        if flower_key in name_lower:
            return flower_val
    return None

def format_dimensions(dims):
    """Format dimensions into readable string"""
    if not dims:
        return ""
    parts = []
    if 'diameter' in dims and 'height' in dims:
        return f"{dims['diameter']}cm wide and {dims['height']}cm tall"
    if 'diameter' in dims:
        parts.append(f"{dims['diameter']}cm in diameter")
    if 'height' in dims:
        parts.append(f"{dims['height']}cm tall")
    if 'length' in dims:
        parts.append(f"{dims['length']}cm long")
    if 'width' in dims:
        parts.append(f"{dims['width']}cm wide")
    if 'dim1' in dims and 'dim2' in dims:
        if 'dim3' in dims:
            return f"{dims['dim1']}x{dims['dim2']}x{dims['dim3']}cm"
        else:
            return f"{dims['dim1']}x{dims['dim2']}cm"
    if 'volume' in dims:
        parts.append(f"{dims['volume']} litre capacity")
    if 'ml' in dims:
        parts.append(f"{dims['ml']}ml capacity")
    return " and ".join(parts[:2])

def get_product_type_templates(name):
    """Get product type and multiple template options"""
    name_lower = name.lower()
    
    types = {
        'light house': ('light house', [
            "This enchanting light house glows warmly when illuminated, casting magical patterns through its delicate windows. A captivating centrepiece for cosy evenings.",
            "Watch this charming light house come alive when lit, creating atmospheric shadow play. The perfect companion for dark winter nights.",
            "This miniature light house creates a warm, inviting glow. The intricate window details cast beautiful light patterns on surrounding surfaces.",
        ]),
        'lichthaus': ('light house', [
            "This enchanting light house glows warmly when illuminated, casting magical patterns through its delicate windows. A captivating centrepiece for cosy evenings.",
            "Watch this charming light house come alive when lit, creating atmospheric shadow play. The perfect companion for dark winter nights.",
        ]),
        'poetry light': ('poetry light', [
            "This poetry light creates enchanting shadow play when illuminated. The delicate cutout design tells silent stories through light.",
            "Watch magical scenes unfold as candlelight dances through this poetry light's intricate cutouts. Pure atmosphere.",
        ]),
        'poesie': ('poetry light', [
            "This poetry light creates enchanting shadow play when illuminated. The delicate cutout design tells silent stories through light.",
        ]),
        'tealight holder': ('tealight holder', [
            "This tealight holder bathes your space in warm, flickering light. Creates an intimate atmosphere for relaxed evenings.",
            "Place a tealight inside and watch this holder transform your room with gentle, dancing shadows.",
            "This charming tealight holder adds instant warmth to any setting. Perfect for dinner parties or quiet nights in.",
        ]),
        'tealight': ('tealight holder', [
            "This tealight holder bathes your space in warm, flickering light. Creates an intimate atmosphere for relaxed evenings.",
        ]),
        'tea light': ('tealight holder', [
            "This tealight holder bathes your space in warm, flickering light. Creates an intimate atmosphere for relaxed evenings.",
        ]),
        'teelicht': ('tealight holder', [
            "This tealight holder bathes your space in warm, flickering light. Creates an intimate atmosphere for relaxed evenings.",
        ]),
        'candle holder': ('candle holder', [
            "This candle holder creates beautiful ambience for any occasion. The warm glow transforms ordinary moments into special ones.",
            "Elevate your space with this elegant candle holder. Perfect for romantic dinners or peaceful evenings.",
        ]),
        'candleholder': ('candle holder', [
            "This candle holder creates beautiful ambience for any occasion. The warm glow transforms ordinary moments into special ones.",
        ]),
        'candle bowl': ('candle bowl', [
            "This candle bowl holds floating candles or tealights beautifully. Creates mesmerising reflections as the flame dances.",
        ]),
        'vase': ('vase', [
            "This elegant vase showcases flowers beautifully, from single stems to full bouquets. Equally striking as a sculptural piece.",
            "Display your favourite blooms in this stunning vase. The thoughtful proportions suit everything from wildflowers to formal arrangements.",
            "This versatile vase brings joy whether holding fresh flowers, dried stems, or standing alone as a decorative accent.",
        ]),
        'bowl': ('bowl', [
            "This beautiful bowl serves many purposes - from holding fruit to displaying treasures. A versatile piece for any room.",
            "Use this charming bowl for serving, storage, or simply as a decorative accent. Form meets function beautifully.",
        ]),
        'plate': ('plate', [
            "This plate combines beauty with function. Perfect for serving favourite treats or as a decorative accent piece.",
            "A beautiful plate for everyday use or special occasions. Makes even simple moments feel considered.",
        ]),
        'platter': ('platter', [
            "This generous platter makes entertaining effortless. Present your culinary creations on this impressive centrepiece.",
        ]),
        'dish': ('dish', [
            "This lovely dish holds everything from trinkets to treats. A charming addition to any surface.",
        ]),
        'mug': ('mug', [
            "This charming mug makes every drink more enjoyable. The generous size is perfect for morning coffee or evening hot chocolate.",
            "Wrap your hands around this lovely mug and savour your favourite hot drinks. A daily pleasure.",
        ]),
        'cup': ('cup', [
            "This elegant cup elevates your daily tea or coffee ritual. Simple pleasures, beautifully presented.",
        ]),
        'espresso cup': ('espresso cup', [
            "This refined espresso cup is perfectly proportioned for your daily shot. Small but perfectly formed.",
        ]),
        'espresso': ('espresso cup', [
            "This refined espresso cup is perfectly proportioned for your daily shot. Small but perfectly formed.",
        ]),
        'napkin': ('napkins', [
            "These quality napkins add personality to your table setting. Practical style for everyday or special occasions.",
        ]),
        'serviette': ('napkins', [
            "These quality napkins add personality to your table setting. Practical style for everyday or special occasions.",
        ]),
        'chain': ('decorative chain', [
            "This decorative chain creates beautiful displays draped across mantles, wound through branches, or hung on walls.",
            "Add movement and charm with this lovely chain. Versatile enough for seasonal decorating or permanent display.",
        ]),
        'garland': ('garland', [
            "This charming garland adds instant atmosphere. Drape across doorways, mantles, or wind through table settings.",
        ]),
        'wreath': ('wreath', [
            "This beautiful wreath creates a welcoming display for doors, walls, or tables. A lasting alternative to fresh florals.",
        ]),
        'ornament': ('ornament', [
            "This decorative ornament adds charm wherever it hangs. Perfect for Christmas trees, windows, or year-round display.",
        ]),
        'hanger': ('hanging decoration', [
            "This hanging decoration catches the light and adds gentle movement. Beautiful on trees, in windows, or from branches.",
        ]),
        'figurine': ('figurine', [
            "This charming figurine brings character and warmth to shelves and surfaces. A delightful decorative accent.",
        ]),
        'figure': ('figurine', [
            "This charming figurine brings character and warmth to shelves and surfaces. A delightful decorative accent.",
        ]),
        'necklace': ('necklace', [
            "This elegant necklace sits beautifully at the collarbone. A meaningful piece for everyday wear or special occasions.",
        ]),
        'keyring': ('keyring', [
            "This charming keyring keeps your keys organised with personality. A small daily pleasure.",
        ]),
        'keychain': ('keyring', [
            "This charming keyring keeps your keys organised with personality. A small daily pleasure.",
        ]),
        'jar': ('jar', [
            "This elegant jar provides stylish storage for cotton balls, jewellery, or small treasures. Practical beauty.",
        ]),
        'box': ('storage box', [
            "This decorative box keeps treasures safe and organised. A beautiful addition to dressers and shelves.",
        ]),
        'basket': ('basket', [
            "This lovely basket combines beauty with practicality. Perfect for storage, display, or gift-giving.",
        ]),
        'blanket': ('blanket', [
            "This cosy blanket wraps you in warmth and style. Perfect for sofas, beds, or outdoor evenings.",
        ]),
        'cushion': ('cushion', [
            "This beautiful cushion adds comfort and character to sofas and chairs. A simple way to refresh any room.",
        ]),
        'coaster': ('coasters', [
            "These stylish coasters protect surfaces while adding charm to your drinks service. Practical with personality.",
        ]),
        'butter dish': ('butter dish', [
            "This butter dish keeps butter fresh and perfectly spreadable. A charming essential for breakfast tables.",
        ]),
        'egg cup': ('egg cup', [
            "This sweet egg cup makes breakfast more enjoyable. The perfect throne for your soft-boiled eggs.",
        ]),
        'jug': ('jug', [
            "This elegant jug pours beautifully and looks stunning on the table. Perfect for water, juice, or as a vase.",
        ]),
        'pitcher': ('pitcher', [
            "This lovely pitcher serves with style. A versatile piece for drinks, flowers, or display.",
        ]),
        'bottle stopper': ('bottle stopper', [
            "This decorative bottle stopper seals wine in style. A practical gift with personality.",
        ]),
        'bottle opener': ('bottle opener', [
            "This stylish bottle opener makes opening drinks a pleasure. A practical accessory with charm.",
        ]),
        'led light': ('LED light', [
            "This LED light creates magical atmosphere with a warm, battery-powered glow. Place anywhere without worrying about wires.",
        ]),
        'led': ('LED light', [
            "This LED light creates magical atmosphere with a warm, battery-powered glow. Place anywhere without worrying about wires.",
        ]),
        'lamp': ('lamp', [
            "This beautiful lamp casts a warm, inviting glow. Perfect for creating cosy atmospheres in any room.",
        ]),
        'bell': ('bell', [
            "This decorative bell chimes sweetly when touched. A charming addition to seasonal displays and Christmas trees.",
        ]),
        'nativity': ('nativity scene', [
            "This nativity scene captures the Christmas story with quiet elegance. A treasured centrepiece for the festive season.",
        ]),
        'advent calendar': ('Advent calendar', [
            "This beautiful Advent calendar makes counting down to Christmas a daily delight. A cherished family tradition.",
        ]),
        'advent': ('Advent decoration', [
            "This Advent piece helps count down to Christmas with style. A meaningful part of festive traditions.",
        ]),
        'card': ('greeting card', [
            "This beautiful card conveys your message with artistic flair. More meaningful than ordinary greetings.",
        ]),
        'cake server': ('cake server', [
            "This elegant cake server presents desserts with style. Makes celebrations feel extra special.",
        ]),
        'cake stand': ('cake stand', [
            "This beautiful cake stand displays your bakes impressively. The perfect stage for celebratory treats.",
        ]),
        'etagere': ('tiered stand', [
            "This elegant tiered stand displays treats beautifully. Perfect for afternoon tea or special gatherings.",
        ]),
        'spoon': ('serving spoon', [
            "This beautiful serving spoon elevates your table setting. A lovely gift for anyone who enjoys cooking.",
        ]),
        'salt': ('salt and pepper set', [
            "This set keeps seasonings at hand with style. A charming addition to any dining table.",
        ]),
        'pepper': ('salt and pepper set', [
            "This set keeps seasonings at hand with style. A charming addition to any dining table.",
        ]),
        'picture frame': ('picture frame', [
            "This elegant frame displays your cherished memories beautifully. A meaningful home for special photos.",
        ]),
        'photo frame': ('photo frame', [
            "This lovely frame showcases your precious photos with style. A heartfelt gift for treasured memories.",
        ]),
        'piggy bank': ('piggy bank', [
            "This charming piggy bank makes saving feel special. A thoughtful gift that encourages good habits.",
        ]),
        'money box': ('money box', [
            "This decorative money box encourages saving in style. A meaningful gift that keeps on giving.",
        ]),
        'board game': ('board game', [
            "This beautifully designed game brings people together. Perfect for quality time with family and friends.",
        ]),
        'game': ('game', [
            "This beautifully designed game brings people together. Perfect for quality time with family and friends.",
        ]),
        'chess': ('chess set', [
            "This elegant chess set combines strategy with style. A stunning gift for chess enthusiasts.",
        ]),
        'wine cooler': ('wine cooler', [
            "This elegant wine cooler keeps bottles perfectly chilled while looking stunning on the table.",
        ]),
        'wine glass': ('wine glass', [
            "This beautiful wine glass makes every sip feel special. Elegant enough for celebrations, lovely enough for everyday.",
        ]),
        'aroma lamp': ('aroma lamp', [
            "This aroma lamp fills your space with fragrance as the gentle warmth releases calming scents. Atmosphere and aroma combined.",
        ]),
        'aroma': ('aroma lamp', [
            "This aroma lamp fills your space with fragrance as the gentle warmth releases calming scents. Atmosphere and aroma combined.",
        ]),
        'diffuser': ('diffuser', [
            "This elegant diffuser spreads beautiful fragrance throughout your space. A stylish way to scent your home.",
        ]),
        'incense': ('incense holder', [
            "This incense holder keeps ash contained while releasing calming fragrance. Perfect for mindful moments.",
        ]),
        'air refresher': ('air refresher', [
            "This air refresher brings natural fragrance home. A beautiful and practical way to freshen any room.",
        ]),
        'candle': ('candle', [
            "This beautiful candle adds warmth and ambience to any space. The gentle flame creates instant atmosphere.",
        ]),
        'scented candle': ('scented candle', [
            "This scented candle fills your space with fragrance while creating warm ambience. A sensory pleasure.",
        ]),
        'soap': ('soap', [
            "This lovely soap makes handwashing a pleasure. Beautiful enough to display, practical enough for daily use.",
        ]),
        'hand cream': ('hand cream', [
            "This nourishing hand cream keeps hands soft and pampered. A little luxury for everyday care.",
        ]),
        'bag': ('bag', [
            "This charming bag combines style with practicality. Perfect for shopping, gifts, or everyday use.",
        ]),
        'pouch': ('pouch', [
            "This sweet pouch keeps small essentials organised. A practical accessory with personality.",
        ]),
        'purse': ('purse', [
            "This lovely purse keeps your essentials close in style. A beautiful everyday companion.",
        ]),
        'towel': ('towel', [
            "This quality towel combines softness with style. A practical piece that adds charm to bathrooms and kitchens.",
        ]),
        'apron': ('apron', [
            "This charming apron protects clothes while adding style to cooking. A lovely gift for anyone who loves the kitchen.",
        ]),
        'oven glove': ('oven glove', [
            "This practical oven glove protects hands while looking great in the kitchen. Safety meets style.",
        ]),
        'tea towel': ('tea towel', [
            "This lovely tea towel adds charm to your kitchen. Practical for drying and beautiful for display.",
        ]),
        'storage': ('storage container', [
            "This practical storage piece keeps items organised while looking beautiful. Form meets function.",
        ]),
        'tray': ('tray', [
            "This elegant tray makes serving a pleasure. Perfect for breakfast in bed, drinks, or display.",
        ]),
        'clock': ('clock', [
            "This beautiful clock keeps time with style. A functional piece that doubles as wall art.",
        ]),
        'mirror': ('mirror', [
            "This lovely mirror reflects light and adds depth to any room. A practical piece with decorative charm.",
        ]),
        'hook': ('hook', [
            "This charming hook keeps items organised while adding character to walls. Practical with personality.",
        ]),
        'hanger': ('hanger', [
            "This decorative hanger adds charm wherever it's placed. Beautiful for display or practical storage.",
        ]),
        'magnet': ('magnet', [
            "This charming magnet adds personality to fridges and magnetic surfaces. A small daily pleasure.",
        ]),
        'bookmark': ('bookmark', [
            "This elegant bookmark keeps your place in style. A thoughtful gift for book lovers.",
        ]),
        'notebook': ('notebook', [
            "This lovely notebook inspires writing and note-taking. Beautiful pages for your thoughts and ideas.",
        ]),
        'calendar': ('calendar', [
            "This beautiful calendar helps organise your year with style. A practical piece that adds charm to walls.",
        ]),
        'music box': ('music box', [
            "This enchanting music box plays a gentle melody when opened. A magical gift for all ages.",
        ]),
        'snow globe': ('snow globe', [
            "This magical snow globe creates a miniature winter wonderland. Shake and watch the snow dance.",
        ]),
        'mobile': ('mobile', [
            "This charming mobile adds gentle movement and visual interest. Beautiful for nurseries or any room.",
        ]),
        'windchime': ('wind chime', [
            "This melodic wind chime creates soothing sounds in the breeze. Brings peaceful music to gardens and patios.",
        ]),
        'bird feeder': ('bird feeder', [
            "This charming bird feeder attracts feathered friends to your garden. Enjoy nature up close.",
        ]),
        'plant pot': ('plant pot', [
            "This lovely plant pot showcases your greenery beautifully. The perfect home for houseplants.",
        ]),
        'flower pot': ('plant pot', [
            "This lovely plant pot showcases your greenery beautifully. The perfect home for houseplants.",
        ]),
        'planter': ('planter', [
            "This stylish planter displays plants beautifully. Brings the outdoors in with style.",
        ]),
    }
    
    for key, (ptype, templates) in types.items():
        if key in name_lower:
            return ptype, random.choice(templates)
    
    return None, None

def generate_description(product, brand):
    """Generate a description for a product"""
    name = product['name']
    
    # Extract all features
    dims = extract_dimensions(name)
    dim_str = format_dimensions(dims)
    qty = extract_quantity(name)
    color = extract_color(name)
    animal = extract_animal(name)
    theme = extract_theme(name)
    material = extract_material(name)
    design = extract_design_name(name)
    flower = extract_flower(name)
    ptype, base_desc = get_product_type_templates(name)
    
    parts = []
    
    # Build opener
    if ptype:
        article = 'An' if ptype[0].lower() in 'aeiou' else 'A'
        
        modifiers = []
        if color and color not in ['natural']:
            modifiers.append(color)
        if material:
            modifiers.append(material)
        if animal and animal not in ['angel', 'Santa', 'snowman']:
            modifiers.append(f"{animal}")
        if flower and flower != 'flower':
            modifiers.append(f"{flower}")
            
        if modifiers:
            mod_str = ' '.join(modifiers[:2])
            if animal and animal not in modifiers:
                opener = f"{article} {mod_str} {ptype} featuring a {animal} design"
            elif flower and flower not in modifiers:
                opener = f"{article} {mod_str} {ptype} with {flower} motif"
            else:
                opener = f"{article} {mod_str} {ptype}"
        else:
            if animal:
                opener = f"{article} charming {animal} {ptype}"
            elif flower:
                opener = f"{article} lovely {flower} {ptype}"
            elif design:
                opener = f"{article} {design} {ptype}"
            else:
                opener = f"{article} {ptype}"
        
        if dim_str:
            opener += f", measuring {dim_str}"
        
        parts.append(opener + ".")
        
        if base_desc:
            parts.append(base_desc)
    else:
        # Generic opener for unknown types
        clean_name = re.sub(r'\d+x\d+.*?cm|\d+cm|D\.\d+|H\.\d+|L\.\d+', '', name).strip()
        clean_name = re.sub(r'\s+', ' ', clean_name)
        
        if dim_str:
            parts.append(f"Measuring {dim_str}, this piece brings thoughtful design to your home.")
        else:
            parts.append("A beautifully crafted piece that brings warmth and character to any space.")
        
        parts.append("Designed with attention to detail and made to be treasured.")
    
    # Add quantity info
    if qty and int(qty) > 1:
        parts.append(f"This set includes {qty} pieces for a complete look.")
    
    # Theme-specific closings
    closings = {
        'Christmas': ["A treasured addition to your festive celebrations.", "Makes Christmas feel extra special.", "A beautiful part of holiday traditions."],
        'Advent': ["Makes the countdown to Christmas magical.", "A cherished part of Advent traditions."],
        'Easter': ["Perfect for spring celebrations and Easter displays.", "Brings Easter joy to your home."],
        'birthday': ["Makes birthday celebrations more memorable.", "A thoughtful birthday gift."],
        'wedding': ["A beautiful gift for newlyweds.", "Celebrates love and new beginnings."],
        'love': ["A romantic gift for someone special.", "Celebrates love beautifully."],
        'heart': ["A heartfelt gift for someone you love.", "Shares love in a tangible way."],
        'baby': ["A sweet welcome for new arrivals.", "A cherished gift for new parents."],
        "Valentine's": ["Perfect for Valentine's Day.", "A romantic gesture of love."],
        "Mother's Day": ["A thoughtful gift for Mother's Day.", "Shows appreciation beautifully."],
        "Father's Day": ["A meaningful Father's Day gift.", "Shows appreciation for Dad."],
    }
    
    if theme and theme in closings:
        parts.append(random.choice(closings[theme]))
    elif animal:
        animal_closings = [
            f"A delightful gift for {animal} lovers.",
            f"Perfect for anyone who adores {animal}s.",
            f"A charming gift for {animal} enthusiasts.",
        ]
        parts.append(random.choice(animal_closings))
    else:
        generic_closings = [
            "A thoughtful gift for someone special.",
            "A lovely addition to any home.",
            "Perfect for gifting or treating yourself.",
            "Makes everyday moments more beautiful.",
            "A beautiful accent for any room.",
            "Adds character and warmth to your space.",
        ]
        parts.append(random.choice(generic_closings))
    
    return " ".join(parts)

# Brand-specific adjustments
def adjust_for_brand(description, brand):
    """Make minor adjustments based on brand personality"""
    # These are subtle - we don't mention brand names in descriptions
    return description

# Process all products
print("Generating descriptions for all products...")
print("=" * 50)

brand_counts = {}
for product in data['products']:
    brand = product.get('brand', 'Unknown')
    if brand not in brand_counts:
        brand_counts[brand] = 0
    brand_counts[brand] += 1
    
    new_desc = generate_description(product, brand)
    new_desc = adjust_for_brand(new_desc, brand)
    product['description'] = new_desc

# Save
with open('/Users/matt/Desktop/home-and-verse/backend/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Generated descriptions for {len(data['products'])} products")
print("\nBy brand:")
for brand, count in sorted(brand_counts.items(), key=lambda x: -x[1]):
    print(f"  {brand}: {count}")
print("\n✓ Saved to products.json")
