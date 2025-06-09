
from django.db import models

class Photo(models.Model):
    patient_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    face_visible = models.BooleanField(default=True)
    blurred = models.BooleanField(default=False)
    dummy_name_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.created_at.date()}"

class PhotoImage(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.photo.patient_name} at {self.uploaded_at}"

class BiometricData(models.Model):
    patient = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='biometrics')
    measurement_type = models.CharField(max_length=100)  
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    averaged_to = models.CharField(max_length=50, blank=True, null=True)  

    def __str__(self):
        return f"{self.measurement_type} at {self.timestamp}"
