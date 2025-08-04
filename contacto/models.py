from django.db import models
from django.utils import timezone

class Contacto(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    subject = models.CharField(max_length=200, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de envío")

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Mensaje de {self.name} - {self.subject}"
