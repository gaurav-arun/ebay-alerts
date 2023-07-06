import requests
from django.core.cache import cache
from . import utils as ebay_utils
from .models import AccessToken


class Auth:
    URL = ebay_utils.get_base_url() + '/identity/v1/oauth2/token'

    # The token expires in 7200 seconds,
    # but we want to cache it for a little less than that
    REDUCE_EXPIRATION_TIME_BY = 60

    @classmethod
    def _cache_token(cls, key: str, value: str, timeout: int):
        cache.set(key=key, value=value, timeout=timeout)

    @classmethod
    def get_token(cls, api_key: str) -> str:
        token = cache.get(api_key)

        if token is None:
            access_token: AccessToken = cls._get_new_token()
            cls._cache_token(key=api_key, value=access_token.access_token, timeout=access_token.expires_in - cls.REDUCE_EXPIRATION_TIME_BY)
            token = access_token.access_token

        return token

    @classmethod
    def _get_new_token(cls) -> AccessToken:
        data = {
            'grant_type': 'client_credentials',
            'scope': 'https://api.ebay.com/oauth/api_scope',
        }

        token = ebay_utils.get_encoded_oauth_basic_token()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {token}',
        }
        response = requests.post(cls.URL, data=data, headers=headers)
        response.raise_for_status()

        return AccessToken.from_dict(response.json())
