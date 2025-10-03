# blog/views.py
from django.shortcuts import render, get_object_or_404,redirect
from .models import BlogPage, BlogCategory, BlogTag, BlogAuthor
from django.contrib import messages
from .forms import BlogCommentForm
from .models import BlogComment,BlogSidebarWidget
from django.db.models import Count, Q
from django.db.models import Prefetch, Q   # <- agrega Prefetch (y Q si lo usas)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import BlogPostForm
from .models import BlogPost, BlogAuthor

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

def _get_author_for_user(user):
    """
    Devuelve BlogAuthor para el usuario:
      1) slug == username
      2) nombre == full_name/username
      3) si es staff, lo crea automáticamente
    """
    username = (user.get_username() or "").strip()
    full_name = (user.get_full_name() or "").strip() or username

    author = BlogAuthor.objects.filter(slug=username).first()
    if author: return author

    author = BlogAuthor.objects.filter(nombre__iexact=full_name).first()
    if author: return author

    if user.is_staff:
        from django.utils.text import slugify
        return BlogAuthor.objects.create(nombre=full_name, slug=slugify(username or full_name))
    return None

class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "blog.add_blogpost"
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog_list")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        action = request.POST.get("action")
        if action == "preview" and form.is_valid():
            draft = form.save(commit=False)
            author = _get_author_for_user(request.user)
            draft.autor = author
            if not draft.slug:
                draft.slug = form.generate_unique_slug(form.cleaned_data.get("titulo",""))
            context = self.get_context_data(form=form, preview_obj=draft, is_preview=True)
            return self.render_to_response(context)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        author = _get_author_for_user(self.request.user)
        if not author:
            form.add_error(None, "No se pudo asociar un autor a tu usuario. Pide a un admin que te cree un BlogAuthor.")
            return self.form_invalid(form)

        post.autor = author

        action = self.request.POST.get("action")
        if action == "publish":
            post.publicado = True
            if not post.fecha_publicacion:
                post.fecha_publicacion = timezone.now()
        else:
            post.publicado = False  # guardar como borrador

        if not post.slug:
            post.slug = form.generate_unique_slug(form.cleaned_data.get("titulo",""))

        post.save()
        form.save_m2m()
        messages.success(self.request, "¡Post creado!" if action != "publish" else "¡Post publicado!")
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "blog.change_blogpost"
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/post_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        action = request.POST.get("action")
        if action == "preview" and form.is_valid():
            draft = form.save(commit=False)
            draft.autor = self.object.autor  # conserva el autor
            context = self.get_context_data(form=form, preview_obj=draft, is_preview=True)
            return self.render_to_response(context)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        action = self.request.POST.get("action")
        if action == "publish":
            post.publicado = True
            if not post.fecha_publicacion:
                post.fecha_publicacion = timezone.now()
        else:
            post.publicado = False
        if not post.slug:
            post.slug = form.generate_unique_slug(form.cleaned_data.get("titulo",""))
        post.save()
        form.save_m2m()
        messages.success(self.request, "¡Post actualizado!" if action != "publish" else "¡Post publicado!")
        return super().form_valid(form)