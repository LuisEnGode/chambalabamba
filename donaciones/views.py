from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from decouple import config
import requests
import json
# from paypal.standard.forms import PayPalPaymentsForm # No longer needed
from .models import DonacionSection, Donacion
import uuid
from decimal import Decimal, InvalidOperation

# Import the make_paypal_payment function from the new utility file
from .paypal_utils import make_paypal_payment

def index(request):
    donacion_sections = DonacionSection.objects.filter(publicado=True)
    return render(request, 'donaciones/donaciones.html', {'donacion_sections': donacion_sections})

def donacion_paypal(request):
    if request.method == 'POST':
        # Try to get amount from radio buttons first, then from the 'other' input field
        monto = request.POST.get('amount')
        if not monto:
            monto = request.POST.get('amount_other')

        # Basic validation to ensure monto is not None or empty before creating Donacion
        if not monto:
            # Handle the case where no amount is provided. Redirect to an error page or show a message.
            return redirect('donaciones') # Or redirect to a specific error page

        nombre = request.POST.get('first_name', 'Anónimo')
        email = request.POST.get('email', 'anonimo@example.com')

        # Ensure monto is a Decimal before saving
        try:
            monto_decimal = Decimal(monto)
        except InvalidOperation:
            # Handle invalid amount format
            return redirect('donaciones') # Or redirect to a specific error page

        donacion = Donacion.objects.create(
            nombre=nombre,
            email=email,
            monto=monto_decimal,
        )

        # Use the API-based payment creation
        amount = monto # Use the string amount for PayPal API
        currency = "USD" # Default currency
        # Construct return and cancel URLs using reverse, passing the donacion.id as a custom parameter
        return_url = request.build_absolute_uri(reverse('donacion_exitosa')) + f"?custom_id={donacion.id}"
        cancel_url = request.build_absolute_uri(reverse('donacion_cancelada'))

        success, payment_id, approval_url = make_paypal_payment(amount, currency, return_url, cancel_url)

        if success:
            # Redirect to PayPal's approval URL
            return redirect(approval_url)
        else:
            # Handle error, perhaps render an error page or redirect to a generic error URL
            # Log the error details from make_paypal_payment if available
            print(f"Failed to initiate PayPal payment. Payment ID: {payment_id}, Approval URL: {approval_url}")
            return redirect('donaciones') # Redirect to donations page for now

    # If not POST, redirect to donations page
    return redirect('donaciones')

def donacion_exitosa(request):
    # Retrieve the custom_id (Donacion ID) from the URL parameters
    custom_id = request.GET.get('custom_id')
    payment_id = request.GET.get('paymentId') # Also get paymentId if available

    if custom_id:
        try:
            donacion = Donacion.objects.get(id=custom_id)
            # Update the donation status to completed
            donacion.completado = True
            if payment_id: # Only update paypal_id if paymentId is present
                donacion.paypal_id = payment_id
            donacion.save()
            print(f"Donacion {custom_id} marked as completed. PayPal ID: {payment_id}")
        except Donacion.DoesNotExist:
            # Handle case where Donacion object is not found
            print(f"Donacion with custom_id {custom_id} not found.")
        except Exception as e:
            # Handle other potential errors during update
            print(f"Error updating Donacion status for custom_id {custom_id}: {e}")
    else:
        print("No custom_id found in URL parameters for donacion_exitosa.")

    # Fetch the DonacionSection to display success message
    donacion_section = DonacionSection.objects.filter(publicado=True).first()
    context = {
        'donacion_section': donacion_section
    }
    return render(request, 'donaciones/donacion_exitosa.html', context)

def donacion_cancelada(request):
    # Fetch the DonacionSection to display cancellation message
    donacion_section = DonacionSection.objects.filter(publicado=True).first()
    context = {
        'donacion_section': donacion_section
    }
    return render(request, 'donaciones/donacion_cancelada.html', context)
