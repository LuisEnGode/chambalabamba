from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Nuevo mensaje de contacto: {form.cleaned_data['subject']}"
            message = f"De: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
            message += f"Teléfono: {form.cleaned_data['phone']}\n\n"
            message += form.cleaned_data['message']
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                return redirect('contacto:gracias')
            except Exception as e:
                # Podrías loggear el error si quieres: print(e)
                print("Error al enviar el correo:", e)
                form.add_error(None, "No se pudo enviar el correo. Por favor, inténtalo de nuevo más tarde.")
    else:
        form = ContactForm()

    return render(request, 'contacto/index.html', {'form': form})

def gracias(request):
    return render(request, 'contacto/gracias.html')
