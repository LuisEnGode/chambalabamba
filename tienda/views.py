from django.shortcuts import render

# Create your views here.


def panel_produtos(request):
    return render(request, 'tienda/panel-productos.html')

def detalle_producto(request, id):
    return render(request, 'tienda/detalle-producto.html')
