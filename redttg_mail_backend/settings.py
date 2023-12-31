import os
import rsa
from pathlib import Path
from tempfile import gettempdir
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

with open(os.path.join(BASE_DIR, 'public_notebook_key.pem'), 'rb') as f:
    NOTEBOOK_PUBLIC_KEY = rsa.PublicKey.load_pkcs1(f.read())

DEBUG = int(os.environ.get('DEBUG', 1)) > 0

ALLOWED_HOSTS = [
    "*" # Using because docker
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'corsheaders',
    'rest_framework',

    'redttg_mail_backend.auth_app',
    'redttg_mail_backend.mail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'redttg_mail_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'redttg_mail_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TZ', 'UTC')

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    os.environ.get('CSRF_FRONTEND_URL', "http://127.0.0.1"),
    os.environ.get('CSRF_DOMAIN', "http://localhost")
]

AUTH_USER_MODEL = 'auth_app.AccountModel'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(gettempdir(), 'files/'))

CELERY_BROKER_URL = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL