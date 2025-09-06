from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import HeroSlide, ValorCard, ProyectoCard, ProductoItem, InstaFoto
from .models import Gallery, GalleryItem

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


#GALERIA INICIAL ULTIMOS EVENTOS



class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1
    fields = ("publicado", "orden", "titulo", "imagen", "alt", "credito", "tags")
    ordering = ("orden",)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("titulo", "seccion", "publicado", "orden", "creado")
    list_filter = ("seccion", "publicado")
    search_fields = ("titulo", "descripcion", "slug")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [GalleryItemInline]

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "publicado", "orden", "creado")
    list_filter = ("publicado",)
    search_fields = ("titulo", "alt", "tags", "credito", "galeria__titulo")
    ordering = ("orden",)
