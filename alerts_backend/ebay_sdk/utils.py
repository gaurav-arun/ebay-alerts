from django.conf import settings
import requests
from django.core.cache import cache
from django.conf import settings
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import logging
import base64
from dataclasses_json import LetterCase, config, dataclass_json
from .models import ItemSummary


def get_base_url():
    if settings.EBAY_API_ENV == 'production':
        return 'https://api.ebay.com'
    elif settings.EBAY_API_ENV == 'sandbox':
        return 'https://api.sandbox.ebay.com'
    elif settings.EBAY_API_ENV == 'mock':
        return 'http://localhost:8002'

    raise ValueError('EBAY_API_ENV is should be one of production, sandbox, or mock')


def get_encoded_oauth_basic_token() -> str:
    """
    Returns the base64 encoded string of ebay_client_id:ebay_client_secret
    """
    ebay_api_key_env = settings.EBAY_API_ENV
    client_id = settings.EBAY_CLIENT_ID_SANDBOX
    client_secret = settings.EBAY_CLIENT_SECRET_SANDBOX

    if ebay_api_key_env == 'production':
        client_id = settings.EBAY_CLIENT_ID_PRODUCTION
        client_secret = settings.EBAY_CLIENT_SECRET_PRODUCTION

    client_creds = ':'.join([client_id, client_secret]).encode('utf-8')
    return base64.b64encode(client_creds).decode('utf-8')


def parse_response(response: dict) -> list[ItemSummary]:
    items = response.get('itemSummaries', [])
    return [ItemSummary.from_dict(item) for item in items]
