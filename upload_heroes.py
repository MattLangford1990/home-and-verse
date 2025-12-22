#!/usr/bin/env python3
"""Upload hero images for homepage - with resize"""

import cloudinary
import cloudinary.uploader
import subprocess
import os

cloudinary.config(
    cloud_name="dcfbgveei",
    api_key="657552718963831",
    api_secret="CqvJk9xq5wxEcrhmOGHjFYc8r_A",
    secure=True
)

images = {
    'hero-christmas': '/Users/matt/Downloads/Rader-Images/92528_Art-F_Lichtobjekt_Weihnachtskrippe_Y23_PV_V01.jpg',
    'hero-gift': '/Users/matt/Downloads/Rader-Images/17438_Art-F_LichthäuserPoesie_LichthausHomeIsWhereTheHeartIs_Y23_PH_V02.jpg',
    'hero-homedecor': '/Users/matt/Downloads/HiDrive-Alle Fotos/ZW02_Fiori_Zwitscherbox_Ambiente_04_2021.jpg',
}

os.makedirs('/tmp/heroes', exist_ok=True)

for name, filepath in images.items():
    print(f'Processing {name}...')
    
    # Resize locally first
    output_path = f'/tmp/heroes/{name}.jpg'
    subprocess.run([
        'sips', '-Z', '1600',
        '--setProperty', 'formatOptions', '85',
        '-s', 'format', 'jpeg',
        filepath,
        '--out', output_path
    ], check=True, capture_output=True)
    
    print(f'  Resized to {os.path.getsize(output_path) / 1024 / 1024:.1f}MB')
    
    # Upload
    result = cloudinary.uploader.upload(
        output_path,
        public_id=f'heroes/{name}',
        overwrite=True
    )
    print(f'  -> {result["secure_url"]}')

print('\nDone!')
