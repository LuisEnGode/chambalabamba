from django.shortcuts import render

def nuestro_camino(request):
    return render(request, 'nosotros/nuestro_camino.html')

def pilar_ecologia(request):
    return render(request, 'nosotros/pilares/ecologia.html')

def pilar_economia(request):
    return render(request, 'nosotros/pilares/economia.html')
