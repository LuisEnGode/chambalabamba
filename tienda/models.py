from django.db import models

class ProductoCategoria(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Categoría de producto"
        verbose_name_plural = "Categorías de producto"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        ProductoCategoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos"
    )
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion_corta = models.CharField(max_length=240, blank=True)
    descripcion = models.TextField(blank=True)

    imagen_portada = models.ImageField(upload_to="productos/portadas/", blank=True, null=True)

    # Precios (puedes migrarlo a Decimal con 2 decimales si quieres exactitud)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_tachado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "-creado"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.titulo


class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos/items/")
    alt = models.CharField(max_length=140, blank=True)
    orden = models.PositiveIntegerField(default=0)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de producto"

    def __str__(self):
        return f"{self.producto.titulo} – {self.alt or self.imagen.name}"
from django.db import models

# Create your models here.
