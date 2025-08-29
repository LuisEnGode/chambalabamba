from django.urls import path
from . import views



urlpatterns = [
    path("", views.voluntariado, name="voluntariado"),
    path("visitas-guiadas", views.visitas, name="visitas-guiadas"),
    path("estancias", views.estancias, name="estancias"),
    path("estancias/<int:id>", views.estancia_detail, name="estancia-detail"),
    path("donaciones/", views.donaciones, name="donaciones"),
]
