"""
URL configuration for chambalabamba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from it my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viewsgit
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.static import serve as serve_static
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')),
    path('contacto/', include('contacto.urls')),
    path('nosotros/', include('nosotros.urls')),
    path('eventos/', include('eventos.urls')),
    path('blog/', include('blog.urls')),
    path('participa/', include('participa.urls')),
    path('donaciones/', include('donaciones.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('tienda/', include('tienda.urls')),
    path("auth/", include("autenticacion.urls")),
   # path('login/', auth_views.LoginView.as_view(template_name='autenticacion/login.html'), name='login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)