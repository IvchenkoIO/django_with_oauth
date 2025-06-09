from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class OAuthTokenLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    token_type = models.CharField(max_length=50, blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Log for user {self.user_id} with client {self.client_id} at {self.timestamp}"