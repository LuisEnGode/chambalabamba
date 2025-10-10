from django import template
from contenido.models import FooterSettings, FooterMenu

register = template.Library()

@register.inclusion_tag("partials/sub_footer_info.html")  # ← sin takes_context
def render_footer():
    about = FooterSettings.objects.first()
    menus = FooterMenu.objects.prefetch_related("links").all()
    return {"about": about, "menus": menus}      # ← NO mezcles context
