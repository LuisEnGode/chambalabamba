from django.contrib import admin
from .models import (
    NosotrosPage, InnerHeader, AboutSection,
    HistorySection, TimelinePeriod, TimelineItem,
    EcoAldeaSection, EcoAldeaCard
)

@admin.register(NosotrosPage)
class NosotrosPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "about", "history", "ecoaldea")
    def has_add_permission(self, request):
        return not NosotrosPage.objects.exists()

@admin.register(InnerHeader)
class InnerHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text", "video_url")

class TimelineItemInline(admin.TabularInline):
    model = TimelineItem
    extra = 1

# --- ADMIN OCULTO: registrado pero no aparece en el índice ---
class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        # Al devolver {} el modelo no se muestra en la página de apps,
        # pero sigue teniendo URLs y vistas para add/change/delete.
        return {}

@admin.register(TimelinePeriod)
class TimelinePeriodAdmin(HiddenModelAdmin):
    inlines = [TimelineItemInline]
    list_display = ("label", "history", "order")
    list_filter = ("history",)
    ordering = ("history", "order")

# Inline dentro de HistorySection con link a "Change"
class TimelinePeriodInline(admin.StackedInline):
    model = TimelinePeriod
    extra = 0
    show_change_link = True

@admin.register(HistorySection)
class HistorySectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    inlines = [TimelinePeriodInline]

class EcoAldeaCardInline(admin.TabularInline):
    model = EcoAldeaCard
    extra = 0

@admin.register(EcoAldeaSection)
class EcoAldeaSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EcoAldeaCardInline]
