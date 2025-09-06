# apps/estancias/models.py
from django.db import models
from django.utils.text import slugify
from inicio.models import BaseOrdenPublicado  # reutiliza tu base


# --- Header + Página (patrón similar a 'Nosotros') ---
class ParticipaHeader(models.Model):
    title = models.CharField("Título", max_length=120, default="Participa")
    breadcrumb_label = models.CharField("Breadcrumb actual", max_length=120, default="Estancias")
    background = models.ImageField(upload_to="participa/headers/", blank=True, null=True)

    class Meta:
        verbose_name = "Sección: Header (Participa)"
        verbose_name_plural = "Sección: Header (Participa)"

    def __str__(self):
        return self.title


class ParticipaPage(models.Model):
    enabled = models.BooleanField(default=True)
    header = models.OneToOneField(ParticipaHeader, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Página: Participa"
        verbose_name_plural = "Página: Participa"

    def __str__(self):
        return "Página Participa"



class Estancia(BaseOrdenPublicado):
    SECCIONES = [
        ("participa_estancias", "Participa – Estancias"),
    ]
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    seccion = models.CharField(max_length=50, choices=SECCIONES, default="participa_estancias")
    resumen = models.TextField(blank=True)       # para el grid
    descripcion = models.TextField(blank=True)   # para el detalle
    tipo = models.CharField(max_length=120, blank=True)   # p.ej. "Casa de madera"
    lugar = models.CharField(max_length=200, blank=True, default="Ecocentro Chambalabamba")
    portada = models.ImageField(upload_to="estancias/portadas/", blank=True)
    alt_portada = models.CharField(max_length=200, blank=True)

    # Precios opcionales
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_tachado = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    # Contacto opcional (para botón WhatsApp del detalle)
    phone_whatsapp = models.CharField(max_length=32, blank=True, help_text="Solo números con código de país, ej: 5939XXXXXXX")

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Estancia"
        verbose_name_plural = "Estancias"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class EstanciaFoto(BaseOrdenPublicado):
    estancia = models.ForeignKey(Estancia, on_delete=models.CASCADE, related_name="fotos")
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="estancias/fotos/")
    alt = models.CharField(max_length=200, blank=True)

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Foto de estancia"
        verbose_name_plural = "Fotos de estancias"

    def __str__(self):
        base = self.titulo or self.alt or self.imagen.name
        return f"{self.estancia.titulo} – {base}"


class EstanciaSpec(models.Model):
    """Pares clave/valor para 'Información adicional' del detalle."""
    estancia = models.ForeignKey(Estancia, on_delete=models.CASCADE, related_name="specs")
    orden = models.PositiveIntegerField(default=0)
    clave = models.CharField(max_length=120)     # ej. "Capacidad"
    valor = models.TextField()                   # ej. "1–2 personas"

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Especificación"
        verbose_name_plural = "Especificaciones"

    def __str__(self):
        return f"{self.clave}: {self.valor[:40]}"
