from django.apps import AppConfig


class KartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kart'

    def ready(self):
        from . import signals
