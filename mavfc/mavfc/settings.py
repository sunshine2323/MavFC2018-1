"""
Django settings for mavfc project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.conf.global_settings import EMAIL_BACKEND

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yifvznb8)7&d-85x#*yv1js46&_%17gs26of-cc27+3ecg6o5@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'experiment',
    'foodcomputer',
    'user',
    'rest_framework',
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

ROOT_URLCONF = 'mavfc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'mavfc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# _ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "media"),
]



SITE_ID = 1



from django.core.urlresolvers import reverse_lazy

LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = reverse_lazy('dj-auth:login')
LOGOUT_URL = reverse_lazy('dj-auth:logout')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'mavfc1234'
EMAIL_HOST_USER = 'maverick.food.comp@gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[MAVFC] '
SERVER_EMAIL = 'maverick.food.comp@gmail.com'
DEFAULT_FROM_EMAIL = 'maverick.food.comp@gmail.com'



from .log_filters import ManagementFilter

verbose = (
    "[%(asctime)s] %(levelname)s "
    "[%(name)s:%(lineno)s] %(message)s")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'remove_migration_sql': {
            '()': ManagementFilter,
        },
    },
    'handlers': {
        'console': {
            'filters': ['remove_migration_sql'],
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'verbose': {
            'format': verbose,
            'datefmt': "%Y-%b-%d %H:%M:%S"
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'formatter': 'verbose'
        },
    },
}






