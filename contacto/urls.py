from django.urls import path
from . import views

app_name = 'contacto'

urlpatterns = [
    path('', views.index, name='contacto')
]
