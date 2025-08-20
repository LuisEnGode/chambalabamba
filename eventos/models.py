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

class Taller(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    schedule = models.CharField(max_length=200, verbose_name="Horario")
    place = models.CharField(max_length=200, verbose_name="Lugar")
    image = models.CharField(max_length=255, verbose_name="Imagen")
    slug = models.SlugField(unique=True, max_length=200, blank=True, help_text="Dejar en blanco para autogenerar.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"
