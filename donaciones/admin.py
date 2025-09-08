# apps/donaciones/admin.py
from django.contrib import admin
from .models import DonacionSection, DonacionMonto

class DonacionMontoInline(admin.TabularInline):
    model = DonacionMonto
    extra = 0
    fields = ("etiqueta", "orden")
    ordering = ("orden",)

@admin.register(DonacionSection)
class DonacionSectionAdmin(admin.ModelAdmin):
    list_display = ("slug", "titulo_superior", "titulo", "publicado", "orden", "progreso")
    list_editable = ("publicado", "orden", "progreso")
    search_fields = ("slug", "titulo", "descripcion")
    inlines = [DonacionMontoInline]
from django.contrib import admin

# Register your models here.
