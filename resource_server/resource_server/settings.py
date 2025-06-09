"""
Django settings for resource_server project.
"""

from pathlib import Path
from urllib.parse import urlparse
import os
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = 'django-insecure-lyo(+5&g+-fwojm1=%jfnh7_8-#f3pdrh27l9qj@w8%z1u2dy#'
DEBUG = True

def get_ngrok_url():
    try:
        response = requests.get("http://ngrok:4040/api/tunnels")
        # Debug: print the response text
        print("Response from ngrok API:", response.text)
        data = response.json()
        tunnels = data.get('tunnels', [])
        if tunnels:
            # For simplicity, use the first tunnel's public_url
            return tunnels[0].get('public_url')
        else:
            print("No tunnels found in the response.")
    except Exception as e:
        print("Error fetching ngrok URL:", e)
    return None


NGROK_URL = get_ngrok_url()
SESSION_COOKIE_DOMAIN = urlparse(NGROK_URL).hostname

ALLOWED_HOSTS = [
    'localhost',
    SESSION_COOKIE_DOMAIN,
    
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photos',
    'corsheaders',
    'resource_server',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'resource_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'resource_server.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'resource_db'),
        'USER': os.getenv('DB_USER', 'resource_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'resource_password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Media files (uploaded images)
MEDIA_URL = '/resource/photos/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'photos')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT settings
JWT_PUBLIC_KEY = open('resource_server/keys/public.pem').read()
JWT_ALGORITHM = 'RS256'

# Proxy settings
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cross-origin settings
CORS_ALLOW_ALL_ORIGINS = True

# Secure cookies for cross-domain with ngrok
SESSION_COOKIE_DOMAIN = '.ngrok-free.app'
SESSION_COOKIE_PATH = '/resource/'
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']

FORCE_SCRIPT_NAME = "/resource"
STATIC_URL = "/static/"