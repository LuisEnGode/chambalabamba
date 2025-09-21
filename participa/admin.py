# participa/admin.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import (VoluntariadoPage,
                     ContentBlock,               # ya lo usas en Voluntariado
                    GuidedVisitsPage,           # singleton de la sección
                    GuidedVisit,                # cada visita
                    GuidedVisitPhoto)           # fotos/galería por visita

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




# ---------- Página (singleton) “Visitas guiadas” ----------
@admin.register(GuidedVisitsPage)
class GuidedVisitsPageAdmin(SingletonAdmin):
    # editar/buscar bloques con (+) y ✎
    autocomplete_fields = ("about_block", "info_block")
    readonly_fields = ("edit_about_link", "edit_info_link")

    fieldsets = (
        ("Estado", {"fields": ("publicado",)}),
        ("Cabecera", {"fields": ("titulo", "subtitulo", "background", "thumb")}),
        ("Bloques", {"fields": ("about_block", "edit_about_link",
                                "info_block", "edit_info_link")}),
        ("Texto de introducción (fallback)", {"fields": ("intro_html",)}),
        ("Quote", {"fields": ("quote_text", "quote_author")}),
        ("Instagram", {"fields": ("instagram_embed_url",)}),
        ("Contacto", {"fields": ("contact_cta_label", "contact_cta_url")}),
    )
    list_display = ("titulo", "subtitulo", "publicado", "actualizado")
    search_fields = ("titulo", "subtitulo", "quote_text")

    # enlaces “Editar …” a los bloques
    def _edit_block_link(self, obj, fk_name, label):
        blk = getattr(obj, fk_name, None)
        if not blk: return "—"
        url = reverse("admin:participa_contentblock_change", args=[blk.pk])
        return format_html('<a class="button" target="_blank" href="{}">Editar “{}”</a>', url, blk)
    def edit_about_link(self, obj): return self._edit_block_link(obj, "about_block", "About")
    def edit_info_link(self, obj):  return self._edit_block_link(obj,  "info_block",  "Info")
    edit_about_link.short_description = "Editar About"
    edit_info_link.short_description  = "Editar Info"

# ---------- Inline de fotos por visita ----------
class GuidedVisitPhotoInline(admin.TabularInline):
    model = GuidedVisitPhoto
    extra = 1
    fields = ("publicado", "orden", "imagen", "preview", "titulo", "alt", "creditos", "is_header")
    readonly_fields = ("preview",)
    ordering = ("orden",)
    def preview(self, obj):
        if getattr(obj, "imagen", None):
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.imagen.url)
        return "—"
    preview.short_description = "Vista previa"

# ---------- Listado/edición de visitas ----------
@admin.register(GuidedVisit)
class GuidedVisitAdmin(admin.ModelAdmin):
    list_display = ("titulo", "breve", "orden", "publicado", "actualizado")
    list_editable = ("orden", "publicado")
    search_fields = ("titulo", "breve", "descripcion_html", "ubicacion", "organizador")
    list_filter = ("publicado",)
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [GuidedVisitPhotoInline]
    actions = ["publicar", "despublicar"]

    def publicar(self, request, queryset):
        queryset.update(publicado=True)
    publicar.short_description = "Marcar como publicados"

    def despublicar(self, request, queryset):
        queryset.update(publicado=False)
    despublicar.short_description = "Marcar como NO publicados"

# (Opcional) Registrar las fotos pero ocultarlas del menú
class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
admin.site.register(GuidedVisitPhoto, HiddenModelAdmin)

# (Asegúrate de que ContentBlock tenga search_fields para el autocomplete)
# @admin.register(ContentBlock) ... si ya está registrado, no lo dupliques.
# Debe tener: search_fields = ("title", "body_html")