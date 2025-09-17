from django.contrib import admin
from django.shortcuts import redirect
from .models import (
    Estancia, EstanciaFoto, EstanciaSpec,
    ParticipaHeader, ParticipaPage,
    VoluntariadoPage, ProyectoVoluntariado
)

# --- Inlines existentes para Estancia (si ya los tienes, conserva) ---
class EstanciaFotoInline(admin.TabularInline):
    model = EstanciaFoto
    extra = 1
    fields = ("publicado","orden","titulo","imagen","alt")
    ordering = ("orden",)

class EstanciaSpecInline(admin.TabularInline):
    model = EstanciaSpec
    extra = 3
    fields = ("orden","clave","valor")
    ordering = ("orden",)

@admin.register(Estancia)
class EstanciaAdmin(admin.ModelAdmin):
    list_display = ("titulo","seccion","tipo","lugar","publicado","orden","creado")
    list_filter = ("seccion","publicado")
    search_fields = ("titulo","resumen","descripcion","tipo","lugar","slug")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [EstanciaFotoInline, EstanciaSpecInline]

# --- Patrón singleton para Header y Página ---
class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()
    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)

@admin.register(ParticipaHeader)
class ParticipaHeaderAdmin(SingletonAdmin):
    list_display = ("title","breadcrumb_label")

@admin.register(ParticipaPage)
class ParticipaPageAdmin(SingletonAdmin):
    list_display = ("enabled","header")


# participa/admin.py
# participa/admin.py
from django.contrib import admin
from django.shortcuts import redirect
from .models import VoluntariadoPage, ProyectoVoluntariado, ContentBlock

# --- Patrón singleton reutilizable ---
class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Permite crear sólo si no existe ningún registro
        return not self.model.objects.exists()
    def changelist_view(self, request, extra_context=None):
        # Si existe el registro único, abre directo su pantalla de edición
        obj = self.model.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)

@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("title", "publicado", "orden", "actualizado")
    list_editable = ("publicado", "orden")
    search_fields = ("title", "body_html")

@admin.register(VoluntariadoPage)
class VoluntariadoPageAdmin(SingletonAdmin):
    fieldsets = (
        ("Estado", {"fields": ("publicado",)}),
        ("Cabecera", {"fields": ("titulo", "subtitulo", "background", "thumb")}),
        ("Bloques", {"fields": ("about_block", "ambiente_block")}),
        ("Texto de introducción (fallback)", {"fields": ("intro_html",)}),
        ("Quote", {"fields": ("quote_text", "quote_author")}),
        ("Instagram", {"fields": ("instagram_embed_url",)}),
        ("Contacto", {"fields": ("contact_cta_label", "contact_cta_url")}),
    )
    raw_id_fields = ("about_block", "ambiente_block")
    list_display = ("titulo", "subtitulo", "publicado", "actualizado")
    search_fields = ("titulo", "subtitulo", "quote_text")

@admin.register(ProyectoVoluntariado)
class ProyectoVoluntariadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden", "publicado")
    list_editable = ("orden", "publicado")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
