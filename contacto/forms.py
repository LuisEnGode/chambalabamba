from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nombres', 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
        min_length=3,
        max_length=100
    )
    email = forms.EmailField(
        label='Correo Electrónico', 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        min_length=5,
        max_length=150
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos."
    )
    phone = forms.CharField(
        validators=[phone_regex], 
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
        max_length=100
    )
    message = forms.CharField(
        label='Mensaje', 
        required=True, 
        widget=forms.Textarea(attrs={'class': 'textarea-control', 'placeholder': 'Mensaje'}),
        min_length=10,
        max_length=1000
    )
