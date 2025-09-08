from django.apps import AppConfig
from .seeders import _seed_donaciones_once
from django.db.models.signals import post_migrate

class DonacionesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "donaciones"

    def ready(self):
        # registra receptores post_migrate
        from . import seeders  # noqa: F401
        post_migrate.connect(_seed_donaciones_once, sender=self)