from django.shortcuts import render

def nuestro_camino(request):
    return render(request, 'nosotros/nuestro_camino.html')

def pilar_bienestar(request):
    return render(request, 'nosotros/pilares/pilar_bienestar.html')

def pilar_ecologia(request):
    return render(request, 'nosotros/pilares/pilar_ecologia.html')

def pilar_economia(request):
    return render(request, 'nosotros/pilares/pilar_economia.html')

def pilar_sociocultural(request):
    return render(request, 'nosotros/pilares/pilar_sociocultural.html')
