import { useState, useEffect, useRef } from 'react';

// Stripe instance - truly lazy loaded (only on checkout)
let stripePromise = null;
const getStripe = async () => {
  if (!stripePromise) {
    // Dynamic import - only loads when checkout is accessed
    const { loadStripe } = await import('@stripe/stripe-js');
    stripePromise = loadStripe('pk_live_51QSVBJGaQyfTCKrLFj4BvIl9U3uyEfqOSNY5q7VZXOVGuxH6Vt50H2qiEadrJINCFcbq2oHVUzuhTHKC09sVBP3m001FdB3VE2');
  }
  return stripePromise;
};

const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';

// Cloudinary image helper - HIGH RES for website (quality customer experience)
const CLOUDINARY_BASE = 'https://res.cloudinary.com/dcfbgveei/image/upload';

// Pre-loaded image manifest - no network requests needed
const IMAGE_EXTRAS = {"EV03": ["EV03_04"], "HA210": ["HA210_230"], "KA25": ["KA25_230911", "KA25_240219"], "KT01": ["KT01_02"], "SK22": ["SK22_23"], "WB20": ["WB20_21"], "WKS29": ["WKS29_30"], "11873": ["11873_1"], "12442": ["12442_4", "12442_500"], "12619": ["12619_01", "12619_02"], "12927": ["12927_01", "12927_012", "12927_03", "12927_04"], "12928": ["12928_01", "12928_02", "12928_03", "12928_04"], "13179": ["13179_01", "13179_02", "13179_03"], "13614": ["13614_01", "13614_02", "13614_03", "13614_04"], "13615": ["13615_01", "13615_02", "13615_03", "13615_04"], "13802": ["13802_01", "13802_02", "13802_03", "13802_04"], "17302": ["17302_3", "17302_500"], "51180": ["51180_2", "51180_3", "51180_4", "51180_5"], "88292": ["88292_2"], "88683": ["88683_01", "88683_02", "88683_03", "88683_04"], "88684": ["88684_01", "88684_02", "88684_03", "88684_04"], "89840": ["89840_01", "89840_02", "89840_03"], "89851": ["89851_01"], "90299": ["90299_2", "90299_3"], "90308": ["90308_1"], "90440": ["90440_1"], "90598": ["90598_1"], "90752": ["90752_2"], "92169": ["92169_1"], "9479": ["9479_3", "9479_500"], "10021": ["10021_500"], "10454": ["10454_500"], "10756": ["10756_500"], "10791": ["10791_500"], "10793": ["10793_500"], "10843": ["10843_500"], "10844": ["10844_500"], "10845": ["10845_500"], "10846": ["10846_500"], "10847": ["10847_500"], "10848": ["10848_500"], "11221": ["11221_500"], "11326": ["11326_500"], "12166": ["12166_500"], "12405": ["12405_500"], "12439": ["12439_500"], "12551": ["12551_500"], "12556": ["12556_500"], "12563": ["12563_500"], "12957": ["12957_500"], "12958": ["12958_500"], "13140": ["13140_500"], "13145": ["13145_500"], "13146": ["13146_500"], "13185": ["13185_500"], "13188": ["13188_500"], "13609": ["13609_500"], "13914": ["13914_01", "13914_500"], "13915": ["13915_04", "13915_500"], "13916": ["13916_03", "13916_500"], "13917": ["13917_02", "13917_500"], "14134": ["14134_500"], "14135": ["14135_500"], "14136": ["14136_500"], "14186": ["14186_500"], "14187": ["14187_500"], "14188": ["14188_500"], "14273": ["14273_500"], "14279": ["14279_500"], "14280": ["14280_500"], "14343": ["14343_500"], "14383": ["14383_500"], "14402": ["14402_500"], "14404": ["14404_500"], "14446": ["14446_500"], "14725": ["14725_500"], "14812": ["14812_500"], "15111": ["15111_500"], "15113": ["15113_500"], "15114": ["15114_500"], "15115": ["15115_500"], "15116": ["15116_500"], "15152": ["15152_02"], "15153": ["15153_03"], "15154": ["15154_01"], "15169": ["15169_500"], "15349": ["15349_500"], "15405": ["15405_500"], "15406": ["15406_500"], "15407": ["15407_500"], "15417": ["15417_500"], "15428": ["15428_500"], "15468": ["15468_500"], "15501": ["15501_500"], "15516": ["15516_500"], "15517": ["15517_500"], "15518": ["15518_500"], "15583": ["15583_500"], "15730": ["15730_500"], "15731": ["15731_500"], "15732": ["15732_500"], "16051": ["16051_500"], "16221": ["16221_500"], "16223": ["16223_500"], "16342": ["16342_500"], "16458": ["16458_500"], "16459": ["16459_500"], "16460": ["16460_500"], "16465": ["16465_500"], "16731": ["16731_500"], "16779": ["16779_500"], "16794": ["16794_500"], "16795": ["16795_500"], "16848": ["16848_500"], "16851": ["16851_500"], "16858": ["16858_500"], "16873": ["16873_500"], "16945": ["16945_500"], "17008": ["17008_500"], "17010": ["17010_500"], "17017": ["17017_500"], "17056": ["17056_500"], "17188": ["17188_500"], "17230": ["17230_500"], "17231": ["17231_500"], "17253": ["17253_500"], "17254": ["17254_500"], "17282": ["17282_500"], "17303": ["17303_500"], "17313": ["17313_500"], "17348": ["17348_500"], "17354": ["17354_500"], "17356": ["17356_500"], "17360": ["17360_500"], "17361": ["17361_500"], "17371": ["17371_500"], "17392": ["17392_500"], "17416": ["17416_500"], "17419": ["17419_500"], "17429": ["17429_500"], "17430": ["17430_500"], "17438": ["17438_500"], "17453": ["17453_500"], "17504": ["17504_500"], "17513": ["17513_500"], "17514": ["17514_500"], "17518": ["17518_500"], "17520": ["17520_500"], "17538": ["17538_500"], "17550": ["17550_500"], "17567": ["17567_500"], "17568": ["17568_500"], "17569": ["17569_500"], "17570": ["17570_500"], "17582": ["17582_500"], "17583": ["17583_500"], "17595": ["17595_500"], "17613": ["17613_500"], "17614": ["17614_500"], "17615": ["17615_500"], "17616": ["17616_500"], "17618": ["17618_500"], "17619": ["17619_500"], "17634": ["17634_500"], "17663": ["17663_500"], "17670": ["17670_500"], "17679": ["17679_500"], "17685": ["17685_500"], "17703": ["17703_500"], "17709": ["17709_500"], "17710": ["17710_500"], "17713": ["17713_500"], "17715": ["17715_500"], "17746": ["17746_500"], "17747": ["17747_500"], "17786": ["17786_500"], "17794": ["17794_500"], "17841": ["17841_500"], "17866": ["17866_500"], "17873": ["17873_500"], "17874": ["17874_500"], "17875": ["17875_500"], "17876": ["17876_500"], "17877": ["17877_500"], "17898": ["17898_500"], "17899": ["17899_500"], "17943": ["17943_500"], "17996": ["17996_500"], "18011": ["18011_500"], "18013": ["18013_500"], "18014": ["18014_500"], "18020": ["18020_500"], "18021": ["18021_500"], "18026": ["18026_500"], "18033": ["18033_500"], "18035": ["18035_500"], "18037": ["18037_500"], "18038": ["18038_500"], "18039": ["18039_500"], "18040": ["18040_500"], "18041": ["18041_500"], "18042": ["18042_500"], "18043": ["18043_500"], "18044": ["18044_500"], "18045": ["18045_500"], "18046": ["18046_500"], "18047": ["18047_500"], "18051": ["18051_500"], "18052": ["18052_500"], "18070": ["18070_500"], "18071": ["18071_500"], "18073": ["18073_500"], "18074": ["18074_500"], "18075": ["18075_500"], "18076": ["18076_500"], "18079": ["18079_500"], "18081": ["18081_500"], "18082": ["18082_500"], "18085": ["18085_500"], "18087": ["18087_500"], "18094": ["18094_500"], "18122": ["18122_500"], "18150": ["18150_500"], "18156": ["18156_500"], "18164": ["18164_500"], "18166": ["18166_500"], "18167": ["18167_500"], "18169": ["18169_500"], "18172": ["18172_500"], "18173": ["18173_500"], "18175": ["18175_500"], "18177": ["18177_500"], "18180": ["18180_500"], "18198": ["18198_500"], "18199": ["18199_500"], "18200": ["18200_500"], "18201": ["18201_500"], "18203": ["18203_500"], "18204": ["18204_500"], "18209": ["18209_500"], "18210": ["18210_500"], "18211": ["18211_500"], "18213": ["18213_01", "18213_500"], "18214": ["18214_500"], "18226": ["18226_500"], "18227": ["18227_500"], "18228": ["18228_500"], "18229": ["18229_500"], "18247": ["18247_500"], "18248": ["18248_500"], "18269": ["18269_500"], "18270": ["18270_500"], "18271": ["18271_500"], "18272": ["18272_500"], "18273": ["18273_500"], "18274": ["18274_500"], "18284": ["18284_500"], "18286": ["18286_500"], "18288": ["18288_500"], "18291": ["18291_500"], "18300": ["18300_500"], "18309": ["18309_500"], "18316": ["18316_500"], "18325": ["18325_500"], "18331": ["18331_500"], "18335": ["18335_500"], "18338": ["18338_500"], "18342": ["18342_500"], "18343": ["18343_500"], "18344": ["18344_500"], "18348": ["18348_500"], "18349": ["18349_500"], "18359": ["18359_500"], "18360": ["18360_500"], "18365": ["18365_500"], "18366": ["18366_500"], "18367": ["18367_500"], "18369": ["18369_500"], "18370": ["18370_500"], "18371": ["18371_500"], "18374": ["18374_500"], "18378": ["18378_500"], "18379": ["18379_500"], "18380": ["18380_500"], "18381": ["18381_500"], "18397": ["18397_500"], "18398": ["18398_500"], "51240": ["51240_1200"], "51241": ["51241_1200"], "51242": ["51242_1200"], "51244": ["51244_1200"], "51245": ["51245_1200"], "51260": ["51260_1200"], "51265": ["51265_1200"], "51266": ["51266_3526"], "51268": ["51268_2"], "51284": ["51284_2647"], "51287": ["51287_1200"], "51370": ["51370_1"], "51371": ["51371_1"], "51372": ["51372_1"], "51373": ["51373_1"], "51374": ["51374_1"], "51375": ["51375_4"], "51391": ["51391_1200"], "51394": ["51394_1200"], "51420": ["51420_500"], "51430": ["51430_1200"], "51431": ["51431_1200"], "51432": ["51432_1200"], "51433": ["51433_1200"], "51434": ["51434_1200"], "51435": ["51435_1200"], "51450": ["51450_1"], "51452": ["51452_2"], "51471": ["51471_2"], "51556": ["51556_500"], "51599": ["51599_500"], "51600": ["51600_500"], "51601": ["51601_500"], "51602": ["51602_500"], "51603": ["51603_500"], "51754": ["51754_500"], "51755": ["51755_500"], "51756": ["51756_500"], "51757": ["51757_500"], "88950": ["88950_500"], "89023": ["89023_500"], "89572": ["89572_04"], "89576": ["89576_01", "89576_02", "89576_03", "89576_04"], "89577": ["89577_02", "89577_03", "89577_04"], "89802": ["89802_500"], "89803": ["89803_500"], "89804": ["89804_500"], "89805": ["89805_500"], "90337": ["90337_500"], "90338": ["90338_500"], "90340": ["90340_500"], "90341": ["90341_500"], "90446": ["90446_500"], "90535": ["90535_500"], "90536": ["90536_500"], "90629": ["90629_500"], "90682": ["90682_500"], "90683": ["90683_500"], "90694": ["90694_500"], "90699": ["90699_500"], "90704": ["90704_500"], "92144": ["92144_500"], "92182": ["92182_500"], "92227": ["92227_500"], "92302": ["92302_001"], "92547": ["92547_500"], "92589": ["92589_500"], "92590": ["92590_500"], "9735": ["9735_500"]};

// Relaxound sound files mapping
const RELAXOUND_SOUNDS = {
  'zwitscherbox': 'https://res.cloudinary.com/dcfbgveei/video/upload/sounds/zwitscherbox.mp3',
  'birdybox': 'https://res.cloudinary.com/dcfbgveei/video/upload/sounds/zwitscherbox.mp3',
  'lakesidebox': 'https://res.cloudinary.com/dcfbgveei/video/upload/sounds/lakesidebox.mp3',
  'oceanbox': 'https://res.cloudinary.com/dcfbgveei/video/upload/sounds/oceanbox.mp3',
  'seabird': 'https://res.cloudinary.com/dcfbgveei/video/upload/sounds/oceanbox.mp3',
  'junglebox': 'https://res.cloudinary.com/dcfbgveei/video/upload/sounds/junglebox.mp3',
};

const getRelaxoundSound = (productName) => {
  const nameLower = productName.toLowerCase();
  for (const [key, url] of Object.entries(RELAXOUND_SOUNDS)) {
    if (nameLower.includes(key)) return url;
  }
  // Default to zwitscherbox for other Relaxound products
  return RELAXOUND_SOUNDS.zwitscherbox;
};

const getImageUrl = (imagePath, size = 'medium') => {
  if (!imagePath) return null;
  
  // Size presets - high quality for website
  const transforms = {
    large: 'w_1200,q_85,f_auto',     // Product page / lightbox - full quality
    medium: 'w_600,q_80,f_auto',     // Product cards
    thumb: 'w_150,q_70,f_auto',      // Thumbnails
  };
  
  // If it's already a full Cloudinary URL, insert transforms after /upload/
  if (imagePath.includes('res.cloudinary.com')) {
    return imagePath.replace('/upload/', `/upload/${transforms[size] || transforms.medium}/`);
  }
  
  // Otherwise, build URL from path like /images/SKU.jpg
  const filename = imagePath.split('/').pop();
  const sku = filename.replace(/\.(jpg|jpeg|png)$/i, '');
  return `${CLOUDINARY_BASE}/${transforms[size] || transforms.medium}/products/${sku}.jpg`;
};

