# apps/contenido/templatetags/contenido_extras.py
from django import template
from contenido.models import Placement

register = template.Library()

@register.simple_tag
def get_placement(key):
    try:
        return Placement.objects.select_related("flyer", "gallery").get(key=key, activo=True)
    except Placement.DoesNotExist:
        return None
