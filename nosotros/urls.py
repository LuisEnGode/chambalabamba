from django.urls import path
from . import views
from .views import pilar_detail,topic_detail,nuestro_camino, gobernanza,principios_valores,territorio

app_name = "nosotros"

urlpatterns = [
    path("nuestro_camino", nuestro_camino, name="nuestro_camino"),
    path("pilares/<slug:slug>/", pilar_detail, name="pilar_detail"),
    path("<slug:slug>/", topic_detail, name="topic_detail"),



]
