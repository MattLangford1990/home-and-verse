import re

# Read the file
with open('/Users/matt/Desktop/home-and-verse/preview.html', 'r') as f:
    content = f.read()

# Add the ImageLightbox component before ProductPage
lightbox = '''function ImageLightbox({ src, alt, onClose }) {
  React.useEffect(() => {
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
      }}>x</button>
      <img src={src} alt={alt} onClick={(e) => e.stopPropagation()}
        style={{maxWidth: '90vw', maxHeight: '90vh', objectFit: 'contain', cursor: 'default'}} />
    </div>
  );
}

'''

content = content.replace(
    'function ProductPage({ product, onBack, onAdd }) {',
    lightbox + 'function ProductPage({ product, onBack, onAdd }) {'
)

# Add lightbox state
content = content.replace(
    'const [selectedImage, setSelectedImage] = React.useState(0);',
    'const [selectedImage, setSelectedImage] = React.useState(0);\n  const [lightboxOpen, setLightboxOpen] = React.useState(false);'
)

# Add lightbox rendering after opening div
content = content.replace(
    '''return (
    <div style={{maxWidth: 1100, margin: '0 auto', padding: '30px 20px'}}>
      {/* Back link */}''',
    '''return (
    <div style={{maxWidth: 1100, margin: '0 auto', padding: '30px 20px'}}>
      {/* Lightbox */}
      {lightboxOpen && images.length > 0 && (
        <ImageLightbox src={`${API_BASE}${images[selectedImage]}`} alt={product.name} onClose={() => setLightboxOpen(false)} />
      )}
      {/* Back link */}'''
)

# Update main image div
old_img = '''<div style={{background: '#f8f8f8', aspectRatio: '1', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: images.length > 1 ? 12 : 0}}>'''

new_img = '''<div onClick={() => images.length > 0 && setLightboxOpen(true)} style={{background: '#f8f8f8', aspectRatio: '1', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: images.length > 1 ? 12 : 0, position: 'relative', cursor: images.length > 0 ? 'zoom-in' : 'default'}}>'''

content = content.replace(old_img, new_img)

# Add magnifying glass after the main image inside the div
old_close = '''            ) : (
              <div style={{color: '#ddd', fontSize: 80}}>✦</div>
            )}
          </div>
          
          {/* Thumbnail Strip */}'''

new_close = '''            ) : (
              <div style={{color: '#ddd', fontSize: 80}}>✦</div>
            )}
            {/* Magnifying Glass */}
            {images.length > 0 && (
              <button onClick={(e) => { e.stopPropagation(); setLightboxOpen(true); }}
                style={{position: 'absolute', bottom: 12, right: 12, width: 40, height: 40, borderRadius: '50%',
                  background: 'rgba(255,255,255,0.9)', border: '1px solid #ddd', display: 'flex',
                  alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.1)'}}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#333" strokeWidth="2">
                  <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/><path d="M11 8v6M8 11h6"/>
                </svg>
              </button>
            )}
          </div>
          
          {/* Thumbnail Strip */}'''

content = content.replace(old_close, new_close)

with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w') as f:
    f.write(content)

print('Done!')
