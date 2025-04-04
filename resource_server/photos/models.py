from django.db import models

# Create your models here.
from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
