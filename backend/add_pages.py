"""
Add Customer Service & About pages to Home & Verse
"""

import re

# Read the file
with open('/Users/matt/Desktop/home-and-verse/preview.html', 'r') as f:
    content = f.read()

# New page components to insert after AboutPage
NEW_PAGES = '''
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
          <li style={{marginBottom: 12}}>Email us at <a href="mailto:returns@homeandverse.com" style={{color: '#222'}}>returns@homeandverse.com</a> with your order number</li>
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
  const [openFaq, setOpenFaq] = React.useState(null);
  
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
      a: "We offer a 30-day returns policy on unused items in original packaging. Simply email us at returns@homeandverse.com and we'll send you a free returns label."
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
        <a href="mailto:hello@homeandverse.com" style={{color: '#222', fontWeight: 500}}>Contact us at hello@homeandverse.com</a>
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
            <a href="mailto:hello@homeandverse.com" style={{color: '#222'}}>hello@homeandverse.com</a>
            <p style={{fontSize: 13, color: '#888', marginTop: 8}}>We aim to reply within 24 hours</p>
          </div>
          
          <div style={{padding: 32, background: '#f8f8f8', textAlign: 'center'}}>
            <div style={{fontSize: 24, marginBottom: 16}}>📞</div>
            <h3 style={{fontSize: 16, fontWeight: 500, marginBottom: 8}}>Phone</h3>
            <a href="tel:+441onal" style={{color: '#222'}}>01onal 123456</a>
            <p style={{fontSize: 13, color: '#888', marginTop: 8}}>Mon-Fri 9am-5pm</p>
          </div>
        </div>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Trade Enquiries</h2>
        
        <p style={{marginBottom: 24}}>
          Are you a retailer interested in stocking our brands? We'd love to hear from you. As the exclusive UK distributor for Räder, Remember, My Flame, and Relaxound, we offer competitive trade terms and dedicated account support.
        </p>
        
        <p style={{marginBottom: 24}}>
          Please email <a href="mailto:trade@homeandverse.com" style={{color: '#222'}}>trade@homeandverse.com</a> with details about your business and we'll be in touch.
        </p>
        
        <h2 style={{fontSize: 20, fontWeight: 500, marginTop: 48, marginBottom: 20, color: '#222'}}>Press & Media</h2>
        
        <p style={{marginBottom: 24}}>
          For press enquiries, product samples, or high-resolution images, please contact <a href="mailto:press@homeandverse.com" style={{color: '#222'}}>press@homeandverse.com</a>
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
          We're always looking for ways to improve. If you have suggestions, we'd love to hear them at hello@homeandverse.com
        </p>
      </div>
    </div>
  );
}

'''

# Find the end of AboutPage function and insert new pages after it
about_page_end = content.find('function ProductsPage')
if about_page_end == -1:
    print("Could not find insertion point")
    exit(1)

content = content[:about_page_end] + NEW_PAGES + content[about_page_end:]

# Update footer links to be clickable
old_footer = '''<div>
              <h4 style={footerHeading}>Customer Service</h4>
              <p style={footerLink}>Delivery Information</p>
              <p style={footerLink}>Returns & Exchanges</p>
              <p style={footerLink}>FAQs</p>
              <p style={footerLink}>Contact Us</p>
            </div>
            <div>
              <h4 style={footerHeading}>About</h4>
              <p onClick={() => { setView('about'); window.scrollTo(0, 0); }} style={{...footerLink, cursor: 'pointer'}}>Our Story</p>
              <p style={footerLink}>Sustainability</p>
            </div>'''

new_footer = '''<div>
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
            </div>'''

content = content.replace(old_footer, new_footer)

# Now add the view rendering for new pages - find where AboutPage is rendered
old_about_render = "{view === 'about' && selectedProduct && ("
# Actually let's look for the right pattern
old_view_render = '''        {view === 'about' && (
          <AboutPage onBack={goHome} />
        )}'''

new_view_render = '''        {view === 'about' && (
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
        )}'''

content = content.replace(old_view_render, new_view_render)

# Write the file
with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w') as f:
    f.write(content)

print("Added all new pages!")
