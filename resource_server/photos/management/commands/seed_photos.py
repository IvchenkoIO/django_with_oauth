from django.core.management.base import BaseCommand
from photos.models import Photo, PhotoImage, BiometricData
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import make_aware
from datetime import datetime, timedelta, date
import random, os

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
        Create sample data
        """
        image_filenames = ['surgery.jpg', 'profile.jpg', 'checkup.jpg']

        # Create surgery record
        photo = Photo.objects.create(
            patient_name="John Doe",
            date_of_birth=date(1990, 5, 10),
            blurred=False,
        )

        # Attach images
        for filename in image_filenames:
            img_path = os.path.join('photos', 'test_assets', filename)
            if not os.path.exists(img_path):
                self.stdout.write(self.style.ERROR(f"Image not found: {filename}"))
                continue

            with open(img_path, 'rb') as img:
                image_file = SimpleUploadedFile(filename, img.read(), content_type='image/jpeg')

            PhotoImage.objects.create(
                photo=photo,
                image=image_file,
                description=""  
            )

        # Add heartrate
        base_time = make_aware(datetime(2025, 5, 1, 8, 0))
        for i in range(2000):
            BiometricData.objects.create(
                patient=photo,
                measurement_type='heart_rate',
                value=random.randint(65, 85),
                timestamp=base_time + timedelta(minutes=5 * i),
                averaged_to=None
            )

        self.stdout.write(self.style.SUCCESS("Data created"))
