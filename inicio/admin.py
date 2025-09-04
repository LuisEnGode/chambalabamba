from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import HeroSlide, ValorCard, ProyectoCard, ProductoItem, InstaFoto

class BaseOrdenPublicadoAdmin(admin.ModelAdmin):
    list_editable = ("publicado", "orden")
    list_filter = ("publicado",)
    ordering = ("orden",)
    search_fields = ("titulo",)

@admin.register(HeroSlide)
class HeroSlideAdmin(BaseOrdenPublicadoAdmin):
    list_display = ("mini", "titulo", "subtitulo", "publicado", "orden", "creado")
    def mini(self, obj):
        return format_html('<img src="{}" style="height:40px;border-radius:6px">', obj.imagen.url) if obj.imagen else "—"

@admin.register(ValorCard)
class ValorCardAdmin(BaseOrdenPublicadoAdmin):
    list_display = ("mini", "titulo", "descripcion", "publicado", "orden", "creado")
    def mini(self, obj):
        return format_html('<img src="{}" style="height:28px">', obj.icono.url) if obj.icono else "—"

@admin.register(ProyectoCard)
class ProyectoCardAdmin(BaseOrdenPublicadoAdmin):
    list_display = ("mini", "titulo", "etiqueta", "url", "publicado", "orden", "creado")
    def mini(self, obj):
        return format_html('<img src="{}" style="height:40px;border-radius:6px">', obj.imagen.url) if obj.imagen else "—"

@admin.register(ProductoItem)
class ProductoItemAdmin(BaseOrdenPublicadoAdmin):
    list_display = ("mini", "titulo", "precio", "precio_tachado", "publicado", "orden")
    def mini(self, obj):
        return format_html('<img src="{}" style="height:36px">', obj.imagen.url) if obj.imagen else "—"

@admin.register(InstaFoto)
class InstaFotoAdmin(BaseOrdenPublicadoAdmin):
    list_display = ("mini", "alt", "enlace", "publicado", "orden")
    def mini(self, obj):
        return format_html('<img src="{}" style="height:32px">', obj.imagen.url) if obj.imagen else "—"
