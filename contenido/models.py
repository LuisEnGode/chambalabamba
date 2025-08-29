from django.db import models

# Create your models here.
# apps/contenido/models.py
from django.db import models
from django.utils.text import slugify

class MediaAsset(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="media/")
    alt = models.CharField(max_length=200, blank=True)
    credito = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Separar por comas")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Gallery(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Galerías"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class GalleryItem(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="items")
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.gallery} · {self.asset} ({self.orden})"

class Flyer(models.Model):
    RATIO_CHOICES = [
        ("1x1", "1:1"),
        ("4x5", "4:5 (IG 1080×1350)"),
        ("16x9", "16:9 (1920×1080)"),
        ("9x16", "9:16 (stories)"),
    ]
    titulo = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to="flyers/")
    ratio = models.CharField(max_length=5, choices=RATIO_CHOICES, default="4x5")
    alt = models.CharField(max_length=200, blank=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Placement(models.Model):
    """
    Slot reutilizable por clave. Uno de los dos campos apunta al contenido.
    Ej: key='home_hero' -> flyer destacado; key='galeria_footer' -> gallery.
    """
    key = models.SlugField(unique=True, help_text="Ej: home_hero, galeria_footer")
    flyer = models.ForeignKey(Flyer, null=True, blank=True, on_delete=models.SET_NULL)
    gallery = models.ForeignKey(Gallery, null=True, blank=True, on_delete=models.SET_NULL)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.key
