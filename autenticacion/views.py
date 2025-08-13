from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import forms
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from autenticacion.forms import RegistroFormulario
from .models import PerfilUsuario
from .forms import PerfilBasicoForm, PerfilProfesionalForm
from .models import PerfilUsuario,TipoUsuario

# Create your views here.

class VRegistro(View):
    def get(self, request):
        form = RegistroFormulario()  # Usamos el formulario personalizado
        return render(request, "autenticacion/autenticacion.html", {"formulario": form})

    def post(self, request):
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario
            usuario = form.save()
            tipo_usuario = form.cleaned_data['tipo_usuario']

            # Verificar si el perfil ya existe
            perfil_usuario, created = PerfilUsuario.objects.get_or_create(usuario=usuario, tipo_usuario=tipo_usuario)

            # Si el perfil se crea, se manejará automáticamente por get_or_create
            # Si ya existe, simplemente no lo tocamos

            # Iniciar sesión después del registro
            login(request, usuario)
            return redirect('Home')  # Redirige a la página principal
        else:
            return render(request, "autenticacion/autenticacion.html", {"formulario": form})


def cerrar_sesion(request):
    print("Cerrando sesion")
    logout(request)
    return redirect('Home')

def logear(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            usuario = authenticate(username=usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                messages.error(request,"usuario no valido")
                return render(request, "login/login.html", {"formulario": form})
        else:
            messages.error(request, "informacion incorrecta")

    form = AuthenticationForm()
    return render(request, "login/login.html", {"formulario": form})


@login_required
def actualizar_perfil(request):
    if request.user.is_superuser:
        tipo_defecto = TipoUsuario.objects.get_or_create(nombre='Administrador')[0]
    else:
        tipo_defecto = TipoUsuario.objects.get_or_create(nombre='Usuario')[0]

    perfil_usuario, created = PerfilUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={'tipo_usuario': tipo_defecto}
    )

    if perfil_usuario.tipo_usuario is None:
        perfil_usuario.tipo_usuario = tipo_defecto
        perfil_usuario.save()

    # Usar solo un formulario completo
    perfil_form = PerfilProfesionalForm(
        request.POST or None,
        request.FILES or None,
        instance=perfil_usuario,
        initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
    )

    if request.method == 'POST':
        if perfil_form.is_valid():
            perfil = perfil_form.save()  # Este save() ya guarda el usuario también
            messages.success(request, "✅ Perfil actualizado correctamente.")
            return redirect('actualizar_perfil')

    return render(request, 'perfil/actualizar_perfil.html', {
        'perfil_form': perfil_form,
    })
