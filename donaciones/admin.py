# apps/donaciones/admin.py
from django.contrib import admin
from .models import DonacionSection, DonacionMonto, Donacion

class DonacionMontoInline(admin.TabularInline):
    model = DonacionMonto
    extra = 0
    fields = ("etiqueta", "orden")
    ordering = ("orden",)

@admin.register(DonacionSection)
class DonacionSectionAdmin(admin.ModelAdmin):
    list_display = ("slug", "titulo_superior", "titulo", "publicado", "orden", "progreso")
    list_editable = ("publicado", "orden", "progreso")
    # Updated search_fields to include new text-based fields
    search_fields = ("slug", "titulo", "descripcion", "intro_text", "success_title", "success_message", "canceled_title", "canceled_message", "paypal_redirect_message")
    # Added new fields to the fields tuple
    fields = (
        "slug", "titulo_superior", "titulo", "descripcion", "progreso",
        "cta_titulo", "cta_boton_texto", "cta_placeholder_otro",
        "intro_text", "donation_image", "success_title", "success_message",
        "canceled_title", "canceled_message", "paypal_redirect_message",
        "publicado", "orden"
    )
    inlines = [DonacionMontoInline]

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "monto", "creado_en", "completado")
    list_filter = ("completado",)
    search_fields = ("nombre", "email", "paypal_id")
