from django.shortcuts import render, get_object_or_404
from .models import Estancia,ParticipaPage

def estancias_list(request):
    page = ParticipaPage.objects.select_related("header").first()
    estancias = (Estancia.objects
                 .filter(seccion="participa_estancias", publicado=True)
                 .order_by("orden","-creado"))
    return render(request, "participa/estancias/estancias_list.html",
                  {"estancias": estancias, "page": page})

def estancia_detail(request, slug):
    page = ParticipaPage.objects.select_related("header").first()
    e = get_object_or_404(Estancia, slug=slug, publicado=True)
    fotos = e.fotos.filter(publicado=True).order_by("orden","-creado")
    specs = e.specs.all().order_by("orden","id")
    return render(request, "participa/estancias/estancia_detail.html",
                  {"page": page, "e": e, "fotos": fotos, "specs": specs, "phone": e.phone_whatsapp or ""})

def voluntariado(request):
    return render(request, 'participa/voluntariado.html')

def visitas(request):
    return render(request, 'participa/visitas-guiadas.html')

def donaciones(request,id):
    return render(request, 'donaciones/donaciones.html')