from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ParticipaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "participa"
    verbose_name = "Participa"

    def ready(self):
        from .seed import _seed_estancias_once
        post_migrate.connect(_seed_estancias_once, sender=self)