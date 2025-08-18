from django.shortcuts import render


def voluntariado(request):
    return render(request, 'participa/voluntariado.html')

def visitas(request):
    return render(request, 'participa/visitas-guiadas.html')

def estancias(request):
    return render(request, 'participa/estancias/estancias.html')

def estancia_detail(request,id):
    return render(request, 'participa/estancias/estancia-detail.html')


# Create your views here.
