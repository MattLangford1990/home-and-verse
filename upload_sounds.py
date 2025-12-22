#!/usr/bin/env python3
"""Upload Relaxound sound files to Cloudinary"""

import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dcfbgveei",
    api_key="657552718963831",
    api_secret="CqvJk9xq5wxEcrhmOGHjFYc8r_A",
    secure=True
)

sound_files = {
    'zwitscherbox': '/Users/matt/Downloads/Zwitscherbox_soundfile_20sec.mp3',
    'lakesidebox': '/Users/matt/Downloads/Lakesidebox_soundfile_20sec.mp3',
    'oceanbox': '/Users/matt/Downloads/Oceanbox_soundfile_20sec.mp3',
    'junglebox': '/Users/matt/Downloads/Junglebox Soundfile Asien Teaser 30s.mp3',
}

for name, filepath in sound_files.items():
    print(f'Uploading {name}...')
    result = cloudinary.uploader.upload(
        filepath,
        public_id=f'sounds/{name}',
        resource_type='video',  # Cloudinary uses 'video' for audio files
        overwrite=True
    )
    print(f'  -> {result["secure_url"]}')

print('\nDone!')
