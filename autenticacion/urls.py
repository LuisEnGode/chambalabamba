from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import VRegistro,cerrar_sesion,logear,actualizar_perfil

urlpatterns = [


    path("", VRegistro.as_view(), name="Autenticacion"),
    path("cerrar_sesion/", cerrar_sesion, name="cerrar_sesion"),
    path("logear/", logear, name="logear"),
    path("actualizar_perfil/", actualizar_perfil, name="actualizar_perfil"),
]