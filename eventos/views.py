from django.shortcuts import render, get_object_or_404
from .models import Festival, Taller

# Create your views here.

def escuela_viva(request):
    return render(request, 'eventos/escuela.html')

def talleres(request):
    talleres = Taller.objects.all()
    return render(request, 'eventos/talleres.html', {'talleres': talleres})

def taller_detail(request, slug):
    taller = get_object_or_404(Taller, slug=slug)
    return render(request, 'eventos/taller_detail.html', {'taller': taller})

def retiros(request):
    return render(request, 'eventos/retiros.html')

def artes(request):
    return render(request, 'eventos/artes.html')

def terapias(request):
    return render(request, 'eventos/terapias.html')

def festivales(request):
    festivales = Festival.objects.all()
    return render(request, 'eventos/festivales.html', {'festivales': festivales})

def festival_detail(request, slug):
    festival = get_object_or_404(Festival, slug=slug)
    return render(request, 'eventos/festival_detail.html', {'festival': festival})
