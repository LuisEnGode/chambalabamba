from django import template
from participa.models import Estancia

register = template.Library()

@register.inclusion_tag("participa/_gallery_headers_estancias.html")
def gallery_headers_estancias(seccion="participa_estancias", title=None, subtitle=None, limit=None):
    qs = (Estancia.objects
          .filter(seccion=seccion, publicado=True)
          .exclude(portada="")                 # solo con imagen
          .order_by("orden", "-creado"))
    if limit:
        try:
            qs = qs[:int(limit)]
        except (TypeError, ValueError):
            pass
    return {"estancias": qs, "title": title, "subtitle": subtitle}