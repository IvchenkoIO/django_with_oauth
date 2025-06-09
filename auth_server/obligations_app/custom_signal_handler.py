from django.db.models.signals import post_save
from django.dispatch import receiver
from oauth2_provider.models import AccessToken
from obligations_app.models import OAuthTokenLog
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

print("✅ Loading SignalHandlers…")
@receiver(post_save, sender=AccessToken)
def token_created_handler(sender, instance, created, **kwargs):
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