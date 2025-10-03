from django import template
from cooperaciones.models import Cooperacion

register = template.Library()

@register.inclusion_tag("cooperaciones/_home_cooperaciones.html")
def _home_cooperaciones(subtitle="Alianzas que nos potencian",
                              title="Cooperaciones",
                              limit=12):
    coops = (Cooperacion.objects
             .filter(publicado=True)
             .only("slug","nombre","logo","portada","excerpt","orden","creado")
             .order_by("orden","-creado")[:int(limit)])
    return {"coops": coops, "subtitle": subtitle, "title": title}
