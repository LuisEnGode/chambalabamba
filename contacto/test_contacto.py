import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chambalabamba.settings')

import django
django.setup()


from django.test import TestCase
from unittest.mock import patch, MagicMock
from contacto.forms import ContactForm
from django.core import mail
from django.conf import settings
from django.http import HttpRequest
from contacto.views import index, gracias
from django.middleware.csrf import CsrfViewMiddleware
from django.core.exceptions import PermissionDenied
import pytest
from django.test import Client
from django.urls import reverse


class ContactoTests(TestCase):
    def setUp(self):
        # Dummy EMAIL_HOST_USER for testing purposes
        settings.EMAIL_HOST_USER = 'test@example.com'

    def test_contact_form_valid(self):
        form_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "subject": "Test Subject",
            "message": "This is a test message.",
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form_data = {
            "name": "",  # Invalid
            "email": "not-an-email",  # Invalid
            "phone": "1234567890",
            "subject": "Test Subject",
            "message": "This is a test message.",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)

    @patch('contacto.views.render')
    def test_index_view_get(self, mock_render):
        request = HttpRequest()
        request.method = 'GET'
        
        index(request)
        
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], request)
        self.assertEqual(args[1], 'contacto/index.html')
        self.assertIsInstance(args[2]['form'], ContactForm)

    @patch('contacto.views.send_mail')
    @patch('contacto.views.redirect')
    def test_index_view_post_success(self, mock_redirect, mock_send_mail):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "+1987654321",
            "subject": "Another Test",
            "message": "This is another test message.",
        }
        
        index(request)
        
        mock_send_mail.assert_called_once()
        mock_redirect.assert_called_once_with('contacto:gracias')

    @patch('contacto.views.render')
    def test_index_view_post_invalid_form(self, mock_render):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "name": "",  # Invalid
            "email": "invalid",  # Invalid
            "phone": "",
            "subject": "",
            "message": "",
        }
        
        index(request)
        
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], request)
        self.assertEqual(args[1], 'contacto/index.html')
        self.assertIsInstance(args[2]['form'], ContactForm)
        self.assertFalse(args[2]['form'].is_valid())

    @patch('contacto.views.render')
    def test_gracias_view(self, mock_render):
        request = HttpRequest()
        request.method = 'GET'
        
        gracias(request)
        
        mock_render.assert_called_once_with(request, 'contacto/gracias.html')

    def test_csrf_middleware_rejection(self):
        # Make a POST request to the contact form URL without CSRF token
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("contacto:index"), {
            "name": "CSRF Test",
            "email": "csrf@example.com",
            "phone": "1234567890",
            "subject": "CSRF Test Subject",
            "message": "This message should be blocked by CSRF.",
        }, secure=True)

        self.assertEqual(response.status_code, 403)  # Expect a redirect
        self.assertIn("CSRF verification failed. Request aborted.", response.content.decode())  # Check the error message
