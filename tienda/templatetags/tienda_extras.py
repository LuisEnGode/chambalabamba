# tienda/templatetags/tienda_extras.py
from django import template
from django.db.models import Q
from tienda.models import Producto, ProductoCategoria

register = template.Library()

def productos_por_categoria(cat_key: str, limit=None):
    """Devuelve productos publicados por slug/nombre de categoría."""
    cat_key = (cat_key or "").strip()
    if not cat_key:
        return Producto.objects.none()

    qs = (
        Producto.objects.filter(publicado=True)
        .filter(
            Q(categoria__slug=cat_key) |
            Q(categoria__slug__iexact=cat_key) |
            Q(categoria__nombre__iexact=cat_key)
        )
        .select_related("categoria")
        .order_by("orden", "-creado")
    )

    # Prefetch seguro (si no tienes related_name='imagenes', usa el set por defecto)
    try:
        Producto._meta.get_field("imagenes")
        qs = qs.prefetch_related("imagenes")
    except Exception:
        qs = qs.prefetch_related("productoimagen_set")

    if limit:
        try:
            limit = int(limit)
            if limit > 0:
                qs = qs[:limit]
        except (TypeError, ValueError):
            pass
    return qs

@register.inclusion_tag("tienda/_products_tabs.html")
def products_tabs(
    header_h5="Visita nuestra tienda",
    header_h2="Productos",
    categorias="",   # CSV "slug:Nombre,slug2:Nombre2"; si vacío = todas las categorías con productos
    limit=8          # productos por categoría
):
    tabs = []

    if categorias:
        # modo explícito
        for raw in str(categorias).split(","):
            raw = raw.strip()
            if not raw:
                continue
            if ":" in raw:
                key, title = raw.split(":", 1)
            else:
                key, title = raw, raw
            key, title = key.strip(), title.strip()
            items = productos_por_categoria(key, limit)
            tabs.append({"id": key, "title": title, "items": items})
    else:
        # todas las categorías con al menos 1 producto publicado
        cats = (
            ProductoCategoria.objects
            .filter(publicado=True, productos__publicado=True)
            .order_by("orden", "nombre")
            .distinct()
        )
        for c in cats:
            tabs.append({
                "id": c.slug,
                "title": c.nombre,
                "items": productos_por_categoria(c.slug, limit),
            })

    return {"header_h5": header_h5, "header_h2": header_h2, "tabs": tabs}
