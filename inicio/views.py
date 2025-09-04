from django.shortcuts import render
from .models import HeroSlide, ValorCard, ProyectoCard, ProductoItem, InstaFoto

def home(request):
    ctx = {
        "hero_slides": HeroSlide.objects.filter(publicado=True).order_by("orden"),
        "valores": ValorCard.objects.filter(publicado=True).order_by("orden")[:12],
        "proyectos": ProyectoCard.objects.filter(publicado=True).order_by("orden")[:12],
        "productos": ProductoItem.objects.filter(publicado=True).order_by("orden")[:4],
        "insta": InstaFoto.objects.filter(publicado=True).order_by("orden")[:7],
    }
    return render(request, 'inicio/home.html',ctx)
