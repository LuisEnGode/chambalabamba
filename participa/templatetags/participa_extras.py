# participa/templatetags/participa_extras.py
from django import template

register = template.Library()

# --------- Imports tolerantes ---------
try:
    # si existen en tu app participa
    from participa.models import Estancia, InstaGallery, ProyectoVoluntariado, VoluntariadoPage
except Exception:
    Estancia = InstaGallery = ProyectoVoluntariado = VoluntariadoPage = None

try:
    # tu app real de cooperaciones
    from cooperaciones.models import Cooperacion
except Exception:
    Cooperacion = None


# ====== ESTANCIAS (si las usas) ======
@register.inclusion_tag("participa/_gallery_headers_estancias.html")
def gallery_headers_estancias(seccion="participa_estancias", title=None, subtitle=None, limit=None, only_with_portada=True):
    if Estancia is None:
        return {"estancias": [], "title": title, "subtitle": subtitle}
    qs = Estancia.objects.filter(publicado=True).order_by("orden", "-creado")
    if hasattr(Estancia, "seccion") and seccion:
        qs = qs.filter(seccion=seccion)
    if only_with_portada:
        qs = qs.exclude(portada="").exclude(portada__isnull=True)
    if limit:
        try:
            qs = qs[: int(limit)]
        except (TypeError, ValueError):
            pass
    return {"estancias": qs, "title": title, "subtitle": subtitle}


# ====== INSTAGRAM GRID (si lo usas) ======
@register.inclusion_tag("participa/_insta_grid.html")
def participa_instagram(slug=None):
    if InstaGallery is None:
        return {"insta": None}
    if slug:
        gal = InstaGallery.objects.filter(publicado=True, seccion="participa_instagram", titulo=slug).first()
    else:
        gal = InstaGallery.objects.filter(publicado=True, seccion="participa_instagram").first()
    return {"insta": gal}


# ====== COOPERACIONES (ÚNICA definición, con seccion) ======
@register.inclusion_tag("participa/_cooperaciones.html", takes_context=False, name="participa_cooperaciones")
def participa_cooperaciones(title=None, subtitle=None, limit=None, seccion=None, order="orden,-creado"):
    """
    Uso:
      {% participa_cooperaciones title="Cooperaciones" subtitle="Alianzas que nos potencian" limit=12 seccion="voluntariado" %}
    """
    qs = []
    if Cooperacion is not None:
        qs = Cooperacion.objects.all()
        # publicado=True si existe
        try:
            qs = qs.filter(publicado=True)
        except Exception:
            pass

        # filtro por seccion/categoria/tags si el modelo lo soporta
        if seccion:
            for candidate in (
                {"seccion": seccion},
                {"seccion__slug": seccion},
                {"categoria__slug": seccion},
                {"categoria__nombre__iexact": seccion},
                {"tags__name__iexact": seccion},
            ):
                try:
                    qs = qs.filter(**candidate)
                    break
                except Exception:
                    continue

        # orden tolerante
        try:
            fields = [f.strip() for f in (order or "").split(",") if f.strip()]
            if fields:
                qs = qs.order_by(*fields)
        except Exception:
            pass

        # límite
        try:
            if limit:
                qs = qs[: int(limit)]
        except Exception:
            pass

    return {"title": title, "subtitle": subtitle, "cooperaciones": qs}


# ====== SIDEBAR PROYECTOS VOLUNTARIADO ======
@register.inclusion_tag("participa/_sidebar_proyectos_voluntariado.html")
def voluntariado_sidebar_projects(limit=10):
    if ProyectoVoluntariado is None:
        return {"proyectos": []}
    qs = ProyectoVoluntariado.objects.filter(publicado=True).order_by("orden", "nombre")[: int(limit)]
    return {"proyectos": qs}


# ====== SINGLETON PAGE ======
@register.simple_tag
def voluntariado_page():
    """Acceso directo al singleton en plantillas: {% voluntariado_page as vp %}"""
    if VoluntariadoPage is None:
        return None
    return VoluntariadoPage.get_solo()
