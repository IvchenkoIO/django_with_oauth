from django.apps import AppConfig


class CustomScopesAndPoliciesAppConfig(AppConfig):
    
	"""
    Configuration class for the custom scopes and policies app.

    Attributes:
        default_auto_field (str): Default primary key field type for models in this app.
        name (str): Full Python path to the application.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_scopes_and_policies_app'
