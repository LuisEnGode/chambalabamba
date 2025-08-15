from django.shortcuts import render

# Create your views here.

def escuela_viva(request):
    return render(request, 'eventos/escuela.html')

def talleres(request):
    return render(request, 'eventos/talleres.html')

def retiros(request):
    return render(request, 'eventos/retiros.html')

def artes(request):
    return render(request, 'eventos/artes.html')

def terapias(request):
    return render(request, 'eventos/terapias.html')

def festivales(request):
    return render(request, 'eventos/festivales.html')
