from django.contrib import admin
from .models import Festival

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'place')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
