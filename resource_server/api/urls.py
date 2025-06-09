from django.urls import path
from photos.views import protected_photos

urlpatterns = [
    path('photos/', protected_photos, name='photos'),
]

