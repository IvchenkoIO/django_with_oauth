'''
custom_scopes_and_policies_app/models.py
----------------------------------------

Data model for extending the OAuth2 authorization code grant with custom policy levels.

Models:
  - CustomGrant: Inherits from django-oauth-toolkit's AbstractGrant and adds a JSON field
    for storing user-selected policy levels alongside the authorization code.
'''

from django.db import models

# Create your models here.
from django.db import models
from django.db.models import JSONField
from oauth2_provider.models import AbstractGrant

class CustomGrant(AbstractGrant):
	"""
    Extended grant model that captures user-defined policy levels for an OAuth2 authorization code.

    Inherits all fields from AbstractGrant (code, application, user, expires, redirect_uri, scope) and adds:
        policy_levels (JSONField): Stores a mapping of data types to selected policy levels,
                                   e.g., {"average numerical values?": "hourly", ...}.
                                   
    """


    policy_levels = JSONField(null=True, blank=True)
