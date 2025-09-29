# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import BlogPage, BlogPost, BlogCategory, BlogTag, BlogAuthor
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import BlogCommentForm
from .models import BlogComment,BlogSidebarWidget
from django.db.models import Count, Q

COMMON_PREFETCH = ("tags", "fotos")
COMMON_SELECT   = ("autor", "categoria")

def _base_ctx():
    page = (BlogPage.objects
            .select_related("header")
            .prefetch_related("widgets")
            .first())

    # Widgets publicados y ordenados
    widgets = BlogSidebarWidget.objects.none()
    if page:
        widgets = page.widgets.filter(publicado=True).order_by("orden")

    # Archives & tags/cats con conteo de publicados
    archives = (BlogPost.objects.filter(publicado=True)
                .dates("fecha_publicacion", "month", order="DESC"))
    tags = (BlogTag.objects
            .annotate(n=Count("posts", filter=Q(posts__publicado=True), distinct=True))
            .order_by("nombre"))
    cats = (BlogCategory.objects
            .annotate(n=Count("posts", filter=Q(posts__publicado=True)))
            .order_by("nombre"))

    return {"page": page, "widgets": widgets, "archives": archives,
            "all_tags": tags, "all_categories": cats}

def blog_list(request):
    q = request.GET.get("q", "").strip()
    posts = (BlogPost.objects.filter(publicado=True)
             .select_related(*COMMON_SELECT).prefetch_related(*COMMON_PREFETCH)
             .order_by("-fecha_publicacion"))

    if q:
        posts = posts.filter(Q(titulo__icontains=q) | Q(resumen__icontains=q))

    ctx = {"posts": posts, "q": q}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_list.html", ctx)

def blog_list_by_category(request, slug):
    categoria = get_object_or_404(BlogCategory, slug=slug)
    posts = (BlogPost.objects.filter(publicado=True, categoria=categoria)
             .select_related(*COMMON_SELECT).prefetch_related(*COMMON_PREFETCH)
             .order_by("-fecha_publicacion"))
    ctx = {"posts": posts, "categoria": categoria}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_list.html", ctx)

def blog_list_by_tag(request, slug):
    tag = get_object_or_404(BlogTag, slug=slug)
    posts = (BlogPost.objects.filter(publicado=True, tags=tag)
             .select_related(*COMMON_SELECT).prefetch_related(*COMMON_PREFETCH)
             .order_by("-fecha_publicacion"))
    ctx = {"posts": posts, "tag": tag}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_list.html", ctx)

def blog_list_by_author(request, slug):
    autor = get_object_or_404(BlogAuthor, slug=slug)
    posts = (BlogPost.objects.filter(publicado=True, autor=autor)
             .select_related(*COMMON_SELECT).prefetch_related(*COMMON_PREFETCH)
             .order_by("-fecha_publicacion"))
    ctx = {"posts": posts, "autor": autor}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_list.html", ctx)

def blog_list_by_month(request, year, month):
    posts = (BlogPost.objects.filter(publicado=True,
                                     fecha_publicacion__year=year,
                                     fecha_publicacion__month=month)
             .select_related(*COMMON_SELECT).prefetch_related(*COMMON_PREFETCH)
             .order_by("-fecha_publicacion"))
    ctx = {"posts": posts, "archive_year": year, "archive_month": month}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_list.html", ctx)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.select_related(*COMMON_SELECT)
                             .prefetch_related(*COMMON_PREFETCH), slug=slug, publicado=True)
    # relacionados (misma categoría)
    related = (BlogPost.objects.filter(publicado=True, categoria=post.categoria)
               .exclude(id=post.id).order_by("-fecha_publicacion")[:3])
    ctx = {"post": post, "related": related}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_detail.html", ctx)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.select_related(*COMMON_SELECT)
                             .prefetch_related(*COMMON_PREFETCH),
                             slug=slug, publicado=True)

    # Envío de comentario
    form = BlogCommentForm()
    if request.method == "POST":
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            # datos de traza
            c.ip_address = request.META.get("REMOTE_ADDR")
            c.user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]
            # si el usuario está autenticado, lo asociamos
            if request.user.is_authenticated:
                c.user = request.user
                if not c.nombre:
                    c.nombre = request.user.get_full_name() or request.user.get_username()
                if not c.email and hasattr(request.user, "email"):
                    c.email = request.user.email
            # queda PENDING por defecto; moderas en admin
            c.save()
            messages.success(request, "¡Gracias! Tu comentario quedará visible cuando sea aprobado.")
            return HttpResponseRedirect(request.path)

    # Comentarios visibles (aprobados)
    comentarios = post.comentarios.filter(status=BlogComment.Status.APPROVED).select_related("user")

    related = (BlogPost.objects.filter(publicado=True, categoria=post.categoria)
               .exclude(id=post.id).order_by("-fecha_publicacion")[:3])

    ctx = {"post": post, "related": related, "comentarios": comentarios, "form": form}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_detail.html", ctx)