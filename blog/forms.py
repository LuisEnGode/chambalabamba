from django import forms


class PostForm(forms.ModelForm):
    class Meta:

        fields = ['titulo', 'contenido', 'imagen', 'categorias']
        widgets = {
            'categorias': forms.CheckboxSelectMultiple()
        }
