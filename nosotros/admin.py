from django.contrib import admin
from .models import (
    NosotrosPage, InnerHeader, AboutSection,
    HistorySection, TimelinePeriod, TimelineItem,
    EcoAldeaSection, EcoAldeaCard
)

@admin.register(NosotrosPage)
class NosotrosPageAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "header", "about", "history", "ecoaldea")
    # opcional: impedir más de 1
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

@admin.register(TimelinePeriod)
class TimelinePeriodAdmin(admin.ModelAdmin):
    inlines = [TimelineItemInline]
    list_display = ("label", "history", "order")
    list_filter = ("history",)
    ordering = ("history", "order")

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
from django.contrib import admin

# Register your models here.
