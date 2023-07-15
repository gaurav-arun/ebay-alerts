"""
Django settings for alerts_backend project.

Generated by 'django-admin startproject' using Django 4.2.2.

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
SECRET_KEY = "django-insecure-1x^a)b3k429d%$xfy5c75ck)ep&y6da9p6@oc96hf@**f&a^$&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Ebay API settings
EBAY_API_ENV = os.environ.get("EBAY_API_ENV", "sandbox")
EBAY_CLIENT_ID_SANDBOX = os.environ.get("EBAY_CLIENT_ID_SANDBOX")
EBAY_CLIENT_SECRET_SANDBOX = os.environ.get("EBAY_CLIENT_SECRET_SANDBOX")
EBAY_CLIENT_ID_PRODUCTION = os.environ.get("EBAY_CLIENT_ID_PRODUCTION")
EBAY_CLIENT_SECRET_PRODUCTION = os.environ.get("EBAY_CLIENT_SECRET_PRODUCTION")
EBAY_MOCK_SERVER_URL = os.environ.get("EBAY_MOCK_SERVER_URL", "http://localhost:3000")

# PubSub settings
PUBSUB_HOST = os.environ.get("PUBSUB_HOST", "localhost")
PUBSUB_PORT = os.environ.get("PUBSUB_PORT", 6379)
PUBSUB_CHANNEL = os.environ.get("PUBSUB_CHANNEL", "ebay-alerts")

ALLOWED_HOSTS = ["host.docker.internal", "localhost"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
]

SPECTACULAR_SETTINGS = {
    "TITLE": "Ebay Alerts",
    "DESCRIPTION": "APIs to perform CRUD operations for Alerts",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVERS": [{"url": "http://localhost:8000/", "description": "Local server"}],
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
}

# Email settings for Inbucket (Local)
# -----------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = "2500"
EMAIL_HOST_USER = "your@djangoapp.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@ebayalerts.com")

# Application definition

INSTALLED_APPS = [
    "alerts.apps.AlertsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "django_celery_beat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "alerts_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(process)d] %(levelname)s %(asctime)s %(module)s "
            "%(name)s.%(funcName)s:%(lineno)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}

WSGI_APPLICATION = "alerts_backend.wsgi.application"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = ""

POSTGRES_HOST = "localhost"
REDIS_HOST = "localhost"

# Redis
REDIS_URL = f"redis://{REDIS_HOST}:6379"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "DOC",
    }
}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ebay_alert",
        "USER": "ebay_alert",
        "PASSWORD": "ebay_alert",
        "HOST": f"{POSTGRES_HOST}",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        )
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
