import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
print ("BD",BASE_DIR)
# Seguridad
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Aplicaciones instaladas
INSTALLED_APPS = [
    'autenticacion.apps.AutenticacionConfig',
    "core.apps.CoreConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',

    "crispy_forms",
    "crispy_bootstrap4",
    "django_cleanup.apps.CleanupConfig",
    # apps personalizadas:

    'inicio',
    'filosofia',
    'saberes',
    'escuela',
    'hospedaje',
    'voluntariado',
    'donaciones',
    'tienda',
    'noticias',
    'contacto',
    'blog',
    'participa',
    'contenido',
    "eventos.apps.EventosConfig",
    "nosotros.apps.NosotrosConfig",
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "perfil"
LOGOUT_REDIRECT_URL = "home"

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"


ROOT_URLCONF = 'chambalabamba.urls'
CKEDITOR_UPLOAD_PATH = "uploads/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chambalabamba.wsgi.application'

# Archivos estáticos
STATIC_URL = "/static/"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static'),
    os.path.join(BASE_DIR, 'contacto', 'static'),
    os.path.join(BASE_DIR, 'inicio', 'static'),
    os.path.join(BASE_DIR, 'nosotros', 'static'),
    os.path.join(BASE_DIR, 'donaciones', 'static'),
    os.path.join(BASE_DIR, 'blog', 'static'),
    os.path.join(BASE_DIR, 'participa', 'static'),
    os.path.join(BASE_DIR, 'tienda', 'static'),
    os.path.join(BASE_DIR, 'eventos', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Base de datos
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.eu'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
