from django.shortcuts import render


def voluntariado(request):
    return render(request, 'participa/voluntariado.html')

def visitas(request):
    return render(request, 'participa/visitas-guiadas.html')



# Create your views here.
