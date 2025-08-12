from django.shortcuts import render, get_object_or_404
from blog.models import Post, Categoria
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from autenticacion.models import PerfilUsuario, TipoUsuario, Especialidad


from django.db.models import Count
# Create your views here.

def blog(request):
    posts = Post.objects.all()
   # categorias = Categoria.objects.all()
    categorias = Categoria.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return render(request, "blog/blog-panel.html",{"posts":posts,"categorias":categorias})

def categoria(request,categoria_id):
    # Obtiene la categoría por su ID
    categoria = get_object_or_404(Categoria, id=categoria_id)
    # Filtra los posts relacionados con esa categoría
    posts = Post.objects.filter(categorias=categoria)
    return render(request, 'blog/categorias.html', {
        'posts': posts,
        'categoria': categoria  # ✅ más claro y coherente
    })


@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user  # Asignar el usuario actual como autor
            post.save()
            form.save_m2m()  # Guardar las categorías seleccionadas
            return redirect('Blog')  # Redirigir a la lista de posts
    else:
        form = PostForm()

    return render(request, 'blog/crear_post.html', {'form': form})



def detalle_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Obtén todas las categorías asociadas a ese post
    categorias = post.categorias.all()

    # Filtra todos los posts que pertenezcan a estas categorías (excluyendo el post actual)
    posts_relacionados = Post.objects.filter(categorias__in=categorias).exclude(id=post.id)


    profesionales = PerfilUsuario.objects.filter(tipo_usuario__nombre="Profesional")
    subscripciones_profesionales = {}
    for prof in profesionales:
        subscripciones_profesionales.setdefault(prof.usuario.id, {
            "plan": "free",
            "is_active": False,
        })

    profesionales_nuevos = PerfilUsuario.objects.filter(
        tipo_usuario__nombre="Profesional"
    ).order_by('usuario__date_joined')[:6]

    return render(request, 'blog/ver_post.html', {
        'post': post,'posts_relacionados':posts_relacionados,
        'subscripciones_profesionales': subscripciones_profesionales,
        'destacados': profesionales_nuevos,
    })
