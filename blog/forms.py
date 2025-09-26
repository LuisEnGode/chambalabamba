from django import forms
from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    # honeypot
    hp = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = BlogComment
        fields = ("nombre", "email", "website", "cuerpo", "hp")
        widgets = {
            "cuerpo": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_hp(self):
        v = self.cleaned_data.get("hp")
        if v:  # si el bot lo rellena
            raise forms.ValidationError("Error de validación.")
        return v
