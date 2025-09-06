from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.db.models.functions import Now  # Django 5.x

class BaseOrdenPublicado(models.Model):
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True,db_default=Now())
    actualizado = models.DateTimeField(auto_now=True,db_default=Now())

    class Meta:
        abstract = True
        ordering = ["orden", "-creado"]

# 1) HERO / SLIDER
class HeroSlide(BaseOrdenPublicado):
    titulo = models.CharField(max_length=150)
    subtitulo = models.CharField(max_length=250, blank=True)
    boton1_texto = models.CharField(max_length=40, blank=True)
    boton1_url = models.URLField(blank=True)
    boton2_texto = models.CharField(max_length=40, blank=True)
    boton2_url = models.URLField(blank=True)
    imagen = models.ImageField(upload_to="inicio/hero/")

    def __str__(self):
        return self.titulo

# 2) VALORES / CARDS PEQUEÑAS CON ICONO
class ValorCard(BaseOrdenPublicado):
    titulo = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, blank=True)
    icono = models.ImageField(upload_to="inicio/icons/", blank=True, null=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)[:90]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

# 3) PROYECTOS EN MOVIMIENTO (cards del carrusel)
class ProyectoCard(BaseOrdenPublicado):
    titulo = models.CharField(max_length=120)
    resumen = models.CharField(max_length=220, blank=True)
    imagen = models.ImageField(upload_to="inicio/proyectos/")
    url = models.URLField(blank=True)
    etiqueta = models.CharField(max_length=30, blank=True)  # p.ej. “Ecstatic Dance”

    def __str__(self):
        return self.titulo

# 4) PRODUCTOS (grid de 4)
class ProductoItem(BaseOrdenPublicado):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="inicio/productos/")
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    precio_tachado = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    url = models.URLField(blank=True)  # o reversa a url de detalle

    def __str__(self):
        return self.titulo

# 5) GALERÍA / INSTAGRAM
class InstaFoto(BaseOrdenPublicado):
    imagen = models.ImageField(upload_to="inicio/galerias/")
    alt = models.CharField(max_length=160, blank=True)
    enlace = models.URLField(blank=True)  # si quieres que haga click a algo

    def __str__(self):
        return self.alt or f"Foto #{self.pk}"

#GALERIA INICIAL ULTIMOS EVENTOS

class Gallery(BaseOrdenPublicado):
    SECCIONES = [
        ("home_cabecera", "Home – Cabecera"),
        ("home_ult_evento", "Home – Último evento"),
        ("nosotros_cabecera", "Nosotros – Cabecera"),
        ("proyectos_movimiento", "Home – Proyecto movimiento"),
        ("participa_estancias", "Participa – Estancias"),
    ]
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    seccion = models.CharField(max_length=50, choices=SECCIONES, default="home_cabecera")
    descripcion = models.TextField(blank=True)
    portada = models.ImageField(upload_to="inicio/galerias/portadas/", blank=True)
    alt_portada = models.CharField(max_length=200, blank=True)

    # ... (campos que ya tienes)
    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Galeria ultimo evento"
        verbose_name_plural = "Galeria ultimos eventos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class GalleryItem(BaseOrdenPublicado):
    galeria = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="items")
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="inicio/galerias/items/")
    alt = models.CharField(max_length=200, blank=True)
    credito = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Separar por comas")

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Galeria ultimo evento item"
        verbose_name_plural = "Galeria ultimo evento item"

    def __str__(self):
        base = self.titulo or self.alt or self.imagen.name
        return f"{self.galeria.titulo} – {base}"
