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
        verbose_name = "1. Página: Nosotros / About Us Page"
        verbose_name_plural = "1. Página: Nosotros / About Us Page"

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
        verbose_name = "2. Sección: Cabecera / Header Section"
        verbose_name_plural = "2. Sección: Cabecera / Header Section"

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
        verbose_name = "3. Sección: Acerca + Video / About + Video"
        verbose_name_plural = "3. Sección: Acerca + Video / About + Video"

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
        verbose_name = "4. Sección: Historia / History Section"
        verbose_name_plural = "4. Sección: Historia / History Section"

    def __str__(self):
        return self.title


class TimelinePeriod(models.Model):
    history = models.ForeignKey(HistorySection, on_delete=models.CASCADE, related_name="periods")
    label = models.CharField("Rango de años", max_length=60)  # ej: "2000 - 2002"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Periodo (Timeline) / Timeline Period"
        verbose_name_plural = "Periodos (Timeline) / Timeline Periods"

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
        verbose_name = "5. Sección: EcoAldea / EcoVillage Section"
        verbose_name_plural = "5. Sección: EcoAldea / EcoVillage Section"

    def __str__(self):
        return self.title


class EcoAldeaCard(models.Model):
    section = models.ForeignKey(EcoAldeaSection, on_delete=models.CASCADE, related_name="cards")
    icon = models.ImageField(
        upload_to="nosotros/",
        help_text="Icono ~60px de alto",
        blank=True,
        null=True
    )
    title = models.CharField(max_length=120)
    text = models.TextField()
    link_text = models.CharField("Texto del enlace", max_length=120, blank=True)
    link_url = models.CharField("URL del enlace", max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Tarjeta EcoAldea / EcoVillage Card"
        verbose_name_plural = "Tarjeta EcoAldea / EcoVillage Card"

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
