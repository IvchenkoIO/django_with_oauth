from django.apps import AppConfig


class ObligationsAppConfig(AppConfig):
    """
    Configuration class for the obligation app.

    Attributes:
        default_auto_field (str): Default primary key field type for models in this app.
        name (str): Full Python path to the application.
    """


    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obligations_app'

    def ready(self):
        import obligations_app.custom_signal_handler  # Import signals to register handlers