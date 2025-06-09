from PIL import Image, ImageFilter
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io
import os

def get_blurred_image_url(image_path, request):
    """
    Blurs the image at the given path, saves it to 'media/blurred/', and returns its absolute URL.
    """
    try:
        with Image.open(image_path) as img:
            blurred = img.filter(ImageFilter.GaussianBlur(radius=10))
            buffer = io.BytesIO()
            blurred.save(buffer, format='JPEG')
            buffer.seek(0)

            filename = f"blurred_{os.path.basename(image_path)}"
            blurred_rel_path = os.path.join("blurred", filename)

            if not default_storage.exists(blurred_rel_path):
                default_storage.save(blurred_rel_path, ContentFile(buffer.read()))

            return request.build_absolute_uri(default_storage.url(blurred_rel_path))

    except Exception as e:
        print(f"Blurring error: {e}")
        return None
