from django.db import models
from django.utils.text import slugify

class Festival(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    date = models.CharField(max_length=200, verbose_name="Fecha")
    time = models.CharField(max_length=200, verbose_name="Hora")
    place = models.CharField(max_length=200, verbose_name="Lugar")
    image = models.ImageField(upload_to='festivales', verbose_name="Imagen", null=True, blank=True)
    flyer = models.ImageField(upload_to='festivales/flyers', verbose_name="Flyer", null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True, help_text="Dejar en blanco para autogenerar.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "1.3 Sección: Lista de Festivales"
        verbose_name_plural = "1.3 Sección: Lista de Festivales"

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
        verbose_name = "2.3 Sección: Lista de Talleres"
        verbose_name_plural = "2.3 Sección: Lista de Talleres"
        db_table = 'eventos_taller'


# ──────────────────────────────────────────────────────────────────────────────
# Página de Talleres
# ──────────────────────────────────────────────────────────────────────────────

class TalleresPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField("TalleresHeader", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Header")
    intro = models.OneToOneField("TalleresIntroSection", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sección de Introducción")

    class Meta:
        verbose_name = "2. Página: Talleres"
        verbose_name_plural = "2. Página: Talleres"

    def __str__(self):
        return "Página de Talleres"

class TalleresHeader(models.Model):
    title = models.CharField(max_length=120, default="Talleres", verbose_name="Título")
    breadcrumb_label = models.CharField(max_length=120, default="Talleres", verbose_name="Breadcrumb actual")
    background = models.ImageField(upload_to="eventos/", help_text="Imagen de fondo del header")

    class Meta:
        verbose_name = "2.1 Sección: Header de Talleres"
        verbose_name_plural = "2.1 Sección: Header de Talleres"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# Página de Festivales
# ──────────────────────────────────────────────────────────────────────────────

class FestivalesPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField("FestivalesHeader", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Header")
    intro = models.OneToOneField("FestivalesIntroSection", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sección de Introducción")

    class Meta:
        verbose_name = "1. Página: Festivales"
        verbose_name_plural = "1. Página: Festivales"

    def __str__(self):
        return "Página de Festivales"

class FestivalesHeader(models.Model):
    title = models.CharField(max_length=120, default="Festivales", verbose_name="Título")
    breadcrumb_label = models.CharField(max_length=120, default="Festivales", verbose_name="Breadcrumb actual")
    background = models.ImageField(upload_to="eventos/", help_text="Imagen de fondo del header")

    class Meta:
        verbose_name = "1.1 Sección: Header de Festivales"
        verbose_name_plural = "1.1 Sección: Header de Festivales"

    def __str__(self):
        return self.title

class FestivalesIntroSection(models.Model):
    title = models.CharField(max_length=160, default="¡Celebra con nosotros!", verbose_name="Título")
    paragraph1 = models.TextField(blank=True, verbose_name="Párrafo 1")
    paragraph2 = models.TextField(blank=True, verbose_name="Párrafo 2")
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    cta_text = models.CharField(max_length=80, blank=True, default="Ver todos los festivales", verbose_name="Texto del botón")
    cta_url = models.CharField(max_length=300, blank=True, default="#festivales-grid", verbose_name="URL del botón")

    class Meta:
        verbose_name = "1.2 Sección: Introducción de Festivales"
        verbose_name_plural = "1.2 Sección: Introducción de Festivales"

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
        verbose_name = "2.2 Sección: Introducción de Talleres"
        verbose_name_plural = "2.2 Sección: Introducción de Talleres"

    def __str__(self):
        return self.title
