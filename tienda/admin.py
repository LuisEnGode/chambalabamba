from django.contrib import admin
from django.utils.html import format_html
from .models import ProductoCategoria, Producto, ProductoImagen

@admin.register(ProductoCategoria)
class ProductoCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "publicado", "orden")
    list_editable = ("publicado", "orden")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 0
    fields = ("publicado", "orden", "imagen", "alt")
    ordering = ("orden",)
    show_change_link = True


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("mini", "titulo", "categoria", "precio", "precio_tachado", "publicado", "orden", "creado")
    list_editable = ("publicado", "orden")
    list_filter = ("publicado", "categoria")
    search_fields = ("titulo", "descripcion", "descripcion_corta", "slug")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [ProductoImagenInline]

    def mini(self, obj):
        if obj.imagen_portada:
            return format_html('<img src="{}" style="height:40px;border-radius:6px">', obj.imagen_portada.url)
        return "—"


# (Opcional) Registrar el admin oculto para acceder a /change/ directo sin mostrarlo en el índice:
class _Hidden(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
@admin.register(ProductoImagen)
class ProductoImagenAdmin(_Hidden):
    list_display = ("producto", "orden", "publicado")
