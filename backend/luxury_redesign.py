"""
Home & Verse - Luxury Aesthetic Redesign
=========================================
Transforms the site to a premium, editorial feel with:
- Elegant serif typography
- Mood imagery sections  
- Refined color palette
- Generous whitespace
- Subtle animations
"""

# Read the current file
with open('/Users/matt/Desktop/home-and-verse/preview.html', 'r') as f:
    content = f.read()

# 1. Update fonts - add Cormorant Garamond for headings
old_fonts = '''<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">'''
new_fonts = '''<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">'''
content = content.replace(old_fonts, new_fonts)

# 2. Update base styles
old_styles = '''<style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', -apple-system, sans-serif; background: #fff; color: #222; font-size: 14px; line-height: 1.5; }
        a { text-decoration: none; color: inherit; }
        button { font-family: inherit; cursor: pointer; }
        input, select { font-family: inherit; }
        ::selection { background: #222; color: #fff; }
    </style>'''

new_styles = '''<style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'DM Sans', -apple-system, sans-serif; 
            background: #faf9f7; 
            color: #2c2c2c; 
            font-size: 14px; 
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }
        a { text-decoration: none; color: inherit; }
        button { font-family: inherit; cursor: pointer; }
        input, select { font-family: inherit; }
        ::selection { background: #2c2c2c; color: #fff; }
        
        /* Luxury heading styles */
        h1, h2, h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 400; }
        
        /* Smooth scrolling */
        html { scroll-behavior: smooth; }
        
        /* Refined transitions */
        * { transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, transform 0.3s ease, opacity 0.3s ease; }
        
        /* Elegant focus states */
        button:focus-visible, a:focus-visible { outline: 2px solid #b8a089; outline-offset: 2px; }
        
        /* Image hover zoom */
        .img-zoom { overflow: hidden; }
        .img-zoom img { transition: transform 0.6s ease; }
        .img-zoom:hover img { transform: scale(1.05); }
    </style>'''
content = content.replace(old_styles, new_styles)

# 3. Replace the HomePage function with luxurious version
old_homepage_start = "function HomePage({ products, bestsellers, onCategoryClick, onProductClick, onAdd, getCategoryCount }) {"
old_homepage_end = '''      {/* Trust Bar */}
      <section style={{padding: '40px 20px', borderTop: '1px solid #eee'}}>
        <div style={{maxWidth: 900, margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 40, textAlign: 'center'}}>
          <div>
            <p style={{fontSize: 13, fontWeight: 500, marginBottom: 2}}>Free Delivery</p>
            <p style={{fontSize: 12, color: '#888'}}>On orders over £30</p>
          </div>
          <div>
            <p style={{fontSize: 13, fontWeight: 500, marginBottom: 2}}>30-Day Returns</p>
            <p style={{fontSize: 12, color: '#888'}}>Hassle-free returns</p>
          </div>
          <div>
            <p style={{fontSize: 13, fontWeight: 500, marginBottom: 2}}>Secure Payment</p>
            <p style={{fontSize: 12, color: '#888'}}>SSL encrypted checkout</p>
          </div>
        </div>
      </section>
    </>
  );
}'''

new_homepage = '''function HomePage({ products, bestsellers, onCategoryClick, onProductClick, onAdd, getCategoryCount }) {
  const newProducts = products.slice(0, 8);
  
  // Mood image URLs (using Unsplash for placeholders - replace with your own)
  const moodImages = {
    hero: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=1600&q=80',
    candles: 'https://images.unsplash.com/photo-1602523961358-f9f03dd557db?w=800&q=80',
    lighting: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80',
    tableware: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
    living: 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=1200&q=80',
    christmas: 'https://images.unsplash.com/photo-1512389142860-9c449e58a814?w=1200&q=80',
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
      <section style={{
        background: '#2c2c2c',
        padding: '20px',
        textAlign: 'center'
      }}>
        <p style={{
          color: '#b8a089',
          fontSize: 13,
          letterSpacing: '3px',
          textTransform: 'uppercase',
          fontWeight: 300
        }}>
          Free UK Delivery Over £30 · 30-Day Returns · Gift Wrapping Available
        </p>
      </section>

      {/* Category Grid with Images */}
      <section style={{padding: '100px 20px'}}>
        <div style={{maxWidth: 1400, margin: '0 auto'}}>
          <div style={{textAlign: 'center', marginBottom: 60}}>
            <p style={{
              fontSize: 12,
              letterSpacing: '3px',
              color: '#b8a089',
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
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 24
          }}>
            {NAV_CATEGORIES.map((cat, i) => (
              <button 
                key={cat.slug} 
                onClick={() => onCategoryClick(cat.slug)}
                className="img-zoom"
                style={{
                  position: 'relative',
                  aspectRatio: i === 0 || i === 5 ? '4/5' : '4/3',
                  background: '#f0ebe4',
                  border: 'none',
                  cursor: 'pointer',
                  overflow: 'hidden',
                  gridRow: i === 0 || i === 5 ? 'span 2' : 'span 1'
                }}
              >
                {/* Category image placeholder - gradient for now */}
                <div style={{
                  position: 'absolute',
                  inset: 0,
                  background: `linear-gradient(135deg, ${
                    ['#d4c5b5', '#c9b8a8', '#bfae9e', '#d9cfc5', '#c4b5a5', '#cfc0b0'][i]
                  } 0%, ${
                    ['#e8ddd0', '#ddd0c0', '#d3c6b6', '#ebe3db', '#d8ccc0', '#e0d5c8'][i]
                  } 100%)`,
                  transition: 'transform 0.6s ease'
                }} />
                {/* Overlay */}
                <div style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'rgba(0,0,0,0.1)',
                  transition: 'background 0.3s ease'
                }} />
                {/* Category name */}
                <div style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  padding: '30px',
                  background: 'linear-gradient(to top, rgba(0,0,0,0.4) 0%, transparent 100%)'
                }}>
                  <p style={{
                    fontFamily: "'Cormorant Garamond', Georgia, serif",
                    fontSize: 24,
                    color: '#fff',
                    fontWeight: 400
                  }}>{cat.name}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Editorial Section - Brand Story */}
      <section style={{
        background: '#f5f2ed',
        padding: '120px 20px'
      }}>
        <div style={{
          maxWidth: 1200,
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 80,
          alignItems: 'center'
        }}>
          <div style={{paddingRight: 40}}>
            <p style={{
              fontSize: 12,
              letterSpacing: '3px',
              color: '#b8a089',
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
                color: '#b8a089',
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
            <div style={{
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
                color: '#b8a089',
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
        background: '#f5f2ed',
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
          {['Räder', 'Remember', 'My Flame', 'Relaxound'].map(brand => (
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
        <div style={{
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
}'''

