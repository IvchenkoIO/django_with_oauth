
'''
obligations_app/models.py
-------------------------

Data model for logging OAuth token usage and obligations in the resource server.

Models:
  - OAuthTokenLog: Records each token issuance or use event with metadata for auditing.
'''

from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class OAuthTokenLog(models.Model):
    """
        Log entry for OAuth2 token actions, capturing user, client, and token metadata.

        Fields:
        timestamp (DateTimeField): Auto-generated timestamp when the log entry is created.
        user_id (CharField): Identifier for the user associated with the token.
        client_id (CharField): OAuth2 client identifier (application/client ID).
        token_type (CharField): Type of token issued (e.g., 'Bearer'); optional.
        scope (TextField): Granted scopes string; optional.
        message (TextField): Additional context or description for the log; optional.
    
    """
    timestamp = models.DateTimeField(auto_now_add=True) #Time when this log entry was created
    user_id = models.CharField(max_length=255) #Primary key or unique identifier of the user
    client_id = models.CharField(max_length=255) #OAuth2 client (application) ID associated with this token
    token_type = models.CharField(max_length=50, blank=True, null=True) #Type of token issued, e.g., 'Bearer'
    scope = models.TextField(blank=True, null=True) #Space-delimited list of scopes granted to the token
    message = models.TextField(blank=True) #Optional detailed message or context for this log entry

    def __str__(self):
        """
            Return a human-readable representation of the token log entry.

            Format: "Log for user <user_id> with client <client_id> at <timestamp>".
        """
        
        return f"Log for user {self.user_id} with client {self.client_id} at {self.timestamp}"