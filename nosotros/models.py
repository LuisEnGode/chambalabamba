from django.db import models
from django.core.validators import URLValidator

# ──────────────────────────────────────────────────────────────────────────────
# 0) Página (singleton)
# ──────────────────────────────────────────────────────────────────────────────
class NosotrosPage(models.Model):
    # Solo 1 registro
    enabled = models.BooleanField(default=True)

    # Relación 1-1 a secciones
    header = models.OneToOneField("InnerHeader", on_delete=models.SET_NULL, null=True, blank=True)
    about  = models.OneToOneField("AboutSection", on_delete=models.SET_NULL, null=True, blank=True)
    history = models.OneToOneField("HistorySection", on_delete=models.SET_NULL, null=True, blank=True)
    ecoaldea = models.OneToOneField("EcoAldeaSection", on_delete=models.SET_NULL, null=True, blank=True)
    # testimonios: a futuro

    class Meta:
        verbose_name = "Página: Nosotros"
        verbose_name_plural = "Página: Nosotros"

    def __str__(self):
        return "Página Nosotros"


# ──────────────────────────────────────────────────────────────────────────────
# 1) Inner Header
# ──────────────────────────────────────────────────────────────────────────────
class InnerHeader(models.Model):
    title = models.CharField("Título", max_length=120, default="Nosotros")
    breadcrumb_label = models.CharField("Breadcrumb actual", max_length=120, default="Nuestro camino")
    background = models.ImageField(upload_to="nosotros/", help_text="Imagen de fondo del header")

    class Meta:
        verbose_name = "Sección: Header"
        verbose_name_plural = "Sección: Header"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# 2) About + Video
# ──────────────────────────────────────────────────────────────────────────────
class AboutSection(models.Model):
    title = models.CharField(max_length=160, default="Chambalabamba, ecoaldea viva")
    lead  = models.TextField("Intro (negrita)", blank=True)
    body  = models.TextField("Párrafo", blank=True)
    cta_text = models.CharField("Texto botón", max_length=80, blank=True, default="Contact Us")
    cta_url  = models.CharField("URL botón", max_length=300, blank=True)
    video_url = models.CharField("URL de video (Vimeo/YouTube)", max_length=500, validators=[URLValidator()], blank=True)

    class Meta:
        verbose_name = "Sección: About + Video"
        verbose_name_plural = "Sección: About + Video"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# 3) Historia (imagen lateral + timeline)
# ──────────────────────────────────────────────────────────────────────────────
class HistorySection(models.Model):
    subtitle = models.CharField("Subtítulo", max_length=120, default="About our History")
    title = models.CharField("Título", max_length=120, default="Our Success Story")
    side_image = models.ImageField(upload_to="nosotros/", blank=True, null=True)

    class Meta:
        verbose_name = "Sección: Historia"
        verbose_name_plural = "Sección: Historia"

    def __str__(self):
        return self.title


class TimelinePeriod(models.Model):
    history = models.ForeignKey(HistorySection, on_delete=models.CASCADE, related_name="periods")
    label = models.CharField("Rango de años", max_length=60)  # ej: "2000 - 2002"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Periodo (Timeline)"
        verbose_name_plural = "Periodos (Timeline)"

    def __str__(self):
        return self.label


class TimelineItem(models.Model):
    period = models.ForeignKey(TimelinePeriod, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=120)
    body  = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Caja de Timeline"
        verbose_name_plural = "Cajas de Timeline"

    def __str__(self):
        return f"{self.period.label} · {self.title}"


# ──────────────────────────────────────────────────────────────────────────────
# 4) EcoAldea (3 tarjetas)
# ──────────────────────────────────────────────────────────────────────────────
class EcoAldeaSection(models.Model):
    title = models.CharField(max_length=160, default="Sé parte de la Eco Aldea")

    class Meta:
        verbose_name = "Sección: EcoAldea"
        verbose_name_plural = "Sección: EcoAldea"

    def __str__(self):
        return self.title


class EcoAldeaCard(models.Model):
    section = models.ForeignKey(EcoAldeaSection, on_delete=models.CASCADE, related_name="cards")
    icon = models.ImageField(upload_to="nosotros/", help_text="Icono 60px aprox.")
    title = models.CharField(max_length=120)
    text  = models.TextField()
    link_text = models.CharField(max_length=120, blank=True)
    link_url  = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Tarjeta EcoAldea"
        verbose_name_plural = "Tarjetas EcoAldea"

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
