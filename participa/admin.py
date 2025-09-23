# participa/admin.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import (VoluntariadoPage,
                     ContentBlock,               # ya lo usas en Voluntariado
                    GuidedVisitsPage,           # singleton de la sección
                    )

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not self.model.objects.exists()
    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj: return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)

@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("title", "publicado", "orden", "actualizado")
    list_editable = ("publicado", "orden")
    search_fields = ("title", "body_html")  # <-- necesario para autocomplete

@admin.register(VoluntariadoPage)
class VoluntariadoPageAdmin(SingletonAdmin):
    # ← Esto reemplaza a raw_id_fields
    autocomplete_fields = ("about_block", "ambiente_block")

    # Links de edición directa (ver punto 2)
    readonly_fields = ("edit_about_link", "edit_ambiente_link")

    fieldsets = (
        ("Estado", {"fields": ("publicado",)}),
        ("Cabecera", {"fields": ("titulo", "subtitulo", "background", "thumb")}),
        ("Bloques", {
            "fields": (
                "about_block", "edit_about_link",
                "ambiente_block", "edit_ambiente_link",
            )
        }),
        ("Texto de introducción (fallback)", {"fields": ("intro_html",)}),
        ("Quote", {"fields": ("quote_text", "quote_author")}),
        ("Instagram", {"fields": ("instagram_embed_url",)}),
        ("Contacto", {"fields": ("contact_cta_label", "contact_cta_url")}),
    )

    list_display = ("titulo", "subtitulo", "publicado", "actualizado")
    search_fields = ("titulo", "subtitulo", "quote_text")

    # ---------------- helpers de enlace directo ----------------
    def edit_about_link(self, obj):
        if obj and obj.about_block_id:
            url = reverse("admin:participa_contentblock_change", args=[obj.about_block_id])
            return format_html('<a class="button" href="{}" target="_blank">Editar “{}”</a>', url, obj.about_block)
        return "—"
    edit_about_link.short_description = "Editar About"

    def edit_ambiente_link(self, obj):
        if obj and obj.ambiente_block_id:
            url = reverse("admin:participa_contentblock_change", args=[obj.ambiente_block_id])
            return format_html('<a class="button" href="{}" target="_blank">Editar “{}”</a>', url, obj.ambiente_block)
        return "—"
    edit_ambiente_link.short_description = "Editar Ambiente"



