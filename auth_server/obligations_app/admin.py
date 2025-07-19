from django.contrib import admin
from .models import OAuthTokenLog


# Register your models here.
@admin.register(OAuthTokenLog)
class OAuthTokenLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for OAuthTokenLog.

    Shows the timestamp, user_id, client_id, token_type and scope in list view,
    enables filtering by client_id and searching by user_id or message.
    """
    list_display = (
        'timestamp',
        'user_id',
        'client_id',
        'token_type',
        'scope',
    )
    list_filter = (
        'client_id',
        'token_type',
    )
    search_fields = (
        'user_id',
        'message',
    )
    readonly_fields = (
        'timestamp',
        'user_id',
        'client_id',
        'token_type',
        'scope',
        'message',
    )