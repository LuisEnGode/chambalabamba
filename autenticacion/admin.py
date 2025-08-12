from django.contrib import admin

# Register your models here.
# mi_app/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import PerfilUsuario, TipoUsuario, Especialidad
from django.contrib.auth.admin import UserAdmin

# Registro de TipoUsuario
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Registro de Especialidad
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Personaliza el modelo de Usuario en el admin
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

class UsuarioAdmin(UserAdmin):
    inlines = [PerfilUsuarioInline]
    list_display = ['username', 'email', 'get_tipo_usuario']

    def get_tipo_usuario(self, obj):
        return obj.perfilusuario.tipo_usuario
    get_tipo_usuario.admin_order_field = 'perfilusuario__tipo_usuario'
    get_tipo_usuario.short_description = 'Tipo de Usuario'

# Re-registrar el modelo User con la clase personalizada
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

# Registro de modelos en el admin
admin.site.register(TipoUsuario, TipoUsuarioAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.unregister(User)  # Desregistrar el modelo User para registrar nuestro propio admin
admin.site.register(User, UsuarioAdmin)