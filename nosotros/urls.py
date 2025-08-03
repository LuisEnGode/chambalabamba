from django.urls import path
from . import views

urlpatterns = [
    path('nuestro-camino/', views.nuestro_camino, name='nuestro_camino'),
    path('pilares/bienestar/', views.pilar_bienestar, name='pilar_bienestar'),
    path('pilares/ecologia/', views.pilar_ecologia, name='pilar_ecologia'),
    path('pilares/economia/', views.pilar_economia, name='pilar_economia'),
    path('pilares/sociocultural/', views.pilar_sociocultural, name='pilar_sociocultural'),

]
