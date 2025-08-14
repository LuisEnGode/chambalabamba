from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models
from .models import PerfilUsuario, TipoUsuario, Especialidad
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit


# 📌 Formulario de Registro
# 📌 Formulario de Registro
class RegistroFormulario(UserCreationForm):
    # Tipo de usuario editable
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.exclude(nombre__in=['Administrador', 'Usuario', 'Usuario Normal']),
        label="Tipo de usuario",
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'tipo_usuario']

    def save(self, commit=True):
        user = super().save(commit=False)  # Guardar usuario sin confirmar
        if commit:
            user.save()  # Guardar usuario en la base de datos

        # Crear el perfil de usuario asociado
        tipo_usuario = self.cleaned_data['tipo_usuario']
        PerfilUsuario.objects.create(usuario=user, tipo_usuario=tipo_usuario)

        return user



# 📌 Formulario para CLIENTES (básico)
class PerfilBasicoForm(forms.ModelForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.exclude(nombre__in=['Administrador', 'Usuario', 'Usuario Normal']),
        label="Tipo de usuario",
        required=True,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# 📌 Formulario para PROFESIONALES (con especialidades y más datos)
class PerfilProfesionalForm(forms.ModelForm):
    # Campos relacionados a PerfilUsuario
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.exclude(nombre__in=['Administrador', 'Usuario', 'Usuario Normal']),
        label="Tipo de usuario",
        required=True,
    )

    especialidades = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Especialidades"
    )

    anios_experiencia = forms.IntegerField(required=False, label="Años de experiencia")

    OPCIONES_ATENCION = [
        ("Solo adultos", "Solo adultos"),
        ("Solo niños", "Solo niños"),
        ("Ambos", "Adultos y niños"),
    ]

    adultos_ninos = forms.ChoiceField(
        choices=[
            ("Solo adultos", "Solo adultos"),
            ("Solo niños", "Solo niños"),
            ("Ambos", "Adultos y niños"),
        ],
        required=False,
        label="¿A quién atiendes?"
    )

    nom_lugar = forms.CharField(
        max_length=100,
        required=False,
        label="Nombre del lugar de atención principal"
    )

    direccion = forms.CharField(max_length=100, required=False, label="Direccion del lugar de atención principal")
    ubicacion = forms.CharField(max_length=100, required=False, label="Ubicación principal (latitud, longitud)")

    nom_lugar2 = forms.CharField(
        max_length=100,
        required=False,
        label="Nombre del segundo lugar (opcional)"
    )

    direccion2 = forms.CharField(max_length=100, required=False, label="Direccion del lugar de atención secundaria")
    ubicacion2 = forms.CharField(
        max_length=100,
        required=False,
        label="Ubicación secundaria (latitud, longitud)"
    )

    contacto1 = forms.CharField(max_length=100, required=False, label="Contacto principal")
    contacto2 = forms.CharField(max_length=100, required=False, label="Contacto secundario")

    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción de tus servicios de forma general")

    # Campos del modelo User
    first_name = forms.CharField(max_length=30, required=False, label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, label="Apellido")
    email = forms.EmailField(required=False, label="Correo electrónico")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.tipo_usuario.nombre != "Cliente":
            self.fields['tipo_usuario'].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = True  # Evita duplicación automática
        self.helper.layout = Layout(
            Fieldset("📝 Datos del usuario", 'first_name', 'last_name', 'email'),
            Fieldset("👤 Perfil profesional",
                     'tipo_usuario', 'especialidades', 'anios_experiencia', 'adultos_ninos',
                     'nom_lugar', 'direccion', 'ubicacion',
                     'nom_lugar2', 'direccion2', 'ubicacion2',
                     'contacto1', 'contacto2', 'descripcion', 'imagen'
                     ),
            Submit('submit', 'Guardar cambios', css_class='btn btn-success')
        )
    class Meta:
        model = PerfilUsuario
        fields = [
            'tipo_usuario',
            'especialidades',
            'anios_experiencia',
            'adultos_ninos',
            'nom_lugar',
            'direccion',
            'ubicacion',
            'nom_lugar2',
            'direccion2',
            'ubicacion2',
            'contacto1',
            'contacto2',
            'descripcion',
            'imagen',
        ]

    def save(self, commit=True):
        perfil = super().save(commit=False)

        # Guardamos datos del usuario
        if perfil.usuario:
            usuario = perfil.usuario
            usuario.first_name = self.cleaned_data.get('first_name', '')
            usuario.last_name = self.cleaned_data.get('last_name', '')
            usuario.email = self.cleaned_data.get('email', '')
            if commit:
                usuario.save()

        # Guardamos tipo de usuario
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        if perfil.tipo_usuario != tipo_usuario:
            perfil.tipo_usuario = tipo_usuario

        if commit:
            perfil.save()
            self.save_m2m()  # Guarda las especialidades (ManyToMany)

        return perfil