from django.db import models

# Create your models here.
from django.db import models
from django.db.models import JSONField
from oauth2_provider.models import AbstractGrant

class CustomGrant(AbstractGrant):
    policy_levels = JSONField(null=True, blank=True)
