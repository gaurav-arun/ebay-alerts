"""
Django settings for alerts_backend project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os  # noqa: E402

from .settings import *  # noqa: E402, F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


SPECTACULAR_SETTINGS = {
    "TITLE": "Ebay Alerts",
    "DESCRIPTION": "APIs to perform CRUD operations for Alerts",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVERS": [{"url": "http://localhost:8000/", "description": "Local server"}],
}


ALLOWED_HOSTS = []
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Swagger UI
    "http://localhost:3000",  # Alert Frontend
]


# Ebay API settings
EBAY_API_ENV = os.environ.get("EBAY_API_ENV", "sandbox")
EBAY_CLIENT_ID_SANDBOX = os.environ.get("EBAY_CLIENT_ID_SANDBOX")
EBAY_CLIENT_SECRET_SANDBOX = os.environ.get("EBAY_CLIENT_SECRET_SANDBOX")
EBAY_CLIENT_ID_PRODUCTION = os.environ.get("EBAY_CLIENT_ID_PRODUCTION")
EBAY_CLIENT_SECRET_PRODUCTION = os.environ.get("EBAY_CLIENT_SECRET_PRODUCTION")
EBAY_MOCK_SERVER_URL = os.environ.get("EBAY_MOCK_SERVER_URL")


# Email settings for Mailtrap
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "sandbox.smtp.mailtrap.io")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "2525")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "False") == "True"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"


# Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

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
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}


# PubSub
PUBSUB_HOST = os.environ.get("PUBSUB_HOST", "localhost")
PUBSUB_PORT = os.environ.get("PUBSUB_PORT", 6379)
PUBSUB_CHANNEL = os.environ.get("PUBSUB_CHANNEL", "ebay-alerts")
PUBSUB_DEFAULT_DB = os.environ.get("PUBSUB_DEFAULT_DB", 0)
