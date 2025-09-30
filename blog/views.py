# blog/views.py
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Count
from .models import BlogPage, BlogPost, BlogCategory, BlogTag, BlogAuthor
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import BlogCommentForm
from .models import BlogComment,BlogSidebarWidget
from django.db.models import Count, Q
from django.db.models import Prefetch, Q   # <- agrega Prefetch (y Q si lo usas)

COMMON_PREFETCH = ("tags", "fotos")
COMMON_SELECT   = ("autor", "categoria")

def _base_ctx():
    page = (BlogPage.objects
            .select_related("header")
            .prefetch_related("widgets")
            .first())

    # Widgets publicados y ordenados
    widgets = page.widgets.filter(publicado=True).order_by("orden") if page else BlogSidebarWidget.objects.none()

    # Máximo límite que pidan los widgets de tipo "latest_posts"
    max_latest = max([w.limite or 5 for w in widgets if w.tipo == "latest_posts"] or [0])

    # Trae posts publicados hasta el máximo necesario (evitas consultas por widget)
    latest_posts = []
    if max_latest:
        latest_posts = (BlogPost.objects
                        .filter(publicado=True)
                        .select_related("autor", "categoria")
                        .prefetch_related("tags", "fotos")
                        .order_by("-fecha_publicacion")[:max_latest])

    # Archives & taxonomías
    archives = (BlogPost.objects.filter(publicado=True)
                .dates("fecha_publicacion", "month", order="DESC"))
    tags = (BlogTag.objects
            .annotate(n=Count("posts", filter=Q(posts__publicado=True), distinct=True))
            .order_by("nombre"))
    cats = (BlogCategory.objects
            .annotate(n=Count("posts", filter=Q(posts__publicado=True)))
            .order_by("nombre"))

    return {
        "page": page,
        "widgets": widgets,
        "latest_posts": latest_posts,
        "archives": archives,
        "all_tags": tags,
        "all_categories": cats,
    }

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
    post = get_object_or_404(
        BlogPost.objects.select_related(*COMMON_SELECT).prefetch_related(*COMMON_PREFETCH),
        slug=slug, publicado=True
    )

    if request.method == "POST":
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            #c.status = BlogComment.Status.APPROVED

            # Evita parent de otro post
            if c.parent and c.parent.post_id != post.id:
                c.parent = None

            # Traza
            # Usa los nombres que EXISTAN en tu modelo:
            # Si tu modelo tiene 'ip' y 'ua':
            c.ip = request.META.get("REMOTE_ADDR")
            c.ua = (request.META.get("HTTP_USER_AGENT") or "")[:255]
            # Si en tu modelo son 'ip_address' y 'user_agent', cambia las 2 líneas anteriores.

            # Usuario autenticado (opcional)
            if request.user.is_authenticated:
                c.user = request.user
                if not c.nombre:
                    c.nombre = request.user.get_full_name() or request.user.get_username()
                if not c.email and getattr(request.user, "email", ""):
                    c.email = request.user.email

            # Estado por defecto
            if not c.status:
                c.status = BlogComment.Status.PENDING

            c.save()
            messages.success(request, "¡Gracias! Tu comentario quedará visible cuando sea aprobado.")
            return redirect(request.path + "#comments")
    else:
        form = BlogCommentForm()

    # Comentarios visibles: solo top-level aprobados, con replies aprobadas prefetch
    aprobados_qs = BlogComment.objects.filter(status=BlogComment.Status.APPROVED)
    comentarios = (post.comentarios
                   .filter(status=BlogComment.Status.APPROVED, parent__isnull=True)
                   .select_related("user")
                   .prefetch_related(Prefetch("replies", queryset=aprobados_qs.order_by("creado"))))

    comentarios = comentarios.order_by("-creado")

    related = (BlogPost.objects.filter(publicado=True, categoria=post.categoria)
               .exclude(id=post.id).order_by("-fecha_publicacion")[:3])

    ctx = {"post": post, "related": related, "comentarios": comentarios, "form": form}
    ctx.update(_base_ctx())
    return render(request, "blog/blog_detail.html", ctx)