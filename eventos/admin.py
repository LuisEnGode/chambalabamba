from django.contrib import admin
from .models import (
    Festival, TallerDetail, TalleresPage, TalleresHeader, TalleresIntroSection,
    FestivalesPage, FestivalesHeader, FestivalesIntroSection
)

@admin.register(FestivalesPage)
class FestivalesPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "intro")
    def has_add_permission(self, request):
        return not FestivalesPage.objects.exists()

@admin.register(FestivalesHeader)
class FestivalesHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")

@admin.register(FestivalesIntroSection)
class FestivalesIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text")

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'place')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'date', 'time', 'place', 'image', 'flyer')
        }),
    )

@admin.register(TalleresPage)
class TalleresPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "intro")
    def has_add_permission(self, request):
        return not TalleresPage.objects.exists()

@admin.register(TalleresHeader)
class TalleresHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")

@admin.register(TalleresIntroSection)
class TalleresIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text")

@admin.register(TallerDetail)
class TallerDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'place', 'flyer')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'schedule', 'place', 'image', 'flyer')
        }),
    )
