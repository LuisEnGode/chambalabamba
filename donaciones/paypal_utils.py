from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from decouple import config
import requests
import json

def make_paypal_payment(amount, currency, return_url, cancel_url):
    # Set up PayPal API credentials
    client_id = config("PAYPAL_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")
    # Set up API endpoints
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_url = base_url + '/v1/payments/payment'

    # Request an access token
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        # Log the error for debugging
        print(f"PayPal API authentication failed: {token_response.status_code} - {token_response.text}")
        return False,"Failed to authenticate with PayPal API",None

    try:
        access_token = token_response.json()['access_token']
    except KeyError:
        print(f"Failed to get access token from PayPal API response: {token_response.text}")
        return False, "Failed to get access token", None

    # Create payment payload
    payment_payload = {
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'transactions': [{
            'amount': {'total': str(amount), 'currency': currency},
            'description': 'Donación para Chambalabamba' # Updated description
        }],
        'redirect_urls': {
            'return_url': return_url,
            'cancel_url': cancel_url
        }
    }

    # Create payment request
    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payment_response = requests.post(payment_url, data=json.dumps(payment_payload), headers=payment_headers)
    print(f"PayPal payment creation response: {payment_response.text}") # Log the full response

    if payment_response.status_code != 201:
        print(f"Failed to create PayPal payment: {payment_response.status_code} - {payment_response.text}")
        return False , 'Failed to create PayPal payment.',None

    try:
        payment_id = payment_response.json()['id']
        approval_url = next(link['href'] for link in payment_response.json()['links'] if link['rel'] == 'approval_url')
    except (KeyError, StopIteration):
        print(f"Failed to extract approval URL from PayPal payment response: {payment_response.text}")
        return False, "Failed to get approval URL", None

    return True, payment_id, approval_url

def execute_paypal_payment(payment_id, payer_id, expected_amount, expected_currency):
    client_id = config("PAYPAL_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_execute_url = base_url + f'/v1/payments/payment/{payment_id}/execute'

    # Authenticate with PayPal
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        return False, "Failed to authenticate with PayPal API"

    try:
        access_token = token_response.json()['access_token']
    except KeyError:
        return False, "Failed to get access token"

    # Execute the payment
    execute_payload = {'payer_id': payer_id}
    execute_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    execute_response = requests.post(payment_execute_url, data=json.dumps(execute_payload), headers=execute_headers)

    if execute_response.status_code != 200:
        return False, f"Failed to execute payment: {execute_response.text}"

    # Verify the payment details
    try:
        payment_details = execute_response.json()
        transaction = payment_details['transactions'][0]
        amount = transaction['amount']

        if payment_details['state'] == 'approved' and \
           amount['total'] == str(expected_amount) and \
           amount['currency'] == expected_currency:
            return True, "Payment verified successfully"
        else:
            return False, "Payment verification failed after execution"
    except (KeyError, IndexError):
        return False, "Failed to parse payment details after execution"
