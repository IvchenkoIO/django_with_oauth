from django.apps import AppConfig


class ObligationsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obligations_app'

    def ready(self):
        import obligations_app.custom_signal_handler  # Import signals to register handlers