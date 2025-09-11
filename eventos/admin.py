from django.contrib import admin
from .models import (
    Festival, TallerDetail, TalleresPage, TalleresHeader, TalleresIntroSection,
    FestivalesPage, FestivalesHeader, FestivalesIntroSection,
    ArtesPage, ArtesHeader, ArtesIntroSection, ArtesDiversitySection, Arte,
    ArtesGallerySection, ArtesGalleryImage
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

class ArteInline(admin.TabularInline):
    model = Arte
    extra = 1

class ArtesGalleryImageInline(admin.TabularInline):
    model = ArtesGalleryImage
    extra = 1

@admin.register(ArtesPage)
class ArtesPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "intro", "diversity", "gallery")
    def has_add_permission(self, request):
        return not ArtesPage.objects.exists()

@admin.register(ArtesHeader)
class ArtesHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")

@admin.register(ArtesIntroSection)
class ArtesIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("subtitle", "sidebar_title")

@admin.register(ArtesDiversitySection)
class ArtesDiversitySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [ArteInline]

@admin.register(ArtesGallerySection)
class ArtesGallerySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [ArtesGalleryImageInline]