# Find and replace the HomePage function
import re
homepage_pattern = r'function HomePage\(\{ products, bestsellers.*?\n\}'
# Actually, let's do a simpler find-replace
start_idx = content.find(old_homepage_start)
end_idx = content.find(old_homepage_end) + len(old_homepage_end)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_homepage + content[end_idx:]
    print("HomePage replaced successfully")
else:
    print(f"Could not find HomePage. Start: {start_idx}, End: {end_idx}")

# 4. Update ProductCard for more luxury feel
old_product_card_start = '''function ProductCard({ product, onClick, onAdd }) {
  const [hovered, setHovered] = React.useState(false);
  
  return (
    <div 
      style={{cursor: 'pointer'}} 
      onMouseEnter={() => setHovered(true)} 
      onMouseLeave={() => setHovered(false)}
    >
      {/* Image Container */}
      <div 
        onClick={onClick}
        style={{
          background: '#f8f8f8',
          aspectRatio: '1',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: 12,
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        {product.image_url ? (
          <img src={getImageUrl(product.image_url, 'medium')} alt={`${product.name} by ${product.brand} - Luxury European homeware from Home & Verse`} loading="lazy" style={{maxWidth: '85%', maxHeight: '85%', objectFit: 'contain', transition: 'transform 0.3s', transform: hovered ? 'scale(1.03)' : 'scale(1)'}} />
        ) : (
          <div style={{color: '#ddd', fontSize: 40}}>✦</div>
        )}'''

new_product_card_start = '''function ProductCard({ product, onClick, onAdd }) {
  const [hovered, setHovered] = React.useState(false);
  
  return (
    <div 
      style={{cursor: 'pointer'}} 
      onMouseEnter={() => setHovered(true)} 
      onMouseLeave={() => setHovered(false)}
    >
      {/* Image Container */}
      <div 
        onClick={onClick}
        style={{
          background: '#f5f2ed',
          aspectRatio: '1',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: 16,
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        {product.image_url ? (
          <img src={getImageUrl(product.image_url, 'medium')} alt={`${product.name} by ${product.brand} - Luxury European homeware from Home & Verse`} loading="lazy" style={{maxWidth: '80%', maxHeight: '80%', objectFit: 'contain', transition: 'transform 0.5s ease', transform: hovered ? 'scale(1.05)' : 'scale(1)'}} />
        ) : (
          <div style={{color: '#d4c5b5', fontSize: 40}}>✦</div>
        )}'''

content = content.replace(old_product_card_start, new_product_card_start)

# 5. Update header/nav styling 
old_header = '''<p style={{fontSize: 12, color: '#fff', letterSpacing: '0.5px'}}>
              Free UK delivery on orders over £30 · 30-day returns
            </p>'''
new_header = '''<p style={{fontSize: 11, color: 'rgba(255,255,255,0.9)', letterSpacing: '2px', textTransform: 'uppercase', fontWeight: 300}}>
              Free UK delivery on orders over £30 · 30-day returns
            </p>'''
content = content.replace(old_header, new_header)

# Update logo/brand styling
old_logo = '''<span style={{fontWeight: 600, fontSize: 18, letterSpacing: '2px'}}>HOME & VERSE</span>'''
new_logo = '''<span style={{fontFamily: "'Cormorant Garamond', Georgia, serif", fontWeight: 400, fontSize: 22, letterSpacing: '3px'}}>HOME & VERSE</span>'''
content = content.replace(old_logo, new_logo)

# Write the updated file
with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w') as f:
    f.write(content)

print("Luxury redesign complete!")
print("\\nKey changes:")
print("- Elegant Cormorant Garamond typography for headings")
print("- Full-width hero with mood imagery")
print("- Editorial brand story section")
print("- Refined category grid with gradient placeholders")
print("- Full-width Christmas mood banner with parallax")
print("- Brands showcase section")
print("- Warmer, more sophisticated color palette (#faf9f7, #f5f2ed)")
print("- Generous whitespace and refined spacing")
print("- Subtle hover animations")
