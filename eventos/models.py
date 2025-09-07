from django.db import models
from django.utils.text import slugify

class Festival(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    date = models.CharField(max_length=200, verbose_name="Fecha")
    time = models.CharField(max_length=200, verbose_name="Hora")
    place = models.CharField(max_length=200, verbose_name="Lugar")
    image = models.CharField(max_length=255, verbose_name="Imagen") # Changed from ImageField to CharField
    slug = models.SlugField(unique=True, max_length=200, blank=True, help_text="Dejar en blanco para autogenerar.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Festival"
        verbose_name_plural = "Festivales"

class TallerDetail(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    schedule = models.CharField(max_length=200, verbose_name="Horario")
    place = models.CharField(max_length=200, verbose_name="Lugar")
    image = models.ImageField(upload_to='talleres', verbose_name="Imagen")
    flyer = models.ImageField(upload_to='talleres/flyers', verbose_name="Flyer", null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True, help_text="Dejar en blanco para autogenerar.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sección: Lista de Talleres"
        verbose_name_plural = "Sección: Lista de Talleres"
        db_table = 'eventos_taller'


# ──────────────────────────────────────────────────────────────────────────────
# Página de Talleres
# ──────────────────────────────────────────────────────────────────────────────

class TalleresPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField("TalleresHeader", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Header")
    intro = models.OneToOneField("TalleresIntroSection", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sección de Introducción")

    class Meta:
        verbose_name = "Página: Talleres"
        verbose_name_plural = "Página: Talleres"

    def __str__(self):
        return "Página de Talleres"

class TalleresHeader(models.Model):
    title = models.CharField(max_length=120, default="Talleres", verbose_name="Título")
    breadcrumb_label = models.CharField(max_length=120, default="Talleres", verbose_name="Breadcrumb actual")
    background = models.ImageField(upload_to="eventos/", help_text="Imagen de fondo del header")

    class Meta:
        verbose_name = "Sección: Header de Talleres"
        verbose_name_plural = "Sección: Header de Talleres"

    def __str__(self):
        return self.title

class TalleresIntroSection(models.Model):
    title = models.CharField(max_length=160, default="¡Únete a nuestros talleres transformadores!", verbose_name="Título")
    paragraph1 = models.TextField(blank=True, verbose_name="Párrafo 1")
    paragraph2 = models.TextField(blank=True, verbose_name="Párrafo 2")
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    cta_text = models.CharField(max_length=80, blank=True, default="Ver todos los talleres", verbose_name="Texto del botón")
    cta_url = models.CharField(max_length=300, blank=True, default="#talleres-grid", verbose_name="URL del botón")

    class Meta:
        verbose_name = "Sección: Introducción de Talleres"
        verbose_name_plural = "Sección: Introducción de Talleres"

    def __str__(self):
        return self.title
