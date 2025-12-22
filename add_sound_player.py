#!/usr/bin/env python3
"""Add sound player to Relaxound products on product page"""

with open('/Users/matt/Desktop/home-and-verse/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add sound mapping constant after CLOUDINARY_BASE
sound_mapping = '''
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
'''

# Insert after IMAGE_EXTRAS
if 'RELAXOUND_SOUNDS' not in content:
    insert_point = content.find('const IMAGE_EXTRAS =')
    if insert_point > 0:
        # Find end of IMAGE_EXTRAS line
        end_point = content.find(';', insert_point) + 1
        content = content[:end_point] + '\n' + sound_mapping + content[end_point:]
        print("Added RELAXOUND_SOUNDS mapping")
    else:
        print("Could not find IMAGE_EXTRAS - trying alternative insertion point")
        insert_point = content.find("const getImageUrl")
        content = content[:insert_point] + sound_mapping + '\n' + content[insert_point:]
        print("Added RELAXOUND_SOUNDS mapping (alternative location)")

# Now add the sound player component and button to ProductPage
# Find the ProductPage function and add sound player state and UI

# Add state for audio player in ProductPage
old_product_state = 'const [selectedImage, setSelectedImage] = React.useState(0);'
new_product_state = '''const [selectedImage, setSelectedImage] = React.useState(0);
  const [isPlaying, setIsPlaying] = React.useState(false);
  const audioRef = React.useRef(null);
  
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
  React.useEffect(() => {
    setIsPlaying(false);
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  }, [product.sku]);'''

if 'const [isPlaying' not in content:
    content = content.replace(old_product_state, new_product_state)
    print("Added audio state to ProductPage")

# Add the play button after the stock indicator
old_stock = '''<div style={{display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24}}>
            <span style={{width: 8, height: 8, borderRadius: '50%', background: '#22c55e'}} />
            <span style={{fontSize: 13, color: '#666'}}>In stock ({product.stock} available)</span>
          </div>'''

new_stock = '''<div style={{display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24}}>
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
          )}'''

if 'Sound player for Relaxound' not in content:
    content = content.replace(old_stock, new_stock)
    print("Added sound player button to ProductPage")

with open('/Users/matt/Desktop/home-and-verse/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! Relaxound products now have a 'Listen to the Sound' button")
