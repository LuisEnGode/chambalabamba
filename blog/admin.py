from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import BlogComment

from .models import (
    BlogPage, BlogHeader,
    BlogAuthor, BlogCategory, BlogTag,
    BlogPost, BlogPostPhoto,
    BlogSidebarWidget
)

# Helpers
class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not self.model.objects.exists()
    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)

# Inlines
class BlogPostPhotoInline(admin.TabularInline):
    model = BlogPostPhoto
    extra = 1
    fields = ("publicado", "orden", "imagen", "preview", "titulo", "alt", "creditos", "is_header")
    readonly_fields = ("preview",)
    ordering = ("orden", "id")
    def preview(self, obj):
        if getattr(obj, "imagen", None):
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.imagen.url)
        return "—"

class BlogSidebarWidgetInline(admin.StackedInline):
    model = BlogSidebarWidget
    extra = 0
    fields = (
        "publicado", "orden", "tipo", "titulo", "body_html", "limite",
        "proyectos", "link_label", "link_url"
    )
    autocomplete_fields = ("proyectos",)

# Página
@admin.register(BlogPage)
class BlogPageAdmin(SingletonAdmin):
    readonly_fields = ("header_preview", "edit_header_link")
    fieldsets = (
        ("Estado", {"fields": ("enabled",)}),
        ("Header", {"fields": ("header", "header_preview", "edit_header_link")}),
        ("Intro (opcional)", {"fields": ("intro_html",)}),
        ("CTAs", {"fields": ("volunteer_url", "donate_url")}),
    )
    inlines = [BlogSidebarWidgetInline]
    list_display = ("id", "enabled", "header")

    def header_preview(self, obj):
        hdr = obj.header
        if hdr and getattr(hdr, "background", None):
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', hdr.background.url)
        return "—"
    header_preview.short_description = "Preview fondo"

    def edit_header_link(self, obj):
        hdr = getattr(obj, "header", None)
        if hdr and hdr.pk:
            url = reverse(f"admin:{hdr._meta.app_label}_{hdr._meta.model_name}_change", args=[hdr.pk])
            return format_html('<a class="button" href="{}" target="_blank">Editar header</a>', url)
        return "—"

# Header oculto del menú
try:
    admin.site.register(BlogHeader, HiddenModelAdmin)
except admin.sites.AlreadyRegistered:
    pass

# Taxonomía
@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    fields = ("status", "nombre", "email", "cuerpo", "creado")
    readonly_fields = ("creado",)
    ordering = ("-creado",)

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("post", "nombre", "email", "status", "creado")
    list_filter = ("status", "creado", "post")
    search_fields = ("nombre", "email", "cuerpo", "post__titulo")
    ordering = ("-creado",)
    actions = ["aprobar", "rechazar", "marcar_spam"]

    def aprobar(self, request, queryset):
        queryset.update(status=BlogComment.Status.APPROVED)
    aprobar.short_description = "Aprobar seleccionados"

    def rechazar(self, request, queryset):
        queryset.update(status=BlogComment.Status.REJECTED)
    rechazar.short_description = "Rechazar seleccionados"

    def marcar_spam(self, request, queryset):
        queryset.update(status=BlogComment.Status.SPAM)
    marcar_spam.short_description = "Marcar como spam"

# Posts
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("orden", "titulo", "categoria", "autor", "publicado", "fecha_publicacion", "comentarios_count")
    list_display_links = ("titulo",)
    list_editable = ("orden", "publicado")
    list_filter = ("publicado", "categoria", "autor", "tipo")
    search_fields = ("titulo", "slug", "resumen", "cuerpo_html")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [BlogPostPhotoInline]
    date_hierarchy = "fecha_publicacion"
    ordering = ("-fecha_publicacion", "orden", "titulo")
    inlines = [BlogPostPhotoInline, BlogCommentInline]



