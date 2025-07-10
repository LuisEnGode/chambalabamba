from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validate_no_rude_words(value):
    rude_words = [
        'fuck', 'shit', 'damn', 'hell', 'bitch', 'bastard',
        'idiot', 'moron', 'dumbass', 'jerk', 'retard',
        'porn', 'sex', 'blowjob', 'dick', 'pussy', 'tits',
        'racist', 'nazi', 'hate', 'kill', 'die', 'suicide',
        'crap', 'ass', 'whore', 'slut', 'motherf***er',
        'mierda', 'joder', 'coño', 'puta', 'cabrón', 'gilipollas',
        'idiota', 'imbécil', 'pendejo', 'pelotudo', 'tonto',
        'sexo', 'porno', 'polla', 'tetas', 'verga', 'follar',
        'odio', 'matar', 'morir', 'nazi', 'racista',
        'maldito', 'asqueroso', 'desgraciado'
    ]
    for word in rude_words:
        if word in value.lower():
            raise ValidationError(f"Por favor, evita el uso de palabras inapropiadas como '{word}'.")


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nombres',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
        min_length=3,
        max_length=100,
        validators=[validate_no_rude_words]
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        min_length=5,
        max_length=150,
        validators=[validate_no_rude_words]
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos."
    )
    phone = forms.CharField(
        validators=[phone_regex, validate_no_rude_words],
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        max_length=17
    )
    subject = forms.CharField(
        label='Asunto',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}),
        min_length=5,
        max_length=100,
        validators=[validate_no_rude_words]
    )
    message = forms.CharField(
        label='Mensaje',
        required=True,
        widget=forms.Textarea(attrs={'class': 'textarea-control', 'placeholder': 'Mensaje'}),
        min_length=10,
        max_length=1000,
        validators=[validate_no_rude_words]
    )
