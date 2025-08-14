from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
#Clase
class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True,verbose_name=_("Nombre"))
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre if self.nombre else (self.descripcion or "Sin nombre")

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    especialidades = models.ManyToManyField(Especialidad, blank=True)
    nom_lugar =  models.TextField(blank=True, null=True)
    nom_lugar2 = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    ubicacion2 = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    anios_experiencia = models.PositiveIntegerField(blank=True, null=True)
    OPCIONES_ATENCION = [
        ("Solo adultos", "Solo adultos"),
        ("Solo niños", "Solo niños"),
        ("Ambos", "Adultos y niños"),
    ]

    adultos_ninos = models.CharField(
        max_length=20,
        choices=OPCIONES_ATENCION,
        blank=True,
        null=True
    )
    imagen = models.ImageField(upload_to='perfiles_usuario', blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    direccion2 = models.CharField(max_length=100, blank=True, null=True)
    contacto1 = models.CharField(max_length=100, blank=True, null=True)
    contacto2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.usuario:
            return self.usuario.username or f"Usuario ID {self.usuario.id}"
        return "Usuario sin nombre"

def save(self, *args, **kwargs):
    if not self.tipo_usuario:
        admin_tipo, created = TipoUsuario.objects.get_or_create(nombre="Administrador")
        self.tipo_usuario = admin_tipo
    super().save(*args, **kwargs)