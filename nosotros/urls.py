from django.urls import path
from . import views

urlpatterns = [
    path('nuestro-camino/', views.nuestro_camino, name='nuestro_camino'),
    path('pilares/ecologia/', views.pilar_ecologia, name='pilar_ecologia'),
    path('pilares/economia/', views.pilar_economia, name='pilar_economia'),
]