// Categories - must match Zoho data exactly
const NAV_CATEGORIES = [
  { name: 'Christmas', slug: 'Christmas' },
  { name: 'Candles & Fragrance', slug: 'Candles & Fragrance' },
  { name: 'Lighting', slug: 'Lighting' },
  { name: 'Tableware', slug: 'Tableware' },
  { name: 'Home Décor', slug: 'Home Décor' },
  { name: 'Gifts', slug: 'Gifts' },
];

export default function App() {
  const [products, setProducts] = useState([]);
  const [allProducts, setAllProducts] = useState([]);
  const [bestsellers, setBestsellers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [activeCategory, setActiveCategory] = useState(null);
  const [activeBrand, setActiveBrand] = useState(null);
  const [brandsDropdownOpen, setBrandsDropdownOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('popularity');
  const [priceRange, setPriceRange] = useState([0, 500]);
  
  // Brands list
  const BRANDS = ['Räder', 'Remember', 'My Flame', 'Relaxound', 'Ideas4Seasons', 'Elvang'];
  
  const [cart, setCart] = useState([]);
  const [cartOpen, setCartOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [view, setView] = useState('home');
  const [searchOpen, setSearchOpen] = useState(false);
  const [checkoutView, setCheckoutView] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  useEffect(() => { fetchData(); }, []);
  useEffect(() => { filterProducts(); }, [allProducts, activeCategory, activeBrand, searchQuery, sortBy, priceRange]);
  
  // SEO: Update page title and meta based on current view
  useEffect(() => {
    const baseTitle = 'Home & Verse';
    const baseSuffix = ' | Luxury European Homeware';
    let newTitle = baseTitle + baseSuffix;
    let newDescription = 'Discover our curated collection of luxury European homeware from Räder, Remember, My Flame and Relaxound.';
    
    if (view === 'product' && selectedProduct) {
      newTitle = `${selectedProduct.name} by ${selectedProduct.brand} | ${baseTitle}`;
      newDescription = selectedProduct.description || `Shop ${selectedProduct.name} from ${selectedProduct.brand} at Home & Verse. £${selectedProduct.price?.toFixed(2)}. Free UK delivery over £30.`;
      
      // Inject product schema
      updateProductSchema(selectedProduct);
    } else if (view === 'products' && activeCategory) {
      const catName = NAV_CATEGORIES.find(c => c.slug === activeCategory)?.name || activeCategory;
      newTitle = `${catName} | ${baseTitle}`;
      // Category-specific SEO descriptions
      const catDescriptions = {
        'Christmas': 'Shop Christmas decorations, porcelain light houses, festive candles & seasonal gifts. German-designed Christmas homeware from Räder, Remember & more. Free UK delivery over £30.',
        'Candles & Fragrance': 'Luxury soy candles with hidden messages, fragrance diffusers & home scents. Hand-poured Dutch candles from My Flame. Free UK delivery over £30.',
        'Lighting': 'Atmospheric lighting, porcelain candle houses & decorative light objects. German-designed Räder light houses & seasonal illumination. Free UK delivery over £30.',
        'Tableware': 'European tableware, porcelain plates, bowls & dining accessories. Luxury German & Dutch design for your table. Free UK delivery over £30.',
        'Home Décor': 'Unique home decorations, ornaments & interior accessories. European-designed homeware from Räder, Remember & Relaxound. Free UK delivery over £30.',
        'Gifts': 'Unique European gifts for every occasion. Zwitscherbox birdsong boxes, hidden message candles & luxury homeware. Free UK delivery over £30.'
      };
      newDescription = catDescriptions[catName] || `Shop our ${catName.toLowerCase()} collection. Luxury European homeware from Räder, Remember, My Flame and Relaxound. Free UK delivery over £30.`;
      removeProductSchema();
    } else if (view === 'products' && activeBrand) {
      // Brand-specific SEO
      newTitle = `${activeBrand} UK | Shop ${activeBrand} at ${baseTitle}`;
      const brandDescriptions = {
        'Räder': 'Shop Räder UK - German porcelain, atmospheric lighting & iconic light houses since 1990. Official UK stockist. Free delivery over £30.',
        'Remember': 'Shop Remember UK - Bold, colourful German homeware & gifts. Vibrant designs that celebrate colour & pattern. Official UK stockist.',
        'My Flame': 'Shop My Flame UK - Dutch hand-poured soy candles with hidden messages. Natural wax, beautiful fragrances. Official UK stockist.',
        'Relaxound': 'Shop Relaxound UK - Home of the original Zwitscherbox birdsong box. German-designed nature soundboxes. Official UK stockist.',
        'Ideas4Seasons': 'Shop Ideas4Seasons UK - Seasonal decorations & festive homeware for every occasion. Official UK stockist.',
        'Elvang': 'Shop Elvang UK - Luxurious Danish throws, cushions & scarves in premium alpaca wool. Timeless Scandinavian design. Official UK stockist.'
      };
      newDescription = brandDescriptions[activeBrand] || `Shop ${activeBrand} products at Home & Verse. Official UK stockist. Free delivery over £30.`;
      removeProductSchema();
    } else if (view === 'about') {
      newTitle = `Our Story | ${baseTitle}`;
      newDescription = 'Home & Verse brings together luxury European homeware from Räder, Remember, My Flame and Relaxound. Based in the UK.';
      removeProductSchema();
    } else if (view === 'privacy') {
      newTitle = `Privacy Policy | ${baseTitle}`;
      newDescription = 'How Home & Verse collects, uses and protects your personal data. Your privacy rights under UK GDPR.';
      removeProductSchema();
    } else if (view === 'terms') {
      newTitle = `Terms & Conditions | ${baseTitle}`;
      newDescription = 'Terms and conditions for shopping at Home & Verse. Ordering, delivery, returns and your consumer rights.';
      removeProductSchema();
    } else if (view === 'cookies') {
      newTitle = `Cookie Policy | ${baseTitle}`;
      newDescription = 'How Home & Verse uses cookies on our website. Essential and analytics cookies explained.';
      removeProductSchema();
    } else {
      removeProductSchema();
    }
    
    document.title = newTitle;
    
    // Update meta description
    let metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute('content', newDescription);
    
    // Update OG tags
    let ogTitle = document.querySelector('meta[property="og:title"]');
    let ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogTitle) ogTitle.setAttribute('content', newTitle);
    if (ogDesc) ogDesc.setAttribute('content', newDescription);
    
  }, [view, selectedProduct, activeCategory, activeBrand]); // SEO: updates on view/product/category/brand changes
  
  // SEO: Product structured data
  const updateProductSchema = (product) => {
    removeProductSchema();
    if (!product) return;
    
    // Get primary category for breadcrumb
    const primaryCategory = product.categories?.[0] || 'Home Décor';
    
    const schema = {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Product",
          "name": product.name,
          "description": product.description || `${product.name} by ${product.brand}`,
          "sku": product.sku,
          "brand": {
            "@type": "Brand",
            "name": product.brand
          },
          "offers": {
            "@type": "Offer",
            "url": window.location.href,
            "priceCurrency": "GBP",
            "price": product.price,
            "priceValidUntil": new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            "availability": product.in_stock ? "https://schema.org/InStock" : "https://schema.org/OutOfStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {
              "@type": "Organization",
              "name": "Home & Verse"
            },
            "shippingDetails": [
              {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                  "@type": "MonetaryAmount",
                  "value": product.price >= 30 ? 0 : 4.99,
                  "currency": "GBP"
                },
                "shippingDestination": {
                  "@type": "DefinedRegion",
                  "addressCountry": "GB"
                },
                "deliveryTime": {
                  "@type": "ShippingDeliveryTime",
                  "handlingTime": {
                    "@type": "QuantitativeValue",
                    "minValue": 0,
                    "maxValue": 1,
                    "unitCode": "d"
                  },
                  "transitTime": {
                    "@type": "QuantitativeValue",
                    "minValue": 2,
                    "maxValue": 4,
                    "unitCode": "d"
                  }
                }
              },
              {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                  "@type": "MonetaryAmount",
                  "value": 14.99,
                  "currency": "GBP"
                },
                "shippingDestination": [
                  { "@type": "DefinedRegion", "addressCountry": ["DE", "FR", "IT", "ES", "NL", "BE", "AT", "IE", "PL", "PT", "SE", "DK", "FI", "NO", "CH"] },
                  { "@type": "DefinedRegion", "addressCountry": ["US", "CA"] }
                ],
                "deliveryTime": {
                  "@type": "ShippingDeliveryTime",
                  "handlingTime": {
                    "@type": "QuantitativeValue",
                    "minValue": 1,
                    "maxValue": 2,
                    "unitCode": "d"
                  },
                  "transitTime": {
                    "@type": "QuantitativeValue",
                    "minValue": 5,
                    "maxValue": 10,
                    "unitCode": "d"
                  }
                }
              }
            ],
            "hasMerchantReturnPolicy": {
              "@type": "MerchantReturnPolicy",
              "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
              "merchantReturnDays": 30,
              "returnMethod": "https://schema.org/ReturnByMail",
              "returnFees": "https://schema.org/FreeReturn"
            }
          }
        },
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Home",
              "item": "https://www.homeandverse.co.uk/"
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": primaryCategory,
              "item": `https://www.homeandverse.co.uk/category/${primaryCategory.toLowerCase().replace(/ /g, '-').replace(/&/g, 'and')}`
            },
            {
              "@type": "ListItem",
              "position": 3,
              "name": product.name
            }
          ]
        }
      ]
    };
    
    // Add image if available
    if (product.image_url) {
      schema["@graph"][0].image = getImageUrl(product.image_url, 'large');
    }
    
    // Add GTIN/EAN if available
    if (product.ean) {
      schema["@graph"][0].gtin13 = product.ean;
    }
    
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.id = 'product-schema';
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  };
  
  const removeProductSchema = () => {
    const existing = document.getElementById('product-schema');
    if (existing) existing.remove();
  };
  
  const fetchData = async () => {
    try {
      const [productsRes, bestsellersRes] = await Promise.all([
        fetch(`${API_BASE}/api/products?in_stock_only=true`),
        fetch(`${API_BASE}/api/bestsellers?limit=50&in_stock_only=true`).catch(() => null)
      ]);
      
      const productsData = await productsRes.json();
      setAllProducts(productsData.products);
      setProducts(productsData.products);
      
      if (bestsellersRes?.ok) {
        const bestsellersData = await bestsellersRes.json();
        setBestsellers(bestsellersData.bestsellers || []);
      }
      
      setError(null);
    } catch (err) {
      setError('Unable to connect');
    }
    setLoading(false);
  };
  
  const filterProducts = () => {
    let filtered = [...allProducts];
    if (activeCategory) {
      // Products can be in multiple categories - check if activeCategory is in the array
      filtered = filtered.filter(p => {
        const cats = p.categories || [p.category];
        return cats.some(c => c.toLowerCase() === activeCategory.toLowerCase());
      });
    }
    if (activeBrand) {
      filtered = filtered.filter(p => p.brand === activeBrand);
    }
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter(p => p.name.toLowerCase().includes(q) || p.sku.toLowerCase().includes(q));
    }
    filtered = filtered.filter(p => p.price >= priceRange[0] && p.price <= priceRange[1]);
    
    // Sorting
    if (sortBy === 'popularity') {
      // For Christmas, show a varied mix of festive items
      if (activeCategory && activeCategory.toLowerCase() === 'christmas') {
        // Group products by keyword type for variety
        const keywordGroups = {
          light: [],
          house: [],
          santa: [],
          christmas: [],
          candle: [],
          star: [],
          angel: [],
          tree: [],
          other: []
        };
        
        filtered.forEach(p => {
          const name = (p.name || '').toLowerCase();
          let placed = false;
          for (const keyword of ['light', 'house', 'santa', 'christmas', 'candle', 'star', 'angel', 'tree']) {
            if (name.includes(keyword) && !placed) {
              keywordGroups[keyword].push(p);
              placed = true;
            }
          }
          if (!placed) keywordGroups.other.push(p);
        });
        
        // Sort each group by popularity
        Object.keys(keywordGroups).forEach(key => {
          keywordGroups[key].sort((a, b) => (b.popularity_score || 50) - (a.popularity_score || 50));
        });
        
        // Interleave groups for variety - round robin through groups
        const result = [];
        const groupKeys = ['light', 'house', 'santa', 'christmas', 'candle', 'star', 'angel', 'tree', 'other'];
        let maxLen = Math.max(...groupKeys.map(k => keywordGroups[k].length));
        
        for (let i = 0; i < maxLen; i++) {
          for (const key of groupKeys) {
            if (keywordGroups[key][i]) {
              result.push(keywordGroups[key][i]);
            }
          }
        }
        
        filtered = result;
      } else {
        filtered.sort((a, b) => (b.popularity_score || 50) - (a.popularity_score || 50));
      }
    } else if (sortBy === 'price-asc') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-desc') {
      filtered.sort((a, b) => b.price - a.price);
    } else {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    }
    
    setProducts(filtered);
  };
  
  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.sku === product.sku);
      if (existing) return prev.map(item => item.sku === product.sku ? {...item, quantity: item.quantity + 1} : item);
      return [...prev, {...product, quantity: 1}];
    });
    setCartOpen(true);
  };
  
  const updateQuantity = (sku, qty) => {
    if (qty <= 0) setCart(prev => prev.filter(item => item.sku !== sku));
    else setCart(prev => prev.map(item => item.sku === sku ? {...item, quantity: qty} : item));
  };
  
  const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
  const freeShipping = cartTotal >= 30;
  const shippingCost = freeShipping ? 0 : 4.99;
  const orderTotal = cartTotal + shippingCost;
  
  const navigateTo = (category) => {
    setActiveCategory(category);
    setActiveBrand(null);
    setView('products');
    setSearchQuery('');
    window.scrollTo(0, 0);
  };
  
  const navigateToBrand = (brand) => {
    setActiveBrand(brand);
    setActiveCategory(null);
    setView('products');
    setSearchQuery('');
    setBrandsDropdownOpen(false);
    window.scrollTo(0, 0);
  };
  
  const goHome = () => {
    setView('home');
    setActiveCategory(null);
    setActiveBrand(null);
    setSearchQuery('');
    setCheckoutView(false);
    window.scrollTo(0, 0);
  };
  
  const openProduct = (product) => {
    setSelectedProduct(product);
    setView('product');
    window.scrollTo(0, 0);
  };
  
  const startCheckout = () => {
    setCartOpen(false);
    setCheckoutView(true);
    setView('checkout');
    window.scrollTo(0, 0);
  };

  const getCategoryCount = (cat) => {
    return allProducts.filter(p => {
      const cats = p.categories || [p.category];
      return cats.some(c => c && c.toLowerCase() === cat.toLowerCase());
    }).length;
  };

  if (error && !allProducts.length) {
    return (
      <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 40}}>
        <div style={{textAlign: 'center', maxWidth: 420}}>
          <h1 style={{fontSize: 20, fontWeight: 500, marginBottom: 16}}>Home & Verse</h1>
          <p style={{color: '#666', marginBottom: 20}}>Start the backend server to view products</p>
          <code style={{display: 'block', background: '#f5f5f5', padding: 16, borderRadius: 4, fontSize: 12, textAlign: 'left'}}>
            cd ~/Desktop/home-and-verse/backend<br/>
            python3 -m uvicorn main:app --port 8000
          </code>
        </div>
      </div>
    );
  }

  return (
    <div style={{minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
      {/* Christmas Banner */}
      <div style={{background: '#1a472a', color: '#fff', padding: '10px 20px', fontSize: 13, textAlign: 'center'}}>
        🎄 Merry Christmas! Orders will be dispatched from 5th January 2026 🎄
      </div>
      
      {/* Announcement Bar */}
      <div style={{background: '#222', color: '#fff', padding: '8px 20px', fontSize: 12, textAlign: 'center'}}>
        Free UK delivery on orders over £30 · 30-day returns
      </div>
      
      {/* Header */}
      <header style={{borderBottom: '1px solid #e5e5e5', background: '#fff', position: 'sticky', top: 0, zIndex: 100}}>
        <div style={{maxWidth: 1400, margin: '0 auto', padding: '0 20px'}}>
          {/* Logo Row */}
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 60}}>
            <button 
              className="mobile-menu-btn"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)} 
              style={{...iconBtn, display: 'none', width: 40}}
              aria-label="Menu"
            >
              {mobileMenuOpen ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
              )}
            </button>
            <div className="desktop-spacer" style={{width: 100}}/>
            <div onClick={goHome} style={{fontSize: 18, fontWeight: 600, letterSpacing: '0.5px', cursor: 'pointer'}} role="banner" aria-label="Home & Verse - Go to homepage">
              HOME & VERSE
            </div>
            <div style={{display: 'flex', alignItems: 'center', gap: 16, width: 100, justifyContent: 'flex-end'}}>
              <button onClick={() => setSearchOpen(!searchOpen)} style={iconBtn} aria-label="Search">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              </button>
              <button style={iconBtn} aria-label="Account">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </button>
              <button onClick={() => setCartOpen(true)} style={{...iconBtn, position: 'relative'}} aria-label={`Shopping bag with ${cartCount} items`}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                {cartCount > 0 && <span style={cartBadge}>{cartCount}</span>}
              </button>
            </div>
          </div>
          
          {/* Navigation - Desktop */}
          <nav className="desktop-nav" aria-label="Main navigation" style={{display: 'flex', justifyContent: 'center', gap: 28, borderTop: '1px solid #f0f0f0', paddingTop: 12, paddingBottom: 12}}>
            <button onClick={() => { setActiveCategory(null); setActiveBrand(null); setView('products'); }} style={navBtn(activeCategory === null && activeBrand === null && view === 'products')}>
              New In
            </button>
            {NAV_CATEGORIES.map(cat => (
              <button key={cat.slug} onClick={() => navigateTo(cat.slug)} style={navBtn(activeCategory === cat.slug)}>
                {cat.name}
              </button>
            ))}
            {/* Brands Dropdown */}
            <div 
              style={{position: 'relative'}}
              onMouseEnter={() => setBrandsDropdownOpen(true)}
              onMouseLeave={() => setBrandsDropdownOpen(false)}
            >
              <button style={{...navBtn(activeBrand !== null), display: 'flex', alignItems: 'center', gap: 4}}>
                {activeBrand || 'Brands'}
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="m6 9 6 6 6-6"/>
                </svg>
              </button>
              {brandsDropdownOpen && (
                <div style={{
                  position: 'absolute',
                  top: '100%',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  background: '#fff',
                  border: '1px solid #e5e5e5',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                  padding: '8px 0',
                  minWidth: 160,
                  zIndex: 50
                }}>
                  {BRANDS.map(brand => (
                    <button 
                      key={brand}
                      onClick={() => navigateToBrand(brand)}
                      style={{
                        display: 'block',
                        width: '100%',
                        padding: '10px 20px',
                        background: activeBrand === brand ? '#f5f5f5' : 'none',
                        border: 'none',
                        textAlign: 'left',
                        fontSize: 13,
                        cursor: 'pointer',
                        color: '#222'
                      }}
                      onMouseOver={e => e.currentTarget.style.background = '#f5f5f5'}
                      onMouseOut={e => e.currentTarget.style.background = activeBrand === brand ? '#f5f5f5' : 'none'}
                    >
                      {brand}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </nav>
        </div>
        
        {/* Search Dropdown */}
        {searchOpen && (
          <div style={{borderTop: '1px solid #e5e5e5', padding: '16px 20px', background: '#fafafa'}}>
            <div style={{maxWidth: 500, margin: '0 auto'}}>
              <input
                type="text" placeholder="Search for products..."
                aria-label="Search products"
                value={searchQuery}
                onChange={(e) => { setSearchQuery(e.target.value); if (view !== 'products') setView('products'); }}
                autoFocus
                style={{width: '100%', padding: '12px 16px', border: '1px solid #ddd', fontSize: 14, outline: 'none'}}
              />
            </div>
          </div>
        )}
      </header>
      
      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="mobile-menu" style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: '#fff',
          zIndex: 99,
          paddingTop: 80,
          overflowY: 'auto'
        }}>
          <nav style={{padding: '20px'}}>
            <button 
              onClick={() => { setActiveCategory(null); setActiveBrand(null); setView('products'); setMobileMenuOpen(false); }} 
              style={{display: 'block', width: '100%', padding: '16px 0', border: 'none', borderBottom: '1px solid #eee', background: 'none', fontSize: 16, textAlign: 'left', cursor: 'pointer'}}
            >
              New In
            </button>
            {NAV_CATEGORIES.map(cat => (
              <button 
                key={cat.slug}
                onClick={() => { navigateTo(cat.slug); setMobileMenuOpen(false); }} 
                style={{display: 'block', width: '100%', padding: '16px 0', border: 'none', borderBottom: '1px solid #eee', background: 'none', fontSize: 16, textAlign: 'left', cursor: 'pointer'}}
              >
                {cat.name}
              </button>
            ))}
            <div style={{padding: '16px 0', borderBottom: '1px solid #eee'}}>
              <p style={{fontSize: 12, color: '#888', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '1px'}}>Brands</p>
              {BRANDS.map(brand => (
                <button 
                  key={brand}
                  onClick={() => { navigateToBrand(brand); setMobileMenuOpen(false); }} 
                  style={{display: 'block', width: '100%', padding: '12px 0', border: 'none', background: 'none', fontSize: 15, textAlign: 'left', cursor: 'pointer', color: '#444'}}
                >
                  {brand}
                </button>
              ))}
            </div>
          </nav>
        </div>
      )}

      {/* Main Content */}
      <main style={{flex: 1}}>
        {view === 'checkout' && (
          <CheckoutPage 
            cart={cart} 
            cartTotal={cartTotal} 
            onBack={() => { setView('home'); setCheckoutView(false); }}
            updateQuantity={updateQuantity}
          />
        )}
        
        {view === 'product' && selectedProduct && (
          <ProductPage product={selectedProduct} onBack={() => setView('products')} onAdd={addToCart} />
        )}
        
        {view === 'products' && (
          <ProductsPage
            products={products}
            allProducts={allProducts}
            loading={loading}
            category={activeCategory}
            brand={activeBrand}
            sortBy={sortBy}
            setSortBy={setSortBy}
            priceRange={priceRange}
            setPriceRange={setPriceRange}
            onProductClick={openProduct}
            onAdd={addToCart}
            onCategoryChange={setActiveCategory}
            onBrandChange={setActiveBrand}
            getCategoryCount={getCategoryCount}
          />
        )}
        
        {view === 'home' && (
          <HomePage
            products={allProducts}
            bestsellers={bestsellers}
            onCategoryClick={navigateTo}
            onProductClick={openProduct}
            onAdd={addToCart}
            getCategoryCount={getCategoryCount}
          />
        )}
        
        {view === 'about' && (
          <AboutPage onBack={goHome} />
        )}
        
        {view === 'delivery' && (
          <DeliveryPage onBack={goHome} />
        )}
        
        {view === 'returns' && (
          <ReturnsPage onBack={goHome} />
        )}
        
        {view === 'faqs' && (
          <FAQsPage onBack={goHome} />
        )}
        
        {view === 'contact' && (
          <ContactPage onBack={goHome} />
        )}
        
        {view === 'sustainability' && (
          <SustainabilityPage onBack={goHome} />
        )}
        
        {view === 'privacy' && (
          <PrivacyPolicyPage onBack={goHome} />
        )}
        
        {view === 'terms' && (
          <TermsPage onBack={goHome} />
        )}
        
        {view === 'cookies' && (
          <CookiePolicyPage onBack={goHome} />
        )}
      </main>

      {/* Cart Drawer */}
      <CartDrawer 
        cart={cart} 
        cartOpen={cartOpen} 
        setCartOpen={setCartOpen} 
        cartTotal={cartTotal} 
        freeShipping={freeShipping} 
        shippingCost={shippingCost}
        orderTotal={orderTotal}
        updateQuantity={updateQuantity}
        onCheckout={startCheckout}
      />

      {/* Footer */}
      <footer role="contentinfo" style={{background: '#f5ede3', borderTop: '1px solid #e5e5e5', padding: '48px 20px 32px'}}>
        <div style={{maxWidth: 1200, margin: '0 auto'}}>
          <div className="footer-grid" style={{display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 40, marginBottom: 40}}>
            <div>
              <h4 style={footerHeading}>Shop</h4>
              {NAV_CATEGORIES.map(cat => (
                <p key={cat.slug} onClick={() => navigateTo(cat.slug)} style={footerLink}>{cat.name}</p>
              ))}
            </div>
            <div>
              <h4 style={footerHeading}>Customer Service</h4>
              <p onClick={() => { setView('delivery'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>Delivery Information</p>
              <p onClick={() => { setView('returns'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>Returns & Exchanges</p>
              <p onClick={() => { setView('faqs'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>FAQs</p>
              <p onClick={() => { setView('contact'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>Contact Us</p>
            </div>
            <div>
              <h4 style={footerHeading}>About</h4>
              <p onClick={() => { setView('about'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>Our Story</p>
              <p onClick={() => { setView('sustainability'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>Sustainability</p>
            </div>
            <div>
              <h4 style={footerHeading}>Newsletter</h4>
              <p style={{fontSize: 13, color: '#666', marginBottom: 12}}>Sign up for 10% off your first order</p>
              <div style={{display: 'flex'}}>
                <input type="email" placeholder="Email" style={{flex: 1, padding: '10px 12px', border: '1px solid #ddd', borderRight: 'none', fontSize: 13, outline: 'none'}} />
                <button style={{padding: '10px 16px', background: '#222', color: '#fff', border: 'none', fontSize: 12}}>→</button>
              </div>
            </div>
          </div>
          <div className="footer-bottom" style={{borderTop: '1px solid #e5e5e5', paddingTop: 20, display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#999'}}>
            <span>© 2024 Home & Verse. DM Brands Ltd.</span>
            <div style={{display: 'flex', gap: 20}}>
              <span onClick={() => { setView('privacy'); window.scrollTo(0, 0); }} style={{cursor: 'pointer'}}>Privacy Policy</span>
              <span onClick={() => { setView('terms'); window.scrollTo(0, 0); }} style={{cursor: 'pointer'}}>Terms & Conditions</span>
              <span onClick={() => { setView('cookies'); window.scrollTo(0, 0); }} style={{cursor: 'pointer'}}>Cookie Policy</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Styles
const iconBtn = { background: 'none', border: 'none', padding: 6, color: '#222' };
const cartBadge = { position: 'absolute', top: -2, right: -2, background: '#222', color: '#fff', fontSize: 9, width: 16, height: 16, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' };
const navBtn = (active) => ({ background: 'none', border: 'none', fontSize: 13, fontWeight: active ? 500 : 400, color: '#222', padding: '4px 0', borderBottom: active ? '1px solid #222' : '1px solid transparent' });
const footerHeading = { fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 16 };
const footerLink = { fontSize: 13, color: '#666', marginBottom: 10, cursor: 'pointer' };

function HomePage({ products, bestsellers, onCategoryClick, onProductClick, onAdd, getCategoryCount }) {
  const newProducts = products.slice(0, 8);
  
  // Mood image URLs (using Unsplash for placeholders - replace with your own)
  const moodImages = {
    hero: 'https://res.cloudinary.com/dcfbgveei/image/upload/w_1600,q_85,f_auto/mood/christmas_1.jpg',
    candles: 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/products/11JGL0101002_mood1.jpg',
    lighting: 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/products/11LSB0201009_mood1.jpg',
    tableware: 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/products/11OBX0201001_mood1.jpg',
    living: 'https://res.cloudinary.com/dcfbgveei/image/upload/w_1200,q_85,f_auto/mood/homedecor_1.jpg',
    christmas: 'https://res.cloudinary.com/dcfbgveei/image/upload/w_1200,q_85,f_auto/mood/christmas_2.jpg',
  };
  
  return (
    <>
      {/* Hero - Full Width Image */}
      <section style={{
        position: 'relative',
        height: '85vh',
        minHeight: 600,
        maxHeight: 900,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden'
      }}>
        {/* Background Image */}
        <div style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `url(${moodImages.hero})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }} />
        {/* Overlay */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.4) 100%)',
        }} />
        {/* Content */}
        <div style={{
          position: 'relative',
          zIndex: 1,
          textAlign: 'center',
          padding: '0 20px',
          maxWidth: 700
        }}>
          <p style={{
            fontSize: 12,
            letterSpacing: '4px',
            color: 'rgba(255,255,255,0.9)',
            marginBottom: 24,
            textTransform: 'uppercase',
            fontWeight: 300
          }}>
            Luxury European Homeware
          </p>
          <h1 style={{
            fontFamily: "'Cormorant Garamond', Georgia, serif",
            fontSize: 'clamp(36px, 6vw, 64px)',
            fontWeight: 300,
            color: '#fff',
            lineHeight: 1.2,
            marginBottom: 24,
            letterSpacing: '-0.02em'
          }}>
            Beautiful objects for<br/>
            <em style={{fontStyle: 'italic'}}>everyday moments</em>
          </h1>
          <p style={{
            fontSize: 16,
            color: 'rgba(255,255,255,0.85)',
            marginBottom: 40,
            fontWeight: 300,
            maxWidth: 500,
            margin: '0 auto 40px'
          }}>
            Curated collections from Europe's finest design houses
          </p>
          <button 
            onClick={() => onCategoryClick(null)}
            style={{
              padding: '16px 48px',
              background: 'transparent',
              color: '#fff',
              border: '1px solid rgba(255,255,255,0.8)',
              fontSize: 12,
              letterSpacing: '2px',
              cursor: 'pointer',
              textTransform: 'uppercase',
              fontWeight: 400,
              transition: 'all 0.3s ease'
            }}
            onMouseOver={e => { 
              e.currentTarget.style.background = '#fff'; 
              e.currentTarget.style.color = '#2c2c2c'; 
            }}
            onMouseOut={e => { 
              e.currentTarget.style.background = 'transparent'; 
              e.currentTarget.style.color = '#fff'; 
            }}
          >
            Explore Collection
          </button>
        </div>
        {/* Scroll indicator */}
        <div style={{
          position: 'absolute',
          bottom: 40,
          left: '50%',
          transform: 'translateX(-50%)',
          color: '#fff',
          opacity: 0.7,
          animation: 'bounce 2s infinite'
        }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M7 10l5 5 5-5"/>
          </svg>
        </div>
      </section>

      {/* Brand Promise Bar */}
      <section className="brand-bar" style={{
        background: '#2c2c2c',
        padding: '20px',
        textAlign: 'center'
      }}>
        <p style={{
          color: '#8a7561',
          fontSize: 13,
          letterSpacing: '3px',
          textTransform: 'uppercase',
          fontWeight: 300
        }}>
          Free UK Delivery Over £30 · Same Day Dispatch Before 2pm · International Delivery Available
        </p>
      </section>

      {/* Category Grid with Images */}
      <section style={{padding: '100px 20px'}}>
        <div style={{maxWidth: 1400, margin: '0 auto'}}>
          <div style={{textAlign: 'center', marginBottom: 60}}>
            <p style={{
              fontSize: 12,
              letterSpacing: '3px',
              color: '#8a7561',
              marginBottom: 16,
              textTransform: 'uppercase'
            }}>
              Shop by Category
            </p>
            <h2 style={{
              fontFamily: "'Cormorant Garamond', Georgia, serif",
              fontSize: 40,
              fontWeight: 300,
              color: '#2c2c2c'
            }}>
              Explore Our Collections
            </h2>
          </div>
          
          <div className="category-grid" style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 24
          }}>
            {NAV_CATEGORIES.map((cat, i) => {
              const categoryImages = {
                'Christmas': 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/heroes/hero-christmas-1765906153.jpg',
                'Candles & Fragrance': 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/mood/candles_1.jpg',
                'Lighting': 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/heroes/hero-lighting.jpg?v=1765906042',
                'Tableware': 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/heroes/hero-tableware.jpg?v=1765906042',
                'Home Décor': 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/heroes/hero-homedecor.jpg?v=1765906042',
                'Gifts': 'https://res.cloudinary.com/dcfbgveei/image/upload/w_800,q_85,f_auto/heroes/hero-gift-1765906153.jpg'
              };
              return (
                <button 
                  key={cat.slug} 
                  onClick={() => onCategoryClick(cat.slug)}
                  style={{
                    position: 'relative',
                    aspectRatio: '4/3',
                    background: '#f9f3eb',
                    border: 'none',
                    cursor: 'pointer',
                    overflow: 'hidden'
                  }}
                >
                  <img 
                    src={categoryImages[cat.name]}
                    alt={cat.name}
                    style={{
                      position: 'absolute',
                      inset: 0,
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                      transition: 'transform 0.6s ease'
                    }}
                    onMouseOver={e => e.currentTarget.style.transform = 'scale(1.05)'}
                    onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
                  />
                  <div style={{
                    position: 'absolute',
                    inset: 0,
                    background: 'rgba(0,0,0,0.2)',
                    transition: 'background 0.3s ease'
                  }} />
                  <div style={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    right: 0,
                    padding: '30px',
                    background: 'linear-gradient(to top, rgba(0,0,0,0.5) 0%, transparent 100%)'
                  }}>
                    <p style={{
                      fontFamily: "'Cormorant Garamond', Georgia, serif",
                      fontSize: 26,
                      color: '#fff',
                      fontWeight: 400,
                      textShadow: '0 2px 4px rgba(0,0,0,0.3)'
                    }}>{cat.name}</p>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* Editorial Section - Brand Story */}
      <section style={{
        background: '#f9f3eb',
        padding: '120px 20px'
      }}>
        <div className="editorial-grid" style={{
          maxWidth: 1200,
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 80,
          alignItems: 'center'
        }}>
          <div className="editorial-text" style={{paddingRight: 40}}>
            <p style={{
              fontSize: 12,
              letterSpacing: '3px',
              color: '#8a7561',
              marginBottom: 24,
              textTransform: 'uppercase'
            }}>
              Our Philosophy
            </p>
            <h2 style={{
              fontFamily: "'Cormorant Garamond', Georgia, serif",
              fontSize: 42,
              fontWeight: 300,
              color: '#2c2c2c',
              lineHeight: 1.2,
              marginBottom: 24
            }}>
              Objects that tell<br/>
              <em style={{fontStyle: 'italic'}}>stories</em>
            </h2>
            <p style={{
              fontSize: 16,
              color: '#666',
              lineHeight: 1.8,
              marginBottom: 24
            }}>
              We believe in the quiet power of beautiful design. Each piece in our collection 
              is chosen not just for how it looks, but for how it makes you feel — the gentle 
              glow of candlelight, the calm of birdsong, the joy of a table set with care.
            </p>
            <p style={{
              fontSize: 16,
              color: '#666',
              lineHeight: 1.8,
              marginBottom: 32
            }}>
              From German porcelain to Dutch soy candles, every object tells a story of 
              craftsmanship, heritage, and thoughtful design.
            </p>
            <button 
              onClick={() => onCategoryClick(null)}
              style={{
                padding: '14px 36px',
                background: 'transparent',
                color: '#2c2c2c',
                border: '1px solid #2c2c2c',
                fontSize: 12,
                letterSpacing: '2px',
                cursor: 'pointer',
                textTransform: 'uppercase'
              }}
              onMouseOver={e => { 
                e.currentTarget.style.background = '#2c2c2c'; 
                e.currentTarget.style.color = '#fff'; 
              }}
              onMouseOut={e => { 
                e.currentTarget.style.background = 'transparent'; 
                e.currentTarget.style.color = '#2c2c2c'; 
              }}
            >
              Our Story
            </button>
          </div>
          <div style={{
            aspectRatio: '4/5',
            background: `url(${moodImages.living})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }} />
        </div>
      </section>

      {/* Best Sellers */}
      {bestsellers.length > 0 && (
        <section style={{padding: '100px 20px'}}>
          <div style={{maxWidth: 1400, margin: '0 auto'}}>
            <div style={{textAlign: 'center', marginBottom: 60}}>
              <p style={{
                fontSize: 12,
                letterSpacing: '3px',
                color: '#8a7561',
                marginBottom: 16,
                textTransform: 'uppercase'
              }}>
                Customer Favourites
              </p>
              <h2 style={{
                fontFamily: "'Cormorant Garamond', Georgia, serif",
                fontSize: 40,
                fontWeight: 300,
                color: '#2c2c2c'
              }}>
                Best Sellers
              </h2>
            </div>
            <div className="product-grid-4" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: 30
            }}>
              {bestsellers.slice(0, 8).map(product => (
                <ProductCard key={product.sku} product={product} onClick={() => onProductClick(product)} onAdd={onAdd} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Full Width Mood Banner */}
      <section style={{
        position: 'relative',
        height: '60vh',
        minHeight: 400,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `url(${moodImages.christmas})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundAttachment: 'fixed'
        }} />
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'rgba(0,0,0,0.35)'
        }} />
        <div style={{
          position: 'relative',
          zIndex: 1,
          textAlign: 'center',
          padding: '0 20px'
        }}>
          <p style={{
            fontSize: 12,
            letterSpacing: '4px',
            color: '#d4c5a9',
            marginBottom: 20,
            textTransform: 'uppercase'
          }}>
            The Festive Edit
          </p>
          <h2 style={{
            fontFamily: "'Cormorant Garamond', Georgia, serif",
            fontSize: 'clamp(32px, 5vw, 52px)',
            fontWeight: 300,
            color: '#fff',
            lineHeight: 1.2,
            marginBottom: 32
          }}>
            Make your home magical<br/>
            <em style={{fontStyle: 'italic'}}>this Christmas</em>
          </h2>
          <button 
            onClick={() => onCategoryClick('Christmas')}
            style={{
              padding: '16px 48px',
              background: '#d4c5a9',
              color: '#2c2c2c',
              border: 'none',
              fontSize: 12,
              letterSpacing: '2px',
              cursor: 'pointer',
              textTransform: 'uppercase'
            }}
            onMouseOver={e => { 
              e.currentTarget.style.background = '#fff'; 
            }}
            onMouseOut={e => { 
              e.currentTarget.style.background = '#d4c5a9'; 
            }}
          >
            Shop Christmas
          </button>
        </div>
      </section>

      {/* New Arrivals */}
      <section style={{padding: '100px 20px'}}>
        <div style={{maxWidth: 1400, margin: '0 auto'}}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-end',
            marginBottom: 60
          }}>
            <div>
              <p style={{
                fontSize: 12,
                letterSpacing: '3px',
                color: '#8a7561',
                marginBottom: 16,
                textTransform: 'uppercase'
              }}>
                Just Arrived
              </p>
              <h2 style={{
                fontFamily: "'Cormorant Garamond', Georgia, serif",
                fontSize: 40,
                fontWeight: 300,
                color: '#2c2c2c'
              }}>
                New Arrivals
              </h2>
            </div>
            <button 
              onClick={() => onCategoryClick(null)}
              style={{
                background: 'none',
                border: 'none',
                fontSize: 13,
                color: '#666',
                cursor: 'pointer',
                borderBottom: '1px solid #666',
                paddingBottom: 2
              }}
            >
              View all products
            </button>
          </div>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 30
          }}>
            {newProducts.map(product => (
              <ProductCard key={product.sku} product={product} onClick={() => onProductClick(product)} onAdd={onAdd} />
            ))}
          </div>
        </div>
      </section>

      {/* Brand Logos / Partners */}
      <section style={{
        background: '#f9f3eb',
        padding: '80px 20px',
        textAlign: 'center'
      }}>
        <p style={{
          fontSize: 12,
          letterSpacing: '3px',
          color: '#999',
          marginBottom: 40,
          textTransform: 'uppercase'
        }}>
          Our Brands
        </p>
        <div style={{
          maxWidth: 900,
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-around',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 40
        }}>
          {['Räder', 'Remember', 'My Flame', 'Relaxound', 'Elvang'].map(brand => (
            <span key={brand} style={{
              fontFamily: "'Cormorant Garamond', Georgia, serif",
              fontSize: 24,
              color: '#999',
              fontWeight: 400,
              letterSpacing: '2px'
            }}>
              {brand}
            </span>
          ))}
        </div>
      </section>

      {/* Trust Bar - Refined */}
      <section style={{padding: '60px 20px', background: '#fff'}}>
        <div className="product-grid-4" style={{
          maxWidth: 1000,
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 40,
          textAlign: 'center'
        }}>
          <div>
            <div style={{fontSize: 24, marginBottom: 12}}>🚚</div>
            <p style={{fontFamily: "'Cormorant Garamond', Georgia, serif", fontSize: 16, marginBottom: 4}}>Free Delivery</p>
            <p style={{fontSize: 12, color: '#888'}}>On orders over £30</p>
          </div>
          <div>
            <div style={{fontSize: 24, marginBottom: 12}}>↩️</div>
            <p style={{fontFamily: "'Cormorant Garamond', Georgia, serif", fontSize: 16, marginBottom: 4}}>Easy Returns</p>
            <p style={{fontSize: 12, color: '#888'}}>30-day hassle-free</p>
          </div>
          <div>
            <div style={{fontSize: 24, marginBottom: 12}}>🔒</div>
            <p style={{fontFamily: "'Cormorant Garamond', Georgia, serif", fontSize: 16, marginBottom: 4}}>Secure Checkout</p>
            <p style={{fontSize: 12, color: '#888'}}>SSL encrypted</p>
          </div>
          <div>
            <div style={{fontSize: 24, marginBottom: 12}}>🎁</div>
            <p style={{fontFamily: "'Cormorant Garamond', Georgia, serif", fontSize: 16, marginBottom: 4}}>Gift Ready</p>
            <p style={{fontSize: 12, color: '#888'}}>Beautifully packaged</p>
          </div>
        </div>
      </section>
    </>
  );
}

function AboutPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      {/* Back link */}
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Our Story</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <p style={{marginBottom: 24}}>
          Home & Verse brings together a carefully curated collection of European homeware from some of the continent's most distinguished design houses. Based in the UK, we are the exclusive distributors for a family of brands that share our passion for thoughtful design, quality craftsmanship, and the belief that beautiful objects can transform everyday moments into something special.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Our Brands</h2>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Räder</strong> — From their studio in Germany, Räder creates poetic porcelain pieces and atmospheric lighting that capture the magic of the seasons. Their iconic light houses and delicate ceramics have become beloved classics, bringing warmth and wonder to homes across Europe for over three decades.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Remember</strong> — Bold, colourful, and unapologetically joyful. This German design house believes life is too short for beige, crafting vibrant homeware and gifts that celebrate colour, pattern, and playful sophistication. Each piece is designed to spark conversation and bring a smile.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>My Flame</strong> — Born in the Netherlands, My Flame creates hand-poured soy candles with a twist — each one carries a hidden message revealed as the candle burns. Their thoughtful approach to gifting combines beautiful fragrance with meaningful moments of connection.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Relaxound</strong> — The inventors of the original Zwitscherbox, Relaxound brings the calming sounds of nature indoors. These clever German-designed soundboxes deliver moments of birdsong, ocean waves, or forest ambience at the touch of a hand — a simple antidote to the noise of modern life.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Elvang Denmark</strong> — Masters of Scandinavian textile design, Elvang creates luxurious throws, cushions and scarves from the finest alpaca wool and baby llama. Each piece combines timeless Danish aesthetics with exceptional warmth and softness, bringing a touch of Nordic elegance to your home.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Our Philosophy</h2>
        
        <p style={{marginBottom: 24}}>
          We believe in the power of considered design to elevate the everyday. Every product in our collection has been chosen not just for how it looks, but for how it makes you feel — whether that's the gentle glow of a Räder light house on a winter evening, the joy of unwrapping a Remember gift, or the calm that comes from a moment of birdsong.
        </p>
        
        <p style={{marginBottom: 24}}>
          From our base in the UK, we work directly with each of our partner brands, ensuring that every piece that reaches your home meets the standards of quality and craftsmanship that first drew us to these exceptional makers.
        </p>
        
        <p style={{marginBottom: 24, fontStyle: 'italic', color: '#666'}}>
          Thank you for choosing Home & Verse. We hope our collection brings beauty, warmth, and a little magic to your home.
        </p>
      </div>
    </div>
  );
}


function DeliveryPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Delivery Information</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <h2 style={{fontSize: 20, fontWeight: 500, marginBottom: 20, color: '#222'}}>UK Delivery</h2>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Free Standard Delivery</strong> on all orders over £30. Orders under £30 incur a £3.95 delivery charge.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Standard Delivery (2-4 working days)</strong><br/>
          Orders placed before 2pm Monday-Friday are dispatched the same day. Delivery is via Royal Mail or DPD depending on the size of your order.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Express Delivery (Next working day) — £6.95</strong><br/>
          Order before 2pm Monday-Thursday for next working day delivery. Orders placed on Friday before 2pm will arrive Monday.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>International Delivery</h2>
        
        <p style={{marginBottom: 24}}>
          We currently ship to most European countries. International delivery rates are calculated at checkout based on weight and destination.
        </p>
        
        <table style={{width: '100%', borderCollapse: 'collapse', marginBottom: 24}}>
          <thead>
            <tr style={{borderBottom: '1px solid #ddd'}}>
              <th style={{textAlign: 'left', padding: '12px 0', fontWeight: 500}}>Destination</th>
              <th style={{textAlign: 'left', padding: '12px 0', fontWeight: 500}}>Delivery Time</th>
              <th style={{textAlign: 'right', padding: '12px 0', fontWeight: 500}}>From</th>
            </tr>
          </thead>
          <tbody style={{color: '#666'}}>
            <tr style={{borderBottom: '1px solid #eee'}}>
              <td style={{padding: '12px 0'}}>Republic of Ireland</td>
              <td style={{padding: '12px 0'}}>3-5 working days</td>
              <td style={{padding: '12px 0', textAlign: 'right'}}>£7.95</td>
            </tr>
            <tr style={{borderBottom: '1px solid #eee'}}>
              <td style={{padding: '12px 0'}}>EU Countries</td>
              <td style={{padding: '12px 0'}}>5-7 working days</td>
              <td style={{padding: '12px 0', textAlign: 'right'}}>£9.95</td>
            </tr>
            <tr style={{borderBottom: '1px solid #eee'}}>
              <td style={{padding: '12px 0'}}>Rest of World</td>
              <td style={{padding: '12px 0'}}>7-14 working days</td>
              <td style={{padding: '12px 0', textAlign: 'right'}}>£14.95</td>
            </tr>
          </tbody>
        </table>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Order Tracking</h2>
        
        <p style={{marginBottom: 24}}>
          Once your order has been dispatched, you'll receive an email with tracking information. You can track your delivery directly through Royal Mail or DPD's website.
        </p>
        
        <p style={{marginBottom: 24, fontStyle: 'italic', color: '#666'}}>
          Please note: During busy periods (Christmas, sales) delivery times may be slightly longer. We'll always keep you updated.
        </p>
      </div>
    </div>
  );
}

function ReturnsPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Returns & Exchanges</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <h2 style={{fontSize: 20, fontWeight: 500, marginBottom: 20, color: '#222'}}>Our Promise</h2>
        
        <p style={{marginBottom: 24}}>
          We want you to be completely happy with your purchase. If for any reason you're not, we offer a simple 30-day returns policy.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>How to Return</h2>
        
        <ol style={{marginBottom: 24, paddingLeft: 20}}>
          <li style={{marginBottom: 12}}>Email us at <a href="mailto:hello@homeandverse.co.uk" style={{color: '#222'}}>hello@homeandverse.co.uk</a> with your order number</li>
          <li style={{marginBottom: 12}}>We'll send you a returns label and instructions</li>
          <li style={{marginBottom: 12}}>Pack items securely in their original packaging if possible</li>
          <li style={{marginBottom: 12}}>Drop off at your nearest Post Office or arrange collection</li>
        </ol>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Returns Policy</h2>
        
        <p style={{marginBottom: 16}}>
          <strong style={{color: '#222'}}>Timeframe:</strong> Items can be returned within 30 days of delivery
        </p>
        
        <p style={{marginBottom: 16}}>
          <strong style={{color: '#222'}}>Condition:</strong> Items must be unused, in original packaging, with all tags attached
        </p>
        
        <p style={{marginBottom: 16}}>
          <strong style={{color: '#222'}}>Refunds:</strong> Processed within 5-7 working days of receiving your return
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Return Shipping:</strong> Free for UK customers. International customers are responsible for return shipping costs.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Exceptions</h2>
        
        <p style={{marginBottom: 24}}>
          For hygiene reasons, we cannot accept returns on candles that have been lit, diffusers that have been opened, or any personalised items. Sale items are final sale unless faulty.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Damaged or Faulty Items</h2>
        
        <p style={{marginBottom: 24}}>
          If your item arrives damaged or faulty, please contact us within 48 hours with photos and we'll arrange a replacement or full refund including return shipping costs.
        </p>
      </div>
    </div>
  );
}

function FAQsPage({ onBack }) {
  const [openFaq, setOpenFaq] = useState(null);
  
  const faqs = [
    {
      q: "How long will my delivery take?",
      a: "UK standard delivery takes 2-4 working days. Orders placed before 2pm are dispatched same day. Express next-day delivery is available for £6.95."
    },
    {
      q: "Do you offer free delivery?",
      a: "Yes! We offer free standard UK delivery on all orders over £30. Orders under £30 have a £3.95 delivery charge."
    },
    {
      q: "Can I track my order?",
      a: "Absolutely. Once your order is dispatched, you'll receive an email with tracking information so you can follow your delivery every step of the way."
    },
    {
      q: "What is your returns policy?",
      a: "We offer a 30-day returns policy on unused items in original packaging. Simply email us at hello@homeandverse.co.uk and we'll send you a free returns label."
    },
    {
      q: "Do you ship internationally?",
      a: "Yes, we ship to most European countries and beyond. International delivery rates are calculated at checkout based on your location and order weight."
    },
    {
      q: "Are your candles made from natural wax?",
      a: "Our My Flame candles are hand-poured using natural soy wax with cotton wicks, making them cleaner burning and longer lasting than paraffin alternatives."
    },
    {
      q: "What is a Zwitscherbox?",
      a: "The Zwitscherbox is the original birdsong box by Relaxound. It plays 2 minutes of authentic forest birdsong, activated by motion sensor. Simply wave your hand past it to bring the sounds of nature indoors."
    },
    {
      q: "Do you offer gift wrapping?",
      a: "All our products are beautifully packaged and gift-ready. We don't currently offer additional gift wrapping, but we're working on it!"
    },
    {
      q: "How do I care for porcelain items?",
      a: "Our Räder porcelain pieces are best cleaned with a soft, damp cloth. While some items are dishwasher safe, we recommend hand washing to preserve the delicate finishes and extend their life."
    },
    {
      q: "Can I visit your showroom?",
      a: "We're primarily an online retailer, but trade customers are welcome to arrange showroom visits by appointment. Please contact us to arrange."
    }
  ];
  
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Frequently Asked Questions</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        {faqs.map((faq, i) => (
          <div key={i} style={{borderBottom: '1px solid #eee', paddingBottom: 16, marginBottom: 16}}>
            <button 
              onClick={() => setOpenFaq(openFaq === i ? null : i)}
              style={{
                width: '100%', background: 'none', border: 'none', 
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                fontSize: 16, fontWeight: 500, color: '#222', cursor: 'pointer',
                padding: '8px 0', textAlign: 'left'
              }}
            >
              {faq.q}
              <span style={{fontSize: 20, transform: openFaq === i ? 'rotate(45deg)' : 'none', transition: 'transform 0.2s'}}>+</span>
            </button>
            {openFaq === i && (
              <p style={{marginTop: 12, color: '#666', paddingRight: 40}}>{faq.a}</p>
            )}
          </div>
        ))}
      </div>
      
      <div style={{marginTop: 48, padding: 24, background: '#f8f8f8', textAlign: 'center'}}>
        <p style={{marginBottom: 12, color: '#666'}}>Can't find what you're looking for?</p>
        <a href="mailto:hello@homeandverse.co.uk" style={{color: '#222', fontWeight: 500}}>Contact us at hello@homeandverse.co.uk</a>
      </div>
    </div>
  );
}

function ContactPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Contact Us</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <p style={{marginBottom: 32, textAlign: 'center', fontSize: 16}}>
          We'd love to hear from you. Whether you have a question about an order, need help choosing the perfect gift, or just want to say hello.
        </p>
        
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 32, marginBottom: 48}}>
          <div style={{padding: 32, background: '#f8f8f8', textAlign: 'center'}}>
            <div style={{fontSize: 24, marginBottom: 16}}>✉️</div>
            <h3 style={{fontSize: 16, fontWeight: 500, marginBottom: 8}}>Email</h3>
            <a href="mailto:hello@homeandverse.co.uk" style={{color: '#222'}}>hello@homeandverse.co.uk</a>
            <p style={{fontSize: 13, color: '#888', marginTop: 8}}>We aim to reply within 24 hours</p>
          </div>
          
          <div style={{padding: 32, background: '#f8f8f8', textAlign: 'center'}}>
            <div style={{fontSize: 24, marginBottom: 16}}>📞</div>
            <h3 style={{fontSize: 16, fontWeight: 500, marginBottom: 8}}>Phone</h3>
            <a href="tel:+441905616006" style={{color: '#222'}}>+44 1905 616006</a>
            <p style={{fontSize: 13, color: '#888', marginTop: 8}}>Mon-Fri, 9am-5pm</p>
          </div>
        </div>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Trade Enquiries</h2>
        
        <p style={{marginBottom: 24}}>
          Are you a retailer interested in stocking our brands? Home & Verse is the consumer brand of DM Brands Ltd, exclusive UK distributor for Räder, Remember, My Flame, Relaxound, and Ideas4Seasons. We offer competitive trade terms and dedicated account support.
        </p>
        
        <p style={{marginBottom: 24}}>
          Please email <a href="mailto:sales@dmbrands.co.uk" style={{color: '#222'}}>sales@dmbrands.co.uk</a> with details about your business and we'll be in touch.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Press & Media</h2>
        
        <p style={{marginBottom: 24}}>
          For press enquiries, product samples, or high-resolution images, please contact <a href="mailto:hello@homeandverse.co.uk" style={{color: '#222'}}>hello@homeandverse.co.uk</a>
        </p>
      </div>
    </div>
  );
}

function SustainabilityPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Sustainability</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <p style={{marginBottom: 24, fontSize: 16}}>
          We believe beautiful design and environmental responsibility go hand in hand. Here's how we're working to reduce our impact.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Our Brands</h2>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Räder</strong> creates timeless pieces designed to last, not follow fleeting trends. Their porcelain is made in Germany using traditional techniques, and they're committed to reducing packaging waste across their range.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>My Flame</strong> candles are hand-poured using natural soy wax, which burns cleaner and longer than paraffin. The glass containers are designed to be reused or recycled.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Relaxound</strong> uses sustainably sourced wood and bamboo in their soundboxes, and has committed to carbon-neutral shipping for all their products.
        </p>
        
        <p style={{marginBottom: 24}}>
          <strong style={{color: '#222'}}>Elvang Denmark</strong> creates luxurious throws and cushions from alpaca wool - a natural, renewable fibre that requires no chemical processing.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Our Packaging</h2>
        
        <p style={{marginBottom: 24}}>
          We're working to eliminate single-use plastic from our operations. Our shipping boxes are made from recycled cardboard, and we use paper tape and tissue paper rather than plastic alternatives.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Shipping</h2>
        
        <p style={{marginBottom: 24}}>
          We consolidate orders where possible to reduce the number of deliveries, and partner with delivery services that are investing in electric vehicle fleets and carbon offset programmes.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Buy Less, Buy Better</h2>
        
        <p style={{marginBottom: 24}}>
          Perhaps the most sustainable choice is to buy fewer, better things. Every product we stock is chosen for its quality and longevity - pieces designed to be treasured for years, not discarded after seasons.
        </p>
        
        <p style={{marginBottom: 24, fontStyle: 'italic', color: '#666'}}>
          We're always looking for ways to improve. If you have suggestions, we'd love to hear them at hello@homeandverse.co.uk
        </p>
      </div>
    </div>
  );
}

function PrivacyPolicyPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Privacy Policy</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <p style={{marginBottom: 24, fontStyle: 'italic', color: '#666'}}>Last updated: December 2024</p>
        
        <p style={{marginBottom: 24}}>
          Home & Verse ("we", "our", or "us") is committed to protecting your privacy. This policy explains how we collect, use, and safeguard your personal information when you use our website homeandverse.co.uk.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Who We Are</h2>
        <p style={{marginBottom: 24}}>
          Home & Verse is a trading name of DM Brands Ltd, a company registered in England and Wales. We are the data controller responsible for your personal data.
        </p>
        <p style={{marginBottom: 24}}>
          <strong>Contact:</strong> hello@homeandverse.co.uk
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Information We Collect</h2>
        <p style={{marginBottom: 16}}>We collect information that you provide directly to us:</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Order information:</strong> Name, email, delivery address, phone number</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Payment information:</strong> Processed securely by our payment provider (we do not store card details)</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Communications:</strong> Emails and messages you send us</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• <strong>Newsletter:</strong> Email address if you subscribe</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>How We Use Your Information</h2>
        <p style={{marginBottom: 16}}>We use your personal information to:</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Process and fulfil your orders</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Send order confirmations and delivery updates</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Respond to your enquiries and provide customer support</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Send marketing emails (only with your consent)</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• Comply with legal obligations</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Legal Basis for Processing</h2>
        <p style={{marginBottom: 16}}>We process your data based on:</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Contract:</strong> To fulfil orders you place with us</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Legitimate interests:</strong> To improve our services and prevent fraud</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• <strong>Consent:</strong> For marketing communications (you can withdraw anytime)</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Third Parties</h2>
        <p style={{marginBottom: 16}}>We share your information with:</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Delivery partners:</strong> Royal Mail, DPD to fulfil your orders</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Payment processors:</strong> To securely process payments</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Order management:</strong> Zoho (our inventory system)</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• <strong>Email services:</strong> To send transactional and marketing emails</p>
        <p style={{marginBottom: 24}}>We do not sell your personal information to third parties.</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Data Retention</h2>
        <p style={{marginBottom: 24}}>
          We retain order information for 7 years for tax and legal purposes. Marketing preferences are kept until you unsubscribe. You can request deletion of your data at any time.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Your Rights</h2>
        <p style={{marginBottom: 16}}>Under UK GDPR, you have the right to:</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Access your personal data</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Correct inaccurate data</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Request deletion of your data</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Object to processing</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Data portability</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• Withdraw consent at any time</p>
        <p style={{marginBottom: 24}}>To exercise these rights, email us at hello@homeandverse.co.uk</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Cookies</h2>
        <p style={{marginBottom: 24}}>
          We use essential cookies to make our website work. See our Cookie Policy for more details.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Changes to This Policy</h2>
        <p style={{marginBottom: 24}}>
          We may update this policy from time to time. We will notify you of significant changes by email or website notice.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Complaints</h2>
        <p style={{marginBottom: 24}}>
          If you're unhappy with how we handle your data, you can complain to the Information Commissioner's Office (ICO) at ico.org.uk
        </p>
      </div>
    </div>
  );
}

function TermsPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Terms & Conditions</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <p style={{marginBottom: 24, fontStyle: 'italic', color: '#666'}}>Last updated: December 2024</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>1. About Us</h2>
        <p style={{marginBottom: 24}}>
          Home & Verse is a trading name of DM Brands Ltd, a company registered in England and Wales. These terms govern your use of homeandverse.co.uk and any purchases you make.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>2. Ordering</h2>
        <p style={{marginBottom: 24}}>
          When you place an order, you are making an offer to buy. We will confirm acceptance by sending an order confirmation email. A contract is formed when we dispatch your order.
        </p>
        <p style={{marginBottom: 24}}>
          All orders are subject to availability. We reserve the right to refuse any order.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>3. Prices</h2>
        <p style={{marginBottom: 24}}>
          All prices are in pounds sterling (£) and include VAT where applicable. Prices may change without notice, but this won't affect orders already confirmed.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>4. Payment</h2>
        <p style={{marginBottom: 24}}>
          We accept major credit and debit cards. Payment is taken at the time of ordering. All payments are processed securely.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>5. Delivery</h2>
        <p style={{marginBottom: 24}}>
          We aim to dispatch orders placed before 2pm on the same working day. UK standard delivery takes 2-4 working days. International delivery takes 5-10 working days.
        </p>
        <p style={{marginBottom: 24}}>
          Risk of loss passes to you upon delivery. We are not responsible for delays outside our control.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>6. Your Right to Cancel</h2>
        <p style={{marginBottom: 24}}>
          Under the Consumer Contracts Regulations 2013, you have 14 days from delivery to cancel your order for any reason. To cancel, contact us at hello@homeandverse.co.uk
        </p>
        <p style={{marginBottom: 24}}>
          You must return items unused, in original packaging, within 14 days of cancellation. We will refund the full price including standard delivery costs within 14 days of receiving the returned goods.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>7. Our Returns Policy</h2>
        <p style={{marginBottom: 24}}>
          In addition to your statutory rights, we offer a 30-day returns policy. Items must be unused and in original packaging. See our Returns page for full details.
        </p>
        <p style={{marginBottom: 24}}>
          <strong>Exceptions:</strong> For hygiene reasons, we cannot accept returns on candles that have been lit, diffusers that have been opened, or personalised items.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>8. Faulty or Damaged Goods</h2>
        <p style={{marginBottom: 24}}>
          If items arrive damaged or faulty, contact us within 48 hours with photos. We will arrange a replacement or full refund including return postage. Your statutory rights under the Consumer Rights Act 2015 are not affected.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>9. Product Descriptions</h2>
        <p style={{marginBottom: 24}}>
          We try to display products as accurately as possible. Colours may vary slightly due to screen settings. Minor variations in handmade items are normal and not considered defects.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>10. Limitation of Liability</h2>
        <p style={{marginBottom: 24}}>
          We are not liable for any indirect or consequential losses. Our total liability shall not exceed the value of your order. Nothing in these terms excludes liability for death, personal injury, or fraud.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>11. Intellectual Property</h2>
        <p style={{marginBottom: 24}}>
          All content on this website (images, text, logos) is owned by Home & Verse or our licensors. You may not reproduce, distribute, or use any content without permission.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>12. Governing Law</h2>
        <p style={{marginBottom: 24}}>
          These terms are governed by English law. Any disputes will be subject to the exclusive jurisdiction of the English courts.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>13. Contact</h2>
        <p style={{marginBottom: 24}}>
          Questions about these terms? Email us at hello@homeandverse.co.uk
        </p>
      </div>
    </div>
  );
}

function CookiePolicyPage({ onBack }) {
  return (
    <div style={{maxWidth: 800, margin: '0 auto', padding: '60px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 40, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <h1 style={{fontSize: 32, fontWeight: 400, marginBottom: 40, textAlign: 'center'}}>Cookie Policy</h1>
      
      <div style={{fontSize: 15, lineHeight: 1.8, color: '#444'}}>
        <p style={{marginBottom: 24, fontStyle: 'italic', color: '#666'}}>Last updated: December 2024</p>
        
        <p style={{marginBottom: 24}}>
          This policy explains how Home & Verse uses cookies and similar technologies on our website.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>What Are Cookies?</h2>
        <p style={{marginBottom: 24}}>
          Cookies are small text files stored on your device when you visit a website. They help websites function properly and provide information to site owners.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Essential Cookies</h2>
        <p style={{marginBottom: 24}}>
          These cookies are necessary for the website to function. They enable core features like shopping cart, checkout, and security. You cannot opt out of these cookies.
        </p>
        <table style={{width: '100%', borderCollapse: 'collapse', marginBottom: 24}}>
          <thead>
            <tr style={{borderBottom: '1px solid #ddd'}}>
              <th style={{textAlign: 'left', padding: '12px 0', fontWeight: 500}}>Cookie</th>
              <th style={{textAlign: 'left', padding: '12px 0', fontWeight: 500}}>Purpose</th>
              <th style={{textAlign: 'left', padding: '12px 0', fontWeight: 500}}>Duration</th>
            </tr>
          </thead>
          <tbody style={{color: '#666'}}>
            <tr style={{borderBottom: '1px solid #eee'}}>
              <td style={{padding: '12px 0'}}>cart</td>
              <td style={{padding: '12px 0'}}>Stores your shopping cart contents</td>
              <td style={{padding: '12px 0'}}>Session</td>
            </tr>
            <tr style={{borderBottom: '1px solid #eee'}}>
              <td style={{padding: '12px 0'}}>session</td>
              <td style={{padding: '12px 0'}}>Maintains your session while browsing</td>
              <td style={{padding: '12px 0'}}>Session</td>
            </tr>
          </tbody>
        </table>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Analytics Cookies</h2>
        <p style={{marginBottom: 24}}>
          We may use analytics cookies to understand how visitors use our website. This helps us improve the user experience. These cookies collect anonymous information.
        </p>
        <p style={{marginBottom: 24}}>
          If we implement Google Analytics, we will update this policy and provide an option to opt out.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Managing Cookies</h2>
        <p style={{marginBottom: 24}}>
          Most browsers allow you to control cookies through settings. You can:
        </p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• View what cookies are stored</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Delete some or all cookies</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• Block cookies from certain or all sites</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• Set preferences for specific websites</p>
        <p style={{marginBottom: 24}}>
          Note: Blocking essential cookies may prevent you from using our checkout.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Browser Settings</h2>
        <p style={{marginBottom: 16}}>To manage cookies in your browser:</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Chrome:</strong> Settings → Privacy and Security → Cookies</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Firefox:</strong> Settings → Privacy & Security → Cookies</p>
        <p style={{marginBottom: 8, paddingLeft: 20}}>• <strong>Safari:</strong> Preferences → Privacy → Manage Website Data</p>
        <p style={{marginBottom: 24, paddingLeft: 20}}>• <strong>Edge:</strong> Settings → Cookies and Site Permissions</p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Changes to This Policy</h2>
        <p style={{marginBottom: 24}}>
          We may update this policy if we add new cookies or tracking technologies. Check back periodically for updates.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Contact</h2>
        <p style={{marginBottom: 24}}>
          Questions about cookies? Email us at hello@homeandverse.co.uk
        </p>
      </div>
    </div>
  );
}

function ProductsPage({ products, allProducts, loading, category, brand, sortBy, setSortBy, priceRange, setPriceRange, onProductClick, onAdd, onCategoryChange, onBrandChange, getCategoryCount }) {
  const categoryObj = NAV_CATEGORIES.find(c => c.slug === category);
  const categoryName = brand ? brand : (categoryObj?.name || 'All Products');
  const totalProducts = allProducts.length;
  
  // Brand descriptions
  const brandDescriptions = {
    'Räder': 'Poetic German porcelain and atmospheric lighting since 1990. Known for their iconic light houses and delicate ceramics.',
    'Remember': 'Bold, colourful German homeware and gifts that celebrate pattern, colour and playful sophistication.',
    'My Flame': 'Dutch hand-poured soy candles with hidden messages. Beautiful fragrance meets meaningful moments.',
    'Relaxound': 'The inventors of the original Zwitscherbox. German-designed nature soundboxes bringing calm to your home.',
    'Ideas4Seasons': 'Seasonal decorations and festive homeware to celebrate every occasion throughout the year.',
    'Elvang': 'Luxurious Danish throws, cushions and scarves in premium alpaca wool and baby llama. Timeless Scandinavian design.',
  };

  return (
    <div style={{maxWidth: 1400, margin: '0 auto', padding: '20px'}}>
      {/* Breadcrumb */}
      <div style={{fontSize: 12, color: '#888', marginBottom: 20}}>
        <span style={{cursor: 'pointer'}} onClick={() => { onCategoryChange(null); onBrandChange(null); }}>Shop</span>
        {category && <> / <span>{categoryName}</span></>}
        {brand && <> / <span>{brand}</span></>}
      </div>
      
      {/* Page Header */}
      <div style={{marginBottom: 24}}>
        <h1 style={{fontSize: 24, fontWeight: 500, marginBottom: 8}}>{categoryName}</h1>
        {category && !brand && (
          <p style={{fontSize: 13, color: '#666', maxWidth: 600}}>
            {category === 'Christmas' && 'Make your home magical with our festive Christmas collection.'}
            {category === 'Candles & Fragrance' && 'Create the perfect atmosphere with our collection of candles and home fragrance.'}
            {category === 'Lighting' && 'Discover beautiful lighting to illuminate your space.'}
            {category === 'Tableware' && 'Elevate your dining with our curated tableware collection.'}
            {category === 'Home Décor' && 'Put a personal touch on your home with decorations for every room.'}
            {category === 'Gifts' && 'Find the perfect gift for someone special.'}
          </p>
        )}
        {brand && (
          <p style={{fontSize: 13, color: '#666', maxWidth: 600}}>
            {brandDescriptions[brand] || `Explore our collection from ${brand}.`}
          </p>
        )}
      </div>

      {/* Toolbar */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid #eee'}}>
        <span style={{fontSize: 13, color: '#666'}}>{products.length} products</span>
        <div style={{display: 'flex', alignItems: 'center', gap: 8}}>
          <span style={{fontSize: 12, color: '#666'}}>Sort by</span>
          <select value={sortBy} onChange={e => setSortBy(e.target.value)} style={selectStyle}>
            <option value="popularity">Popularity</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="name">Name A-Z</option>
          </select>
        </div>
      </div>
      
      {/* Grid */}
      {loading ? (
        <div style={{textAlign: 'center', padding: 60, color: '#888'}}>Loading...</div>
      ) : products.length === 0 ? (
        <div style={{textAlign: 'center', padding: 60, color: '#888'}}>No products found</div>
      ) : (
        <div className="product-grid-4" style={{display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20}}>
          {products.map(product => (
            <ProductCard key={product.sku} product={product} onClick={() => onProductClick(product)} onAdd={onAdd} />
          ))}
        </div>
      )}
    </div>
  );
}

const filterLabel = { display: 'flex', alignItems: 'center', fontSize: 13, marginBottom: 8, cursor: 'pointer' };
const priceInput = { width: 70, padding: '8px 10px', border: '1px solid #ddd', fontSize: 13, outline: 'none' };
const selectStyle = { padding: '8px 28px 8px 12px', border: '1px solid #ddd', background: '#fff', fontSize: 13, outline: 'none', appearance: 'none', backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E")`, backgroundRepeat: 'no-repeat', backgroundPosition: 'right 10px center' };

function ProductCard({ product, onClick, onAdd }) {
  const [hovered, setHovered] = useState(false);
  
  return (
    <div style={{cursor: 'pointer'}} onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)} onClick={onClick}>
      <div style={{background: '#f8f8f8', aspectRatio: '1', marginBottom: 12, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden'}}>
        {product.has_image ? (
          <img src={getImageUrl(product.image_url, 'medium')} alt={`${product.name} by ${product.brand} - Luxury European homeware from Home & Verse`} loading="lazy" style={{maxWidth: '85%', maxHeight: '85%', objectFit: 'contain', transition: 'transform 0.3s', transform: hovered ? 'scale(1.03)' : 'scale(1)'}} />
        ) : (
          <div style={{color: '#ddd', fontSize: 48}}>✦</div>
        )}
        
        {/* Quick Add */}
        <button onClick={(e) => { e.stopPropagation(); onAdd(product); }} style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          padding: '10px', background: '#222', color: '#fff', border: 'none',
          fontSize: 11, letterSpacing: '0.5px', textTransform: 'uppercase',
          opacity: hovered ? 1 : 0, transition: 'opacity 0.2s', transform: hovered ? 'translateY(0)' : 'translateY(100%)'
        }}>
          Add to bag
        </button>
        
        {/* Stock badge */}
        {product.stock > 0 && (
          <span style={{position: 'absolute', top: 8, left: 8, background: '#fff', padding: '4px 8px', fontSize: 10, color: '#22c55e'}}>
            In stock
          </span>
        )}
      </div>
      <h3 style={{fontSize: 13, fontWeight: 400, marginBottom: 6, lineHeight: 1.4, minHeight: 36}}>{product.name}</h3>
      <p style={{fontSize: 14, fontWeight: 500}}>£{product.price.toFixed(2)}</p>
    </div>
  );
}

function ImageLightbox({ src, alt, onClose }) {
  useEffect(() => {
    const handleEscape = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  return (
    <div onClick={onClose} style={{
      position: 'fixed', inset: 0, zIndex: 300, background: 'rgba(0,0,0,0.9)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'zoom-out'
    }}>
      <button onClick={onClose} style={{
        position: 'absolute', top: 20, right: 20, background: 'none', border: 'none',
        color: '#fff', fontSize: 32, cursor: 'pointer', zIndex: 301
      }}>×</button>
      <img 
        src={src} 
        alt={alt} 
        onClick={(e) => e.stopPropagation()}
        style={{maxWidth: '90vw', maxHeight: '90vh', objectFit: 'contain', cursor: 'default'}} 
      />
    </div>
  );
}

function ProductPage({ product, onBack, onAdd }) {
  const [selectedImage, setSelectedImage] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);
  
  // Get sound URL for Relaxound products
  const soundUrl = product.brand === 'Relaxound' ? getRelaxoundSound(product.name) : null;
  
  const toggleSound = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };
  
  // Reset audio when product changes
  useEffect(() => {
    setIsPlaying(false);
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  }, [product.sku]);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [extraImages, setExtraImages] = useState([]);
  
  // Get SKU from product for Cloudinary lookups
  const sku = product.sku;
  
  // Main image URL
  const mainImage = product.image_url;
  
  // Load extra images - try common patterns and show what works
  useEffect(() => {
    if (!sku) return;
    
    // Try loading variants _2 through _6 AND mood images
    const possibleExtras = [];
    for (let i = 2; i <= 6; i++) {
      possibleExtras.push(`/images/${sku}_${i}.jpg`);
    }
    // Also check for mood images
    for (let i = 1; i <= 4; i++) {
      possibleExtras.push(`/images/${sku}_mood${i}.jpg`);
    }
    
    // Test each one with an Image object (faster than fetch)
    const validExtras = [];
    let completed = 0;
    
    possibleExtras.forEach((path, idx) => {
      const img = new Image();
      img.onload = () => {
        validExtras[idx] = path;
        completed++;
        if (completed === possibleExtras.length) {
          setExtraImages(validExtras.filter(Boolean));
        }
      };
      img.onerror = () => {
        completed++;
        if (completed === possibleExtras.length) {
          setExtraImages(validExtras.filter(Boolean));
        }
      };
      img.src = getImageUrl(path, 'thumb');
    });
  }, [sku]);
  
  // Reset when product changes
  useEffect(() => {
    setSelectedImage(0);
    setExtraImages([]);
  }, [product.sku]);
  
  // Combine main image + extras
  const images = mainImage 
    ? [mainImage, ...extraImages] 
    : extraImages;
  
  return (
    <div style={{maxWidth: 1100, margin: '0 auto', padding: '30px 20px'}}>
      {/* Lightbox */}
      {lightboxOpen && images.length > 0 && (
        <ImageLightbox 
          src={getImageUrl(images[selectedImage], 'large')} 
          alt={`${product.name} by ${product.brand} - Shop at Home & Verse`} 
          onClose={() => setLightboxOpen(false)} 
        />
      )}
      
      {/* Back link */}
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 30, display: 'flex', alignItems: 'center', gap: 6}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back
      </button>
      
      <div className="product-detail-grid" style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 60}}>
        {/* Image Gallery */}
        <div>
          {/* Main Image */}
          <div 
            onClick={() => images.length > 0 && setLightboxOpen(true)}
            style={{background: '#f8f8f8', aspectRatio: '1', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: images.length > 1 ? 12 : 0, position: 'relative', cursor: images.length > 0 ? 'zoom-in' : 'default'}}
          >
            {images.length > 0 ? (
              <img src={getImageUrl(images[selectedImage], 'large')} alt={`${product.name} by ${product.brand} - £${product.price?.toFixed(2)} at Home & Verse`} style={{maxWidth: '80%', maxHeight: '80%', objectFit: 'contain'}} />
            ) : (
              <div style={{color: '#ddd', fontSize: 80}}>✦</div>
            )}
            {/* Magnifying Glass Icon */}
            {images.length > 0 && (
              <button 
                onClick={(e) => { e.stopPropagation(); setLightboxOpen(true); }}
                style={{
                  position: 'absolute', bottom: 12, right: 12,
                  width: 40, height: 40, borderRadius: '50%',
                  background: 'rgba(255,255,255,0.9)', border: '1px solid #ddd',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#333" strokeWidth="2">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="m21 21-4.35-4.35"/>
                  <path d="M11 8v6M8 11h6"/>
                </svg>
              </button>
            )}
          </div>
          
          {/* Thumbnail Strip */}
          {images.length > 1 && (
            <div className="product-thumbs" style={{display: 'flex', gap: 8}}>
              {images.map((img, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedImage(idx)}
                  style={{
                    width: 72, height: 72, padding: 0,
                    background: '#f8f8f8', border: selectedImage === idx ? '2px solid #222' : '1px solid #eee',
                    cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center'
                  }}
                >
                  <img src={getImageUrl(img, 'thumb')} alt={`${product.name} ${idx + 1}`} loading="lazy" style={{maxWidth: '90%', maxHeight: '90%', objectFit: 'contain'}} />
                </button>
              ))}
            </div>
          )}
        </div>
        
        {/* Info */}
        <div>
          <p style={{fontSize: 11, color: '#888', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.5px'}}>
            {(product.categories || [product.category]).join(' · ')}
          </p>
          <h1 style={{fontSize: 24, fontWeight: 500, marginBottom: 12}}>{product.name}</h1>
          <p style={{fontSize: 22, marginBottom: 20}}>£{product.price.toFixed(2)}</p>
          
          {product.description && (
            <p style={{fontSize: 14, color: '#666', lineHeight: 1.7, marginBottom: 24}}>{product.description}</p>
          )}
          
          <div style={{display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24}}>
            <span style={{width: 8, height: 8, borderRadius: '50%', background: '#22c55e'}} />
            <span style={{fontSize: 13, color: '#666'}}>In stock ({product.stock} available)</span>
          </div>
          
          {/* Sound player for Relaxound products */}
          {soundUrl && (
            <div style={{marginBottom: 24, padding: 16, background: '#f8f8f8', borderRadius: 8}}>
              <audio ref={audioRef} src={soundUrl} onEnded={() => setIsPlaying(false)} />
              <button 
                onClick={toggleSound}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  width: '100%',
                  padding: '12px 16px',
                  background: isPlaying ? '#2c2c2c' : '#fff',
                  color: isPlaying ? '#fff' : '#2c2c2c',
                  border: '1px solid #2c2c2c',
                  borderRadius: 4,
                  cursor: 'pointer',
                  fontSize: 14,
                  fontWeight: 500,
                  transition: 'all 0.2s ease'
                }}
              >
                {isPlaying ? (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <rect x="6" y="4" width="4" height="16" rx="1"/>
                    <rect x="14" y="4" width="4" height="16" rx="1"/>
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                )}
                {isPlaying ? 'Pause Sound' : 'Listen to the Sound'}
              </button>
              <p style={{fontSize: 12, color: '#888', marginTop: 8, textAlign: 'center'}}>
                Hear what this soundbox plays
              </p>
            </div>
          )}
          
          <button onClick={() => onAdd(product)} style={{width: '100%', padding: '14px 32px', background: '#222', color: '#fff', border: 'none', fontSize: 13, letterSpacing: '0.5px', marginBottom: 16}}>
            ADD TO BAG
          </button>
          
          <p style={{fontSize: 12, color: '#888', textAlign: 'center'}}>Free delivery on orders over £30</p>
          
          <div style={{marginTop: 32, paddingTop: 20, borderTop: '1px solid #eee', fontSize: 12, color: '#888'}}>
            <p style={{marginBottom: 4}}>SKU: {product.sku}</p>
            {product.ean && <p>EAN: {product.ean}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}

// Stripe initialization
// Using lazy-loaded Stripe from getStripe()

function CheckoutPage({ cart, cartTotal, onBack, updateQuantity, onOrderComplete }) {
  const [formData, setFormData] = useState({
    email: '', firstName: '', lastName: '', address: '', city: '', postcode: '', phone: '', country: 'United Kingdom'
  });
  const [processing, setProcessing] = useState(false);
  const [orderComplete, setOrderComplete] = useState(false);
  const [orderNumber, setOrderNumber] = useState(null);
  const [cardError, setCardError] = useState(null);
  const [cardComplete, setCardComplete] = useState(false);
  const [stripe, setStripe] = useState(null);
  const [elements, setElements] = useState(null);
  const cardElementRef = useRef(null);
  
  // Initialize Stripe Elements
  useEffect(() => {
    const initStripe = async () => {
      const stripeInstance = await getStripe();
      setStripe(stripeInstance);
      
      const elementsInstance = stripeInstance.elements();
      setElements(elementsInstance);
      
      // Create card element
      const cardElement = elementsInstance.create('card', {
        style: {
          base: {
            fontSize: '14px',
            fontFamily: 'DM Sans, -apple-system, sans-serif',
            color: '#2c2c2c',
            '::placeholder': { color: '#999' },
          },
          invalid: { color: '#dc2626' },
        },
        hidePostalCode: true, // We collect this separately
      });
      
      // Mount when container is ready
      const mountCard = () => {
        const container = document.getElementById('card-element');
        if (container && !cardElementRef.current) {
          cardElement.mount('#card-element');
          cardElementRef.current = cardElement;
          
          cardElement.on('change', (event) => {
            setCardError(event.error ? event.error.message : null);
            setCardComplete(event.complete);
          });
        }
      };
      
      // Try mounting immediately and with a delay
      mountCard();
      setTimeout(mountCard, 100);
    };
    
    initStripe();
    
    return () => {
      if (cardElementRef.current) {
        cardElementRef.current.destroy();
        cardElementRef.current = null;
      }
    };
  }, []);
  
  // Country list - UK, EU, USA, Canada
  const COUNTRIES = [
    { name: 'United Kingdom', code: 'UK' },
    { name: '── Europe ──', code: '', disabled: true },
    { name: 'Austria', code: 'AT' },
    { name: 'Belgium', code: 'BE' },
    { name: 'Denmark', code: 'DK' },
    { name: 'Finland', code: 'FI' },
    { name: 'France', code: 'FR' },
    { name: 'Germany', code: 'DE' },
    { name: 'Ireland', code: 'IE' },
    { name: 'Italy', code: 'IT' },
    { name: 'Netherlands', code: 'NL' },
    { name: 'Norway', code: 'NO' },
    { name: 'Poland', code: 'PL' },
    { name: 'Portugal', code: 'PT' },
    { name: 'Spain', code: 'ES' },
    { name: 'Sweden', code: 'SE' },
    { name: 'Switzerland', code: 'CH' },
    { name: '── North America ──', code: '', disabled: true },
    { name: 'United States', code: 'US' },
    { name: 'Canada', code: 'CA' },
  ];
  
  // Calculate shipping based on country
  const isUK = formData.country === 'United Kingdom';
  const isTestOrder = cart.some(item => item.sku === 'TEST001');
  const freeShipping = isTestOrder || (isUK && cartTotal >= 30);
  const shippingCost = isTestOrder ? 0 : (isUK ? (freeShipping ? 0 : 4.99) : 14.99);
  const orderTotal = cartTotal + shippingCost;
  
  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!stripe || !cardElementRef.current) {
      alert('Payment system is loading. Please wait a moment and try again.');
      return;
    }
    
    if (!cardComplete) {
      setCardError('Please enter your card details');
      return;
    }
    
    setProcessing(true);
    setCardError(null);
    
    try {
      // Step 1: Create payment intent on backend
      const intentResponse = await fetch(`${API_BASE}/api/checkout/create-payment-intent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: Math.round(orderTotal * 100), // Stripe uses cents
          currency: 'gbp'
        })
      });
      
      if (!intentResponse.ok) {
        const err = await intentResponse.json();
        throw new Error(err.detail || 'Failed to create payment');
      }
      
      const { client_secret, payment_intent_id } = await intentResponse.json();
      
      // Step 2: Confirm payment with Stripe
      const { error: stripeError, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
        payment_method: {
          card: cardElementRef.current,
          billing_details: {
            name: `${formData.firstName} ${formData.lastName}`,
            email: formData.email,
            phone: formData.phone || undefined,
            address: {
              line1: formData.address,
              city: formData.city,
              postal_code: formData.postcode,
              country: COUNTRIES.find(c => c.name === formData.country)?.code || 'GB'
            }
          }
        }
      });
      
      if (stripeError) {
        throw new Error(stripeError.message);
      }
      
      if (paymentIntent.status !== 'succeeded') {
        throw new Error('Payment was not successful. Please try again.');
      }
      
      // Step 3: Create order in Zoho
      const orderData = {
        items: cart.map(item => ({
          sku: item.sku,
          quantity: item.quantity,
          price: item.price,
          name: item.name
        })),
        customer: {
          email: formData.email,
          name: `${formData.firstName} ${formData.lastName}`,
          phone: formData.phone || '',
          address: {
            address: formData.address,
            city: formData.city,
            state: '',
            zip: formData.postcode,
            country: formData.country
          }
        },
        shipping_method: isUK ? 'standard' : 'international',
        payment_intent_id: payment_intent_id
      };
      
      const orderResponse = await fetch(`${API_BASE}/api/checkout/place-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      });
      
      if (!orderResponse.ok) {
        const err = await orderResponse.json();
        throw new Error(err.detail || 'Failed to create order');
      }
      
      const { order_number } = await orderResponse.json();
      
      setOrderNumber(order_number);
      setOrderComplete(true);
      
    } catch (error) {
      console.error('Checkout error:', error);
      setCardError(error.message || 'Something went wrong. Please try again.');
    } finally {
      setProcessing(false);
    }
  };
  
  if (orderComplete) {
    return (
      <div style={{maxWidth: 600, margin: '0 auto', padding: '80px 20px', textAlign: 'center'}}>
        <div style={{fontSize: 48, marginBottom: 24}}>✓</div>
        <h1 style={{fontSize: 28, fontWeight: 500, marginBottom: 16}}>Thank you for your order!</h1>
        <p style={{fontSize: 16, color: '#666', marginBottom: 8}}>Order #{orderNumber}</p>
        <p style={{fontSize: 14, color: '#888', marginBottom: 32}}>We've sent a confirmation email to {formData.email}</p>
        <button onClick={onBack} style={{padding: '14px 32px', background: '#222', color: '#fff', border: 'none', fontSize: 13}}>Continue Shopping</button>
      </div>
    );
  }
  
  return (
    <div style={{maxWidth: 1000, margin: '0 auto', padding: '40px 20px'}}>
      <button onClick={onBack} style={{background: 'none', border: 'none', fontSize: 13, color: '#666', marginBottom: 30, display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="m15 18-6-6 6-6"/></svg>
        Back to shop
      </button>
      
      <h1 style={{fontSize: 24, fontWeight: 500, marginBottom: 40}}>Checkout</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="checkout-form-grid" style={{display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: 60}}>
          {/* Form */}
          <div>
            <h2 style={{fontSize: 16, fontWeight: 500, marginBottom: 20}}>Contact</h2>
            <input name="email" type="email" placeholder="Email" required value={formData.email} onChange={handleChange} style={inputStyle} />
            
            <h2 style={{fontSize: 16, fontWeight: 500, marginTop: 32, marginBottom: 20}}>Delivery</h2>
            <div className="checkout-name-grid" style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 12}}>
              <input name="firstName" placeholder="First name" required value={formData.firstName} onChange={handleChange} style={inputStyle} />
              <input name="lastName" placeholder="Last name" required value={formData.lastName} onChange={handleChange} style={inputStyle} />
            </div>
            <input name="address" placeholder="Address" required value={formData.address} onChange={handleChange} style={{...inputStyle, marginBottom: 12}} />
            <div className="checkout-city-grid" style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 12}}>
              <input name="city" placeholder="City" required value={formData.city} onChange={handleChange} style={inputStyle} />
              <input name="postcode" placeholder="Postcode" required value={formData.postcode} onChange={handleChange} style={inputStyle} />
            </div>
            <select name="country" value={formData.country} onChange={handleChange} style={{...inputStyle, marginBottom: 12}}>
              {COUNTRIES.map(c => (
                <option key={c.name} value={c.name} disabled={c.disabled}>{c.name}</option>
              ))}
            </select>
            <input name="phone" type="tel" placeholder="Phone (optional)" value={formData.phone} onChange={handleChange} style={inputStyle} />
            
            <h2 style={{fontSize: 16, fontWeight: 500, marginTop: 32, marginBottom: 20}}>Payment</h2>
            <div style={{padding: 16, border: '1px solid #ddd', borderRadius: 4, marginBottom: 12}}>
              <div id="card-element" style={{minHeight: 24}}></div>
            </div>
            {cardError && <p style={{color: '#dc2626', fontSize: 13, marginBottom: 12}}>{cardError}</p>}
            <p style={{fontSize: 12, color: '#888', marginBottom: 24}}>Your payment is processed securely by Stripe.</p>
            
            <button type="submit" disabled={processing} style={{width: '100%', padding: '16px 32px', background: processing ? '#888' : '#222', color: '#fff', border: 'none', fontSize: 14, cursor: processing ? 'not-allowed' : 'pointer'}}>
              {processing ? 'Processing...' : `Pay £${orderTotal.toFixed(2)}`}
            </button>
          </div>
          
          {/* Order Summary */}
          <div className="order-summary">
            <div style={{background: '#f8f8f8', padding: 24}}>
              <h2 style={{fontSize: 16, fontWeight: 500, marginBottom: 20}}>Order Summary</h2>
              {cart.map(item => (
                <div key={item.sku} style={{display: 'flex', gap: 12, marginBottom: 16, paddingBottom: 16, borderBottom: '1px solid #eee'}}>
                  <div style={{width: 60, height: 60, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                    {item.has_image ? <img src={getImageUrl(item.image_url, 'thumb')} alt={item.name} style={{maxWidth: '90%', maxHeight: '90%'}} /> : <span style={{color: '#ddd'}}>✦</span>}
                  </div>
                  <div style={{flex: 1}}>
                    <p style={{fontSize: 13, marginBottom: 4}}>{item.name}</p>
                    <p style={{fontSize: 12, color: '#888'}}>Qty: {item.quantity}</p>
                  </div>
                  <p style={{fontSize: 13}}>£{(item.price * item.quantity).toFixed(2)}</p>
                </div>
              ))}
              
              <div style={{paddingTop: 16}}>
                <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 8}}>
                  <span>Subtotal</span>
                  <span>£{cartTotal.toFixed(2)}</span>
                </div>
                <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 12, color: freeShipping ? '#22c55e' : '#666'}}>
                  <span>Shipping</span>
                  <span>{freeShipping ? 'Free' : `£${shippingCost.toFixed(2)}`}</span>
                </div>
                <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 16, fontWeight: 500, paddingTop: 12, borderTop: '1px solid #ddd'}}>
                  <span>Total</span>
                  <span>£{orderTotal.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}

const inputStyle = { width: '100%', padding: '14px 16px', border: '1px solid #ddd', fontSize: 14, outline: 'none' };

function CartDrawer({ cart, cartOpen, setCartOpen, cartTotal, freeShipping, shippingCost, orderTotal, updateQuantity, onCheckout }) {
  if (!cartOpen) return null;
  
  const progressToFree = Math.min((cartTotal / 30) * 100, 100);
  const amountToFree = Math.max(30 - cartTotal, 0);
  
  return (
    <>
      {/* Backdrop */}
      <div onClick={() => setCartOpen(false)} style={{position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.3)', zIndex: 200}} />
      
      {/* Drawer */}
      <div className="cart-drawer" style={{position: 'fixed', top: 0, right: 0, bottom: 0, width: 420, background: '#fff', zIndex: 201, display: 'flex', flexDirection: 'column'}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px', borderBottom: '1px solid #eee'}}>
          <h2 style={{fontSize: 16, fontWeight: 500}}>Shopping Bag ({cart.reduce((sum, item) => sum + item.quantity, 0)})</h2>
          <button onClick={() => setCartOpen(false)} style={{background: 'none', border: 'none', fontSize: 24, cursor: 'pointer'}}>×</button>
        </div>
        
        {/* Free shipping progress */}
        {!freeShipping && cartTotal > 0 && (
          <div style={{padding: '16px 20px', background: '#f8f8f8', borderBottom: '1px solid #eee'}}>
            <p style={{fontSize: 12, marginBottom: 8}}>Add £{amountToFree.toFixed(2)} more for free delivery</p>
            <div style={{height: 4, background: '#e5e5e5', borderRadius: 2}}>
              <div style={{height: '100%', width: `${progressToFree}%`, background: '#22c55e', borderRadius: 2, transition: 'width 0.3s'}} />
            </div>
          </div>
        )}
        
        {/* Items */}
        <div style={{flex: 1, overflowY: 'auto', padding: 20}}>
          {cart.length === 0 ? (
            <p style={{color: '#888', textAlign: 'center', marginTop: 40}}>Your bag is empty</p>
          ) : (
            cart.map(item => (
              <div key={item.sku} style={{display: 'flex', gap: 16, marginBottom: 20, paddingBottom: 20, borderBottom: '1px solid #eee'}}>
                <div style={{width: 80, height: 80, background: '#f8f8f8', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                  {item.has_image ? <img src={getImageUrl(item.image_url, 'thumb')} alt={item.name} style={{maxWidth: '90%', maxHeight: '90%'}} /> : <span style={{color: '#ddd', fontSize: 24}}>✦</span>}
                </div>
                <div style={{flex: 1}}>
                  <p style={{fontSize: 13, marginBottom: 4}}>{item.name}</p>
                  <p style={{fontSize: 14, fontWeight: 500, marginBottom: 8}}>£{item.price.toFixed(2)}</p>
                  <div style={{display: 'flex', alignItems: 'center', gap: 8}}>
                    <button onClick={() => updateQuantity(item.sku, item.quantity - 1)} style={qtyBtn}>−</button>
                    <span style={{fontSize: 13, minWidth: 20, textAlign: 'center'}}>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.sku, item.quantity + 1)} style={qtyBtn}>+</button>
                    <button onClick={() => updateQuantity(item.sku, 0)} style={{marginLeft: 'auto', background: 'none', border: 'none', fontSize: 12, color: '#888', textDecoration: 'underline', cursor: 'pointer'}}>Remove</button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
        
        {/* Footer */}
        {cart.length > 0 && (
          <div style={{padding: 20, borderTop: '1px solid #eee'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: 13}}>
              <span>Subtotal</span>
              <span>£{cartTotal.toFixed(2)}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 16, fontSize: 13, color: freeShipping ? '#22c55e' : '#666'}}>
              <span>Shipping</span>
              <span>{freeShipping ? 'Free' : `£${shippingCost.toFixed(2)}`}</span>
            </div>
            <button onClick={onCheckout} style={{width: '100%', padding: '14px 24px', background: '#222', color: '#fff', border: 'none', fontSize: 13}}>Checkout · £{orderTotal.toFixed(2)}</button>
          </div>
        )}
      </div>
    </>
  );
}

const qtyBtn = { width: 28, height: 28, border: '1px solid #ddd', background: '#fff', cursor: 'pointer', fontSize: 14 }