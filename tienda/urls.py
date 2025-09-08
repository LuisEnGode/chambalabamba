from django.urls import path
from . import views



urlpatterns = [
    path("", views.lista_productos, name="tienda"),
    path("<slug:slug>/", views.detalle_producto, name="detalle-producto"),
]
