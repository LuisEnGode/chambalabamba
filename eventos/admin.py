from django.contrib import admin
from .models import Festival, Taller

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'place')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'place', 'flyer')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'schedule', 'place', 'image', 'flyer')
        }),
    )
