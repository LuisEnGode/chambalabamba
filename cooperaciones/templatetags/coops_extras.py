from django import template
from cooperaciones.models import Cooperacion, CoopCategoria

register = template.Library()

def _coops_por_categoria(cat_slug: str, limit=None):
    qs = (Cooperacion.objects
          .filter(publicado=True, categoria__slug=cat_slug)
          .select_related("categoria")
          .order_by("orden", "-creado"))
    try:
        limit = int(limit or 0)
        if limit > 0: qs = qs[:limit]
    except (TypeError, ValueError):
        pass
    return qs

@register.inclusion_tag("cooperaciones/_coops_tabs.html")
def coops_tabs(
    header_h5="Alianzas que nos potencian",
    header_h2="Cooperaciones",
    categorias="",   # CSV "slug:Nombre,slug2:Nombre2"; si vacío = TODAS las categorías con coops
    limit=8,
    link_to_list=True,            # convierte el h5 en link a /cooperaciones/
    show_cta_button=False,
    cta_label="Ver todas"
):
    tabs = []
    if categorias:
        for raw in str(categorias).split(","):
            raw = raw.strip()
            if not raw: continue
            key, title = (raw.split(":",1)+[raw])[:2] if ":" in raw else (raw, raw)
            key, title = key.strip(), title.strip()
            tabs.append({"id": key, "title": title, "items": _coops_por_categoria(key, limit)})
    else:
        cats = (CoopCategoria.objects
                .filter(publicado=True, coops__publicado=True)
                .order_by("orden", "nombre").distinct())
        for c in cats:
            tabs.append({"id": c.slug, "title": c.nombre, "items": _coops_por_categoria(c.slug, limit)})

    return {
        "header_h5": header_h5, "header_h2": header_h2, "tabs": tabs,
        "link_to_list": link_to_list, "show_cta_button": show_cta_button, "cta_label": cta_label
    }
