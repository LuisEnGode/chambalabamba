from django import template
from inicio.models import Gallery

register = template.Library()

@register.inclusion_tag("inicio/_gallery_headers_component.html")
def gallery_headers(seccion, title=None, subtitle=None, limit=None):
    qs = (Gallery.objects
          .filter(seccion=seccion, publicado=True)
          .exclude(portada="")            # evita las que no tienen imagen
          .order_by("orden", "-creado"))
    if limit:
        try:
            qs = qs[:int(limit)]
        except (TypeError, ValueError):
            pass
    return {"galerias": qs, "title": title, "subtitle": subtitle}
