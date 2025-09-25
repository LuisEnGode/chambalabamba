from django.urls import path,include
from blog import views


urlpatterns = [

    path('',views.blog,name="Blog"),
    path("detail", views.detail, name="detail"),

]
