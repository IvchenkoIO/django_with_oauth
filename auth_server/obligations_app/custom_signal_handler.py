'''
obligations_app/custom_signal_handler.py
---------------------------------------

Signal handlers for token issuance events in the OAuth2 Authorization Server.

Responsibilities:
  - Listen for AccessToken creation signals.
  - Log token events to the OAuthTokenLog model.
  - Emit email notifications on token issuance.
  - Record events in application logs.
'''

from django.db.models.signals import post_save
from django.dispatch import receiver
from oauth2_provider.models import AccessToken
from obligations_app.models import OAuthTokenLog
from django.core.mail import send_mail
import logging
# Initialize module-level logger
logger = logging.getLogger(__name__)
# Informational print to console/log when module is loaded
print("✅ Loading SignalHandlers…")


@receiver(post_save, sender=AccessToken)
def token_created_handler(sender, instance, created, **kwargs):
    """
    Handle the post-save signal for AccessToken model.

    When a new AccessToken is created, this handler:
      1. Extracts user and client identifiers.
      2. Creates an OAuthTokenLog entry.
      3. Logs an info message to the application logger.
      4. Sends an email notification about the token issuance.

    Args:
        sender (Model): The model class (AccessToken).
        instance (AccessToken): The newly created token instance.
        created (bool): True if this is a creation event, False on updates.
        **kwargs: Additional keyword arguments from the signal.
    """

    # Only handle newly created tokens
    if created:
        # Extract details from the token instance
        user_id = instance.user.id if instance.user else 'unknown'
        client_id = instance.application.client_id if instance.application else 'unknown'
        token_type = 'Bearer'
        scope = instance.scope
        message = f"Token generated for user {user_id} with client {client_id}"
        # Create a log entry in the database
        OAuthTokenLog.objects.create(
            user_id=user_id,
            client_id=client_id,
            token_type='Bearer',
            scope=scope,
            message=message,
        )

        # Log the event to file/console
        logger.info(message)

        # Send an email notification
        send_mail(
            'Token Issued',
            message,
            'privacyengproj@gmail.com',  # Sender email address
            ['io.ivchenko@gmail.com'],  # Recipient list (adjust as needed)
            fail_silently=False,
        )