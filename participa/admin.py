from django.contrib import admin
from django.shortcuts import redirect
from .models import (
    Estancia, EstanciaFoto, EstanciaSpec,
    ParticipaHeader, ParticipaPage
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
