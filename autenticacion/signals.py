from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TipoUsuario  # Ajusta el import según dónde esté tu modelo

@receiver(post_migrate)
def crear_tipos_usuario(sender, **kwargs):
    if sender.name == 'autenticacion':  # Cambia esto al nombre exacto de la app donde esté el modelo
        TipoUsuario.objects.get_or_create(nombre='Profesional')
        TipoUsuario.objects.get_or_create(nombre='Cliente')
