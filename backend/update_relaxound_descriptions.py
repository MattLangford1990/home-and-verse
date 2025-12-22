import json

# Load products
with open('data/products.json') as f:
    data = json.load(f)

# Enhanced descriptions - more emotional, benefit-focused, call-to-action oriented
descriptions = {
    # ZWITSCHERBOX - Birdsong boxes
    "11ZBX0101004": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor. 

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. The bold red finish makes a cheerful statement piece that delivers joy with every passing.""",

    "11ZBX0200002": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. Crafted from sustainable bamboo, this eco-conscious choice brings natural materials together with natural sounds.""",

    "11ZBX0101002": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. Sleek black suits minimalist and contemporary interiors while bringing the timeless joy of birdsong into your space.""",

    "11ZBX0701004": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. The forest green finish and woodland imagery creates a visual celebration of the sounds within.""",

    "11ZBX0101018": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. Understated grey blends seamlessly into any décor while filling your space with refreshing birdsong.""",

    "11ZBX0201004": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. Real oak veneer brings natural warmth and texture, perfectly matched to the forest birdsong within.""",

    "11ZBX0301018": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. This special Robin Redbreast edition features Britain's favourite bird – a perfect gift for nature lovers.""",

    "11ZBX0301007": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. Soft violet creates a calming presence that complements the gentle bird melodies.""",

    "11ZBX0202007": """Transform any room into a woodland sanctuary. The Zwitscherbox is an award-winning German design that plays two minutes of authentic birdsong the moment you walk past – no buttons, no apps, just pure nature activated by motion sensor.

Perfect for the bathroom to start your morning with calm instead of chaos, the hallway to welcome you home after a stressful day, or the home office when you need a mental reset. The adjustable volume lets you set the perfect level, while three AA batteries last for months of gentle chirping.

Over 2 million sold worldwide – there's a reason this clever little box has become a modern classic. Rich dark walnut veneer adds a touch of sophistication while the birdsong within soothes the soul.""",

    # BIRDYBOX - Premium birdsong
    "11BBX0201003": """The Birdybox is the Zwitscherbox's sophisticated older sibling. Premium materials meet the same beloved birdsong in a larger, more refined package that makes a statement in any room.

Motion-activated for completely hands-free relaxation, it plays two minutes of authentic forest ambiance whenever you pass by. The rechargeable battery means no more hunting for AAs, and the enhanced speaker delivers richer, more immersive sound.

Place it in your bathroom for spa-like mornings, your hallway for a gentle welcome home, or your bedroom for a natural wake-up call. The steamed oak finish brings warmth and character to this premium sound experience.""",

    "11BBX0801002": """The Birdybox is the Zwitscherbox's sophisticated older sibling. Premium materials meet the same beloved birdsong in a larger, more refined package that makes a statement in any room.

Motion-activated for completely hands-free relaxation, it plays two minutes of authentic forest ambiance whenever you pass by. The rechargeable battery means no more hunting for AAs, and the enhanced speaker delivers richer, more immersive sound.

Place it in your bathroom for spa-like mornings, your hallway for a gentle welcome home, or your bedroom for a natural wake-up call. The contemporary terrazzo finish in warm toffee tones brings a designer touch to this nature-inspired piece.""",

    # OCEANBOX - Ocean sounds
    "11OBX0301005": """Close your eyes and you're there – waves rolling onto the shore, seagulls calling overhead, the rhythmic pulse of the tide. The Oceanbox brings 100 seconds of the seaside into your home, activated automatically by motion sensor every time you walk past.

It's the perfect escape for landlocked souls who dream of the coast. Mount it in your bathroom for an instant coastal spa experience, or let it transport your living room to the shoreline. The rechargeable battery and wall-mount design make installation effortless.

Inspired by the Baltic Sea, this special edition captures the gentle waves and distinctive calls of coastal seabirds. A thoughtful gift for anyone who finds peace by the water.""",

    "11OBX0201003": """Close your eyes and you're there – waves rolling onto the shore, seagulls calling overhead, the rhythmic pulse of the tide. The Oceanbox brings 100 seconds of the seaside into your home, activated automatically by motion sensor every time you walk past.

It's the perfect escape for landlocked souls who dream of the coast. Mount it in your bathroom for an instant coastal spa experience, or let it transport your living room to the shoreline. The rechargeable battery and wall-mount design make installation effortless.

Warm oak evokes a beachside cabin, driftwood found on the shore – natural materials that perfectly complement the ocean sounds within.""",

    "11OBX0201001": """Close your eyes and you're there – waves rolling onto the shore, seagulls calling overhead, the rhythmic pulse of the tide. The Oceanbox brings 100 seconds of the seaside into your home, activated automatically by motion sensor every time you walk past.

It's the perfect escape for landlocked souls who dream of the coast. Mount it in your bathroom for an instant coastal spa experience, or let it transport your living room to the shoreline. The rechargeable battery and wall-mount design make installation effortless.

The vintage design evokes classic British seaside holidays – candy stripes and nostalgic summers by the sea. A perfect gift for anyone with fond coastal memories.""",

    "11OBX0101001": """Close your eyes and you're there – waves rolling onto the shore, seagulls calling overhead, the rhythmic pulse of the tide. The Oceanbox brings 100 seconds of the seaside into your home, activated automatically by motion sensor every time you walk past.

It's the perfect escape for landlocked souls who dream of the coast. Mount it in your bathroom for an instant coastal spa experience, or let it transport your living room to the shoreline. The rechargeable battery and wall-mount design make installation effortless.

The wave pattern design creates a visual echo of the ocean sounds within – form and function in perfect harmony.""",

    "11OBX0101002": """Close your eyes and you're there – waves rolling onto the shore, seagulls calling overhead, the rhythmic pulse of the tide. The Oceanbox brings 100 seconds of the seaside into your home, activated automatically by motion sensor every time you walk past.

It's the perfect escape for landlocked souls who dream of the coast. Mount it in your bathroom for an instant coastal spa experience, or let it transport your living room to the shoreline. The rechargeable battery and wall-mount design make installation effortless.

Crisp white captures the clean freshness of sea spray and coastal cottages. A versatile choice that complements any bathroom or living space.""",

    # JUNGLEBOX - Rainforest sounds
    "11JGL0101003": """Escape to the rainforest without leaving your living room. The Junglebox plays 120 seconds of authentic Malaysian jungle ambiance – exotic birds calling through the canopy, insects humming in the undergrowth, distant wildlife rustling through tropical foliage.

It's a transportive experience that turns any room into a lush tropical sanctuary. Motion-activated and rechargeable, it triggers automatically whenever you pass by – no apps, no buttons, just instant immersion in nature's most biodiverse soundscape.

Perfect for home offices that need creative inspiration, meditation spaces seeking deeper calm, or anyone who dreams of tropical adventures. The lush green finish mirrors the verdant jungle it celebrates.""",

    "11JGL0701002": """Escape to the rainforest without leaving your living room. The Junglebox plays 120 seconds of authentic Malaysian jungle ambiance – exotic birds calling through the canopy, insects humming in the undergrowth, distant wildlife rustling through tropical foliage.

It's a transportive experience that turns any room into a lush tropical sanctuary. Motion-activated and rechargeable, it triggers automatically whenever you pass by – no apps, no buttons, just instant immersion in nature's most biodiverse soundscape.

Perfect for home offices that need creative inspiration, meditation spaces seeking deeper calm, or anyone who dreams of tropical adventures. Named for Malaysia's legendary Maliau Basin – the 'Lost World' of pristine rainforest captured in sound.""",

    "11JGL0201002": """Escape to the rainforest without leaving your living room. The Junglebox plays 120 seconds of authentic Malaysian jungle ambiance – exotic birds calling through the canopy, insects humming in the undergrowth, distant wildlife rustling through tropical foliage.

It's a transportive experience that turns any room into a lush tropical sanctuary. Motion-activated and rechargeable, it triggers automatically whenever you pass by – no apps, no buttons, just instant immersion in nature's most biodiverse soundscape.

Perfect for home offices that need creative inspiration, meditation spaces seeking deeper calm, or anyone who dreams of tropical adventures. Natural oak grounds the exotic sounds in familiar warmth – the perfect bridge between home and rainforest.""",

    "11JGL0101002": """Escape to the rainforest without leaving your living room. The Junglebox plays 120 seconds of authentic Malaysian jungle ambiance – exotic birds calling through the canopy, insects humming in the undergrowth, distant wildlife rustling through tropical foliage.

It's a transportive experience that turns any room into a lush tropical sanctuary. Motion-activated and rechargeable, it triggers automatically whenever you pass by – no apps, no buttons, just instant immersion in nature's most biodiverse soundscape.

Perfect for home offices that need creative inspiration, meditation spaces seeking deeper calm, or anyone who dreams of tropical adventures. Soft rosy pink brings an unexpected feminine touch to tropical escape – proving nature sounds suit every aesthetic.""",

    "11JGL0701001": """Escape to the rainforest without leaving your living room. The Junglebox plays 120 seconds of authentic Malaysian jungle ambiance – exotic birds calling through the canopy, insects humming in the undergrowth, distant wildlife rustling through tropical foliage.

It's a transportive experience that turns any room into a lush tropical sanctuary. Motion-activated and rechargeable, it triggers automatically whenever you pass by – no apps, no buttons, just instant immersion in nature's most biodiverse soundscape.

Perfect for home offices that need creative inspiration, meditation spaces seeking deeper calm, or anyone who dreams of tropical adventures. Vibrant tropical artwork wraps around the box – a visual feast that hints at the audio paradise within.""",

    "11JGL0101001": """Escape to the rainforest without leaving your living room. The Junglebox plays 120 seconds of authentic Malaysian jungle ambiance – exotic birds calling through the canopy, insects humming in the undergrowth, distant wildlife rustling through tropical foliage.

It's a transportive experience that turns any room into a lush tropical sanctuary. Motion-activated and rechargeable, it triggers automatically whenever you pass by – no apps, no buttons, just instant immersion in nature's most biodiverse soundscape.

Perfect for home offices that need creative inspiration, meditation spaces seeking deeper calm, or anyone who dreams of tropical adventures. Clean white creates a gallery-like frame for the exotic sounds within – minimalist design, maximum impact.""",

    # LAKESIDEBOX - Lake sounds
    "11LSB0201009": """Find yourself at a tranquil Scandinavian lake. Water gently lapping at the shore, birds calling across the still surface, crickets chirping in the reeds, a distant fish jumping. The Lakesidebox plays two minutes of this immersive soundscape whenever you walk past.

It's the sound of a perfect summer's day preserved forever – that moment when time seems to stop and stress melts away. Motion-activated and rechargeable, it brings effortless calm to bathrooms, bedrooms, home offices, or anywhere you need a moment of peace.

The birch-effect finish evokes the silver-barked trees that line Nordic lakeshores. A beautiful reminder to pause, breathe, and find stillness in a busy world.""",

    "11LSB0101004": """Find yourself at a tranquil Scandinavian lake. Water gently lapping at the shore, birds calling across the still surface, crickets chirping in the reeds, a distant fish jumping. The Lakesidebox plays two minutes of this immersive soundscape whenever you walk past.

It's the sound of a perfect summer's day preserved forever – that moment when time seems to stop and stress melts away. Motion-activated and rechargeable, it brings effortless calm to bathrooms, bedrooms, home offices, or anywhere you need a moment of peace.

Soft peach brings gentle warmth to your lakeside escape – a sunset glow that perfectly complements the peaceful sounds within.""",

    # ZIRPYBOX - Cricket sounds
    "11ZPB0701001": """Summer evenings captured in a box. The Zirpybox plays the gentle chirping of crickets and grasshoppers – that unmistakable soundtrack of warm nights and lazy afternoons in Mediterranean meadows.

Motion-activated and rechargeable, it brings the peaceful sounds of a sun-baked countryside into your home. Perfect for creating a relaxing atmosphere in bedrooms, living rooms, or anywhere you want to summon the feeling of endless summer.

The meadow green finish evokes sun-dappled grasslands buzzing with life. A unique and thoughtful gift for anyone who finds peace in nature's gentler sounds.""",

    "11ZPB0201001": """Summer evenings captured in a box. The Zirpybox plays the gentle chirping of crickets and grasshoppers – that unmistakable soundtrack of warm nights and lazy afternoons in Mediterranean meadows.

Motion-activated and rechargeable, it brings the peaceful sounds of a sun-baked countryside into your home. Perfect for creating a relaxing atmosphere in bedrooms, living rooms, or anywhere you want to summon the feeling of endless summer.

Natural wood finish grounds these summery sounds in earthy warmth. A unique and thoughtful gift for anyone who finds peace in nature's gentler sounds.""",

    # SATELLITEBOX
    "11NIG0101001": """The Satellitebox introduces the enchanting song of the nightingale – one of nature's most celebrated vocalists. This compact speaker plays the beautiful, complex melodies of the nightingale's evening serenade whenever you walk past.

Motion-activated and rechargeable, it brings an almost magical quality to any room. The nightingale's song has inspired poets and composers for centuries, and now you can enjoy it in your own home.

The forest green finish is a natural choice for housing these woodland songs. Perfect for bedrooms, hallways, or any space that could use a touch of natural poetry.""",
}

# Update products
updated_count = 0
for product in data['products']:
    sku = product.get('sku')
    if sku in descriptions:
        product['description'] = descriptions[sku]
        updated_count += 1
        print(f"Updated: {sku} - {product.get('name')}")

# Save
with open('data/products.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nUpdated {updated_count} Relaxound product descriptions!")
