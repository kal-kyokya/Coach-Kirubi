import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {'1', 'true', 'yes', 'on'}


def _env_list(name: str, default: str = '') -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(',') if item.strip()]


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')
DEBUG = _env_bool('DJANGO_DEBUG', 'true')

PRODUCTION_SUBDOMAIN = os.getenv('DJANGO_PRODUCTION_SUBDOMAIN', '').strip()
_allowed_hosts = set(_env_list('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1'))
if PRODUCTION_SUBDOMAIN:
    _allowed_hosts.add(PRODUCTION_SUBDOMAIN)
ALLOWED_HOSTS = sorted(_allowed_hosts)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'apps.programs',
    'apps.orders.',
    'apps.pages',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = _env_list('CORS_ALLOWED_ORIGINS', 'http:localhost:5173')

REST_FRAMEWORK = {
    'DEFAULT_RENDER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
}

# Reverse proxy support (Nginx -> Gunicorn unix socket)
USE_X_FORWARDED_HOST = _env_bool('DJANGO_USE_X_FORWARDED_HOST', True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL', '').rstrip('/')
_default_callback_path = '/api/orders/payments/mpesa/callback/'
mpesa_callback_url = os.getenv('MPESA_CALLBACK_URL', '').strip
if not mpesa_callback_url and PUBLIC_BASE_URL:
    mpesa_callback_url = f'{PUBLIC_BASE_URL}{_default_callback_path}'

if not DEBUG and mpesa_callback_url:
    lowered_callback = mpesa_callback_url.lower()
    if 'localhost' in lowered_callback or '127.0.0.1' in lowered_callback:
        raise ValueError('MPESA_CALLBACK_URL must be externally accessible in production.')

MPESA_CONFIG =  {
    'consumer_key': os.getenv('MPESA_CONSUMER_KEY', ''),
    'consumer_secret': os.getenv('MPESA_CONSUMER_SECRET', ''),
    'shortcode': os.getenv('MPESA_SHORTCODE', ''),
    'passkey': os.getenv('MPESA_PASSKEY', ''),
    'callback_url': mpesa_callback_url,
    'environment': os.getenv('MPESA_ENVIRONMENT', 'sandbox'),
    'timeout_seconds': int(os.getenv('MPESA_TIMEOUT_SECONDS', '25')),
    'mock_mode': _env_bool('MPESA_MOCK_MODE', True),
}
