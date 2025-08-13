from django.contrib import admin
from blog.models import Post,Categoria

# Register your models here.
# Registro del modelo Categoria utilizando el decorador
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'created', 'updated')  # Muestra los campos en la lista
    search_fields = ('nombre',)  # Habilita la búsqueda por nombre de categoría
    list_filter = ('created',)  # Filtro por fecha de creación
    ordering = ('-created',)  # Ordena por la fecha de creación en orden descendente

# Registro del modelo Post utilizando el decorador
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('titulo', 'autor', 'created', 'updated')  # Muestra los campos en la lista
    search_fields = ('titulo', 'contenido')  # Habilita la búsqueda por título y contenido
    list_filter = ('categorias', 'created')  # Filtro por categoría y fecha de creación
    ordering = ('-created',)  # Ordena por la fecha de creación en orden descendente