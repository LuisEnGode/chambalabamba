# apps/donaciones/models.py
from django.db import models
from django.utils.text import slugify

class DonacionSection(models.Model):
    # Identificador para colocarla donde la necesites (ej. "home_callout")
    slug = models.SlugField(max_length=60, unique=True, help_text="Ej: home_callout")
    titulo_superior = models.CharField(max_length=120, default="Llamado Consciente")
    titulo = models.CharField(max_length=180, default="Sanación y Regeneración en Chambalabamba")
    descripcion = models.TextField(
        default=(
            "En nuestra Ecocentro, practicamos la sanación y el cultivo de una "
            "conciencia ecológica y espiritual. Tu apoyo nos ayuda a expandir este "
            "espacio de transformación, donde la tierra y el ser se armonizan."
        )
    )
    progreso = models.PositiveIntegerField(default=55, help_text="0–100 (muestra la barra de progreso)")
    cta_titulo = models.CharField(max_length=120, default="Apoya este Espacio")
    cta_boton_texto = models.CharField(max_length=60, default="Contribuir con Amor")
    cta_placeholder_otro = models.CharField(max_length=40, default="$ Otro")

    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "slug"]
        verbose_name = "Sección de Donaciones / Donations Section"
        verbose_name_plural = "Secciones de Donaciones / Donations Sections"

    def __str__(self):
        return f"{self.slug} – {self.titulo}"


class DonacionMonto(models.Model):
    section = models.ForeignKey(DonacionSection, on_delete=models.CASCADE, related_name="montos")
    # Guarda el valor como entero en centavos o como texto. Aquí simple:
    etiqueta = models.CharField(max_length=20, help_text='Ej: "$100"')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Monto sugerido / Suggested Amount"
        verbose_name_plural = "Montos sugeridos / Suggested Amounts"

    def __str__(self):
        return f"{self.section.slug}: {self.etiqueta}"
from django.db import models

# Create your models here.
