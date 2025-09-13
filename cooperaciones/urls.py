from django.urls import path
from . import views

app_name = "coops"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("<slug:slug>/", views.detalle, name="detalle"),
]
