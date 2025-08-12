from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["-created"]

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    contenido = RichTextUploadingField()
    imagen = models.ImageField(upload_to="blog/", null=True, blank=True)
    imagen_2 = models.ImageField(upload_to='posts/', blank=True, null=True)
    imagen_3 = models.ImageField(upload_to='posts/', blank=True, null=True)
    autor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created"]

    def __str__(self):
        return self.titulo