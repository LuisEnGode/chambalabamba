from django.urls import path,include
from blog import views
from blog.views import  crear_post

urlpatterns = [


    path('',views.blog,name="Blog"),
    path('categoria/<int:categoria_id>/',views.categoria,name="Categoria"),
    path('nuevo/', crear_post, name='crear_post'),
    path('post/<int:id>/', views.detalle_post, name='detalle_post'),
]
