from django.urls import path
from . import views

app_name = 'inicio'

urlpatterns = [
    path('', views.home, name='home'),
]
