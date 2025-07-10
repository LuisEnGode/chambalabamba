from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Nuevo mensaje de contacto: {form.cleaned_data['subject']}"
            message = f"De: {form.cleaned_data['name']}\n"
            message += f"Mail: {form.cleaned_data['email']}\n\n"
            message += f"Contactos: {form.cleaned_data['phone']}\n\n"
            message += f"Mensaje: {form.cleaned_data['message']}"
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                # Send a confirmation email to the sender
                confirmation_subject = "Confirmación de recepción de mensaje"
                confirmation_message = f"Gracias por contactarnos. Hemos recibido tu mensaje:\n\n"
                confirmation_message += f"Asunto: {form.cleaned_data['subject']}\n"
                confirmation_message += f"Mensaje: {form.cleaned_data['message']}\n\n"
                confirmation_message += "Nos pondremos en contacto contigo pronto."

                send_mail(
                    confirmation_subject,
                    confirmation_message,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )

                #return redirect('contacto:gracias')
                success_message = "¡Mensaje enviado exitosamente!"
                form = ContactForm()  # Clear the form
                return render(request, 'contacto/index.html', {'form': form, 'success_message': success_message})
            except Exception as e:
                # Podrías loggear el error si quieres: print(e)
                print("Error al enviar el correo:", e)
                form.add_error(None, "No se pudo enviar el correo. Por favor, inténtalo de nuevo más tarde.")
    else:
        form = ContactForm()

    return render(request, 'contacto/index.html', {'form': form})

#def gracias(request):
#    return render(request, 'contacto/gracias.html')
