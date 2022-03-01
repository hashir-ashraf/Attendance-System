from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'Admin'
    default_auto_field = 'django.db.models.BigAutoField'
    def ready(self):
        import Admin.signals
