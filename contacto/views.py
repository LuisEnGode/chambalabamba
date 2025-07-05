from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            subject = form.cleaned_data['subject']
            message = f"De: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
            message += f"Teléfono: {form.cleaned_data['phone']}\n\n"
            message += form.cleaned_data['message']
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return redirect('contacto:index') # Redirect after POST
    else:
        form = ContactForm()

    return render(request, 'contacto/index.html', {'form': form})
