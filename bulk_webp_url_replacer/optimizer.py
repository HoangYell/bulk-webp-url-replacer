"""Image optimizer - downloads and converts images to WebP."""
import os
import requests
from io import BytesIO
from PIL import Image


class ImageOptimizer:
    """Handles downloading and optimizing images."""

    def __init__(self, quality: int = 80, max_width: int = 1200):
        self.quality = quality
        self.max_width = max_width

    def download_and_optimize(self, url: str, save_path: str, format: str = 'WEBP') -> bool:
        """Downloads an image from URL and saves an optimized version."""
        print(f"Processing {url}...")
        try:
            if url.startswith(('http://', 'https://')):
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            else:
                # Treat as local file path
                img = Image.open(url)
            
            # Convert to RGB if saving as JPEG or if original is RGBA/P
            if format.upper() == 'JPEG' and img.mode != 'RGB':
                img = img.convert('RGB')
            elif img.mode == 'RGBA' and format.upper() == 'WEBP':
                # WebP supports RGBA, keep it
                pass
            elif img.mode == 'P':
                img = img.convert('RGBA' if format.upper() == 'WEBP' else 'RGB')
                
            # Resize if too large
            if img.width > self.max_width:
                ratio = self.max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            img.save(save_path, format=format, quality=self.quality, optimize=True)
            print(f"Success: Saved to {save_path}")
            return True
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return False
