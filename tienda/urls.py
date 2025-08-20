from django.urls import path
from . import views



urlpatterns = [
    path('', views.panel_produtos, name='tienda'),
    path("tienda/<int:id>", views.detalle_producto, name="detalle-producto"),
]
