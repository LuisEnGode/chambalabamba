from django import forms
from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    # Honeypot anti-bots
    hp = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = BlogComment
        fields = ("parent", "nombre", "email", "website", "cuerpo", "hp")
        widgets = {
            "parent": forms.HiddenInput(),                 # <- clave para “Responder”
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email (opcional)"}),
            "website": forms.URLInput(attrs={"placeholder": "Sitio (opcional)"}),
            "cuerpo": forms.Textarea(attrs={"rows": 4, "placeholder": "Escribe tu comentario…"}),
        }

    def clean_hp(self):
        v = self.cleaned_data.get("hp")
        if v:
            raise forms.ValidationError("Error de validación.")
        return v
