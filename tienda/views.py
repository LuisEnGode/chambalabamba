from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import get_object_or_404, render
from .models import Producto

def lista_productos(request):
    productos = (Producto.objects
                 .filter(publicado=True)
                 .select_related("categoria")
                 .prefetch_related("imagenes")
                 .order_by("orden", "titulo"))
    return render(request, "tienda/panel-productos.html", {"productos": productos})

def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria").prefetch_related("imagenes"),
        slug=slug, publicado=True
    )
    relacionados = (Producto.objects.filter(publicado=True, categoria=producto.categoria)
                    .exclude(pk=producto.pk).order_by("orden")[:4])
    return render(request, "tienda/detalle-producto.html", {"producto": producto, "relacionados": relacionados})


