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


@admin.register(PilarPage)
class PilarPageAdmin(admin.ModelAdmin):
    list_display = ("slug", "title",)
    list_filter = ("slug",)
    search_fields = ("title",)
    inlines = [PilarParagraphInline, PilarQuoteInline, PilarSidebarInline]
    save_on_top = True
    list_per_page = 20

# ──────────────────────────────────────────────────────────────────────────────
# NOSOTROS: Secciones (Gobernanza, Principios y valores, Territorio)
# ──────────────────────────────────────────────────────────────────────────────


from .models import (
    TopicPage, TopicParagraph, TopicQuote, TopicSidebarWidget,
)

class TopicParagraphInline(admin.TabularInline):
    model = TopicParagraph
    extra = 0
    fields = ("orden", "publicado", "body")
    ordering = ("orden",)

class TopicQuoteInline(admin.TabularInline):
    model = TopicQuote
    extra = 0
    fields = ("orden", "publicado", "text")
    ordering = ("orden",)

class TopicSidebarInline(admin.TabularInline):
    model = TopicSidebarWidget
    extra = 0
    fields = ("orden", "publicado", "title", "text")
    ordering = ("orden",)

@admin.register(TopicPage)
class TopicPageAdmin(admin.ModelAdmin):
    list_display = ("slug", "title")
    list_filter = ("slug",)
    search_fields = ("title",)
    inlines = [TopicParagraphInline, TopicQuoteInline, TopicSidebarInline]
    save_on_top = True



# nosotros/admin.py
from django.contrib import admin
from .models import (
    TopicPage, GobernanzaPage, PrincipiosValoresPage, TerritorioPage,
    TopicParagraph, TopicQuote, TopicSidebarWidget
)

class ParagraphInline(admin.StackedInline):
    model = TopicParagraph
    extra = 0

class QuoteInline(admin.StackedInline):
    model = TopicQuote
    extra = 0

class SidebarInline(admin.StackedInline):
    model = TopicSidebarWidget
    extra = 0

class _BaseTopicAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline, QuoteInline, SidebarInline]
    fields = ("title", "header", "slug")  # o los campos que edites
    readonly_fields = ("slug",)           # fijamos slug

    # Evita que creen más de 1 registro por proxy
    def has_add_permission(self, request):
        return self.get_queryset(request).count() == 0

    # Oculta cualquier otro registro que no sea el de este slug
    filter_slug = None  # lo define cada subclase

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(slug=self.filter_slug)

    # Si quisieras autocrear el registro al entrar por 1a vez:
    def changelist_view(self, request, extra_context=None):
        if self.model.objects.filter(slug=self.filter_slug).count() == 0:
            self.model.objects.create(slug=self.filter_slug, title=self.model._meta.verbose_name.split(". ",1)[1])
        return super().changelist_view(request, extra_context)

@admin.register(GobernanzaPage)
class GobernanzaAdmin(_BaseTopicAdmin):
    filter_slug = "gobernanza"

@admin.register(PrincipiosValoresPage)
class PrincipiosValoresAdmin(_BaseTopicAdmin):
    filter_slug = "principios-y-valores"

@admin.register(TerritorioPage)
class TerritorioAdmin(_BaseTopicAdmin):
    filter_slug = "territorio"


from django.contrib import admin
from .models import TopicPage

# Oculta el modelo base del índice del admin
try:
    admin.site.unregister(TopicPage)
except admin.sites.NotRegistered:
    pass