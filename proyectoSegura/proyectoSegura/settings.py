"""
Django settings for proyectoSegura project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ["https://programacion2024brd", "https://127.0.0.1", "https://google.com"]
CSRF_ALLOWED_ORIGINS = ["https://programacion2024brd", "https://127.0.0.1", "https://google.com"]
CORS_ORIGINS_WHITELIST = ["https://programacion2024brd", "https://127.0.0.1", "https://google.com"]

LIMITE_INTENTOS_LOGIN = 3
LIMITE_SEGUNDOS_LOGIN = 60
LIMITE_SEGUNDOS_TOKEN = 120

#COOKIES CONFIGURATION
SESSION_COOKIE_AGE = 3600 # 1 hora
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # se destruye la sesión si se cierra el navegador

SESSION_COOKIE_SECURE = True # sólo en producción https
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_HTTPONLY = True 



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'db',
    'django_recaptcha',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyectoSegura.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('proyectoSegura/templates')],
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

WSGI_APPLICATION = 'proyectoSegura.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST', 'bd'),
        'PORT': os.environ.get('DB_PORT')
    }
}

# Que tal

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ReCaptcha v2
RECAPTCHA_PUBLIC_KEY = '6LcuvvMpAAAAAGvcxN3PHCy_ACBaiiGQ9sBgdliQ'

RECAPTCHA_PRIVATE_KEY = '6LcuvvMpAAAAAGYz7-Qw49SHLOpIUo-fbxMAqaN2'
# Application definition

CSRF_TRUSTED_ORIGINS = ['https://*.programacion2024brd', 'https://*.127.0.0.1']