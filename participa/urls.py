from django.urls import path
from . import views
from .views import estancias_list,estancia_detail

urlpatterns = [
    path("", views.voluntariado, name="voluntariado"),
    path("visitas-guiadas", views.visitas, name="visitas-guiadas"),
    #path("estancias", views.estancias, name="estancias"),
    #path("estancias/<int:id>", views.estancia_detail, name="estancia-detail"),
    path("donaciones/", views.donaciones, name="donaciones"),

    path("estancias", estancias_list, name="estancias"),
    path("estancias/<slug:slug>/", estancia_detail, name="estancia_detail"),
]
