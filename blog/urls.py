from django.urls import path
from . import views

urlpatterns = [
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/categoria/<slug:slug>/", views.blog_list_by_category, name="blog_by_category"),
    path("blog/tag/<slug:slug>/", views.blog_list_by_tag, name="blog_by_tag"),
    path("blog/autor/<slug:slug>/", views.blog_list_by_author, name="blog_by_author"),
    path("blog/archivo/<int:year>/<int:month>/", views.blog_list_by_month, name="blog_by_month"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
]
