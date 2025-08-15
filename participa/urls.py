from django.urls import path
from . import views



urlpatterns = [
    path("", views.voluntariado, name="voluntariado"),
    path("visitas-guiadas", views.visitas, name="visitas-guiadas"),
]
