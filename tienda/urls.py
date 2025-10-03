from django.urls import path
from . import views

app_name = "tienda"

urlpatterns = [
    path("", views.lista_productos, name="tienda"),
    path("<slug:slug>/", views.detalle_producto, name="detalle-producto"),
]
