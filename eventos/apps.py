from django.apps import AppConfig
from django.apps import AppConfig

class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'


class EventosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "eventos"
    def ready(self):
        from . import signals  # carga señales