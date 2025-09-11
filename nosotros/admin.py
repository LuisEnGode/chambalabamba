from django.contrib import admin
from django.utils.html import format_html
from .models import (
    # ——— “Nosotros / Nuestro Camino” ———
    NosotrosPage, InnerHeader, AboutSection,
    HistorySection, TimelinePeriod, TimelineItem,
    EcoAldeaSection, EcoAldeaCard,

    # ——— “PILARES” ———
    PageHeader, PilarPage, PilarParagraph, PilarQuote, PilarSidebarWidget,
)

# =========================
# N O S O T R O S
# =========================

@admin.register(NosotrosPage)
class NosotrosPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "about", "history", "ecoaldea")
    def has_add_permission(self, request):
        # singleton
        return not NosotrosPage.objects.exists()

@admin.register(InnerHeader)
class InnerHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")
    search_fields = ("title", "breadcrumb_label")

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text", "video_url")
    search_fields = ("title", "cta_text", "video_url")

class TimelineItemInline(admin.TabularInline):
    model = TimelineItem
    extra = 1
    fields = ("order", "title", "body")
    ordering = ("order",)

class HiddenModelAdmin(admin.ModelAdmin):
    # No aparece en el índice, pero sigue accesible
    def get_model_perms(self, request):
        return {}

@admin.register(TimelinePeriod)
class TimelinePeriodAdmin(HiddenModelAdmin):
    inlines = [TimelineItemInline]
    list_display = ("label", "history", "order")
    list_filter = ("history",)
    ordering = ("history", "order")
    search_fields = ("label",)

class TimelinePeriodInline(admin.StackedInline):
    model = TimelinePeriod
    extra = 0
    show_change_link = True

@admin.register(HistorySection)
class HistorySectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    inlines = [TimelinePeriodInline]
    search_fields = ("title", "subtitle")

class EcoAldeaCardInline(admin.TabularInline):
    model = EcoAldeaCard
    extra = 0
    fields = ("order", "icon", "title", "text", "link_text", "link_url")
    ordering = ("order",)

@admin.register(EcoAldeaSection)
class EcoAldeaSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EcoAldeaCardInline]
    search_fields = ("title",)


# =========================
# P I L A R E S
# =========================

class PilarParagraphInline(admin.TabularInline):
    model = PilarParagraph
    extra = 0
    fields = ("orden", "publicado", "body")
    ordering = ("orden",)  # usa ("orden", "-creado") si el modelo tiene 'creado'

class PilarQuoteInline(admin.TabularInline):
    model = PilarQuote
    extra = 0
    fields = ("orden", "publicado", "text")
    ordering = ("orden",)  # idem

class PilarSidebarInline(admin.TabularInline):
    model = PilarSidebarWidget
    extra = 0
    fields = ("orden", "publicado", "title", "text")
    ordering = ("orden",)  # idem

@admin.register(PageHeader)
class PageHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")
    search_fields = ("title", "breadcrumb_label")

@admin.register(PilarPage)
class PilarPageAdmin(admin.ModelAdmin):
    list_display = ("slug", "title",)
    list_filter = ("slug",)
    search_fields = ("title",)
    inlines = [PilarParagraphInline, PilarQuoteInline, PilarSidebarInline]
    save_on_top = True
    list_per_page = 20
