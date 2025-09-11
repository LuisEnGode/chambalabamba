from django.contrib import admin
from .models import (
    Festival, TallerDetail, TalleresPage, TalleresHeader, TalleresIntroSection,
    FestivalesPage, FestivalesHeader, FestivalesIntroSection,
    ArtesPage, ArtesHeader, ArtesIntroSection, ArtesDiversitySection, Arte,
    ArtesGallerySection, ArtesGalleryImage,
    EscuelaPage, EscuelaHeader, EscuelaIntroSection, EscuelaGalleryImage,
    EscuelaSidebar, EscuelaProject,
    RetirosPage, RetirosHeader, RetirosIntroSection, RetirosTypesSection, RetiroType,
    RetirosActivitiesSection, RetiroActivity, RetirosGallerySection, RetirosGalleryImage,
    RetirosTestimonialSection, RetiroTestimonial
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

class EscuelaGalleryImageInline(admin.TabularInline):
    model = EscuelaGalleryImage
    extra = 1

class EscuelaProjectInline(admin.TabularInline):
    model = EscuelaProject
    extra = 1

@admin.register(EscuelaPage)
class EscuelaPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "intro", "sidebar")
    def has_add_permission(self, request):
        return not EscuelaPage.objects.exists()

@admin.register(EscuelaHeader)
class EscuelaHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")

@admin.register(EscuelaIntroSection)
class EscuelaIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EscuelaGalleryImageInline]

@admin.register(EscuelaSidebar)
class EscuelaSidebarAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EscuelaProjectInline]

class RetiroTypeInline(admin.TabularInline):
    model = RetiroType
    extra = 1

class RetiroActivityInline(admin.TabularInline):
    model = RetiroActivity
    extra = 1

class RetirosGalleryImageInline(admin.TabularInline):
    model = RetirosGalleryImage
    extra = 1

class RetiroTestimonialInline(admin.TabularInline):
    model = RetiroTestimonial
    extra = 1

@admin.register(RetirosPage)
class RetirosPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "intro", "types_section", "activities_section", "gallery_section", "testimonial_section")
    def has_add_permission(self, request):
        return not RetirosPage.objects.exists()

@admin.register(RetirosHeader)
class RetirosHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")

@admin.register(RetirosIntroSection)
class RetirosIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "sidebar_title")

@admin.register(RetirosTypesSection)
class RetirosTypesSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetiroTypeInline]

@admin.register(RetirosActivitiesSection)
class RetirosActivitiesSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetiroActivityInline]

@admin.register(RetirosGallerySection)
class RetirosGallerySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetirosGalleryImageInline]

@admin.register(RetirosTestimonialSection)
class RetirosTestimonialSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetiroTestimonialInline]
