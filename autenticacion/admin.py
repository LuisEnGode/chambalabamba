from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite

from .models import PerfilUsuario, TipoUsuario, Especialidad


class MiAdminSite(AdminSite):
    # Parche para el problema del venv: forzar plantilla por defecto del admin
    index_template = "admin/index.html"


# ----- ModelAdmins -----
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = "Perfil de Usuario"


class UsuarioAdmin(UserAdmin):
    inlines = [PerfilUsuarioInline]
    list_display = ["username", "email", "get_tipo_usuario"]

    def get_tipo_usuario(self, obj):
        # Evita fallar si aún no existe el perfil
        perfil = getattr(obj, "perfilusuario", None)
        return getattr(perfil, "tipo_usuario", "-")
    get_tipo_usuario.short_description = "Tipo de Usuario"
    get_tipo_usuario.admin_order_field = "perfilusuario__tipo_usuario"


# ----- Registro en el admin por defecto (si NO usas MiAdminSite en urls.py) -----
# (Si vas a usar MiAdminSite en urls.py, puedes ignorar esta sección y registrar en ese sitio)
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)
admin.site.register(TipoUsuario, TipoUsuarioAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
