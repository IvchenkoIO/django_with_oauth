from PIL import Image, ImageFilter
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from photos.privacy_config import BLUR_STRENGTH
import io
import os

def get_blurred_image_url(image_path, request, blur_level="medium"):
    """
    Dynamically blurs the image based on image size and blur level from config.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            base = min(width, height)

            # Get multiplier from config, default to medium if missing
            multiplier = BLUR_STRENGTH.get(blur_level, BLUR_STRENGTH.get("medium", 0.03))
            radius = max(1, int(base * multiplier))

            blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))
            buffer = io.BytesIO()
            blurred.save(buffer, format='JPEG')
            buffer.seek(0)

            filename = f"blurred_{blur_level}_{os.path.basename(image_path)}"
            blurred_rel_path = os.path.join("photos", "blurred", filename)

            if not default_storage.exists(blurred_rel_path):
                default_storage.save(blurred_rel_path, ContentFile(buffer.read()))

            return request.build_absolute_uri(default_storage.url(blurred_rel_path))

    except Exception as e:
        print(f"Blurring error: {e}")
        return None
