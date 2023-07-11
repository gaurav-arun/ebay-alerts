import base64

from django.conf import settings

from .models import ItemSummary


def get_base_url():
    """
    Returns the base url for the ebay api based on the environment
    """
    if settings.EBAY_API_ENV == "production":
        return "https://api.ebay.com"
    elif settings.EBAY_API_ENV == "sandbox":
        return "https://api.sandbox.ebay.com"
    elif settings.EBAY_API_ENV == "mock":
        return settings.EBAY_MOCK_SERVER_URL

    raise ValueError("EBAY_API_ENV is should be one of production, sandbox, or mock")


def get_encoded_oauth_basic_token() -> str:
    """
    Returns the base64 encoded string of ebay_client_id:ebay_client_secret
    """
    ebay_api_key_env = settings.EBAY_API_ENV
    client_id = settings.EBAY_CLIENT_ID_SANDBOX
    client_secret = settings.EBAY_CLIENT_SECRET_SANDBOX

    if ebay_api_key_env == "production":
        client_id = settings.EBAY_CLIENT_ID_PRODUCTION
        client_secret = settings.EBAY_CLIENT_SECRET_PRODUCTION

    if not client_id or not client_secret:
        raise ValueError(
            "EBAY_CLIENT_ID_<SANDBOX|PRODUCTION> and "
            "EBAY_CLIENT_SECRET_<SANDBOX|PRODUCTION> must be set in .env"
        )

    client_creds = ":".join([client_id, client_secret]).encode("utf-8")
    return base64.b64encode(client_creds).decode("utf-8")


def parse_response(
    response: dict, skip_items_without_price: bool = True
) -> list[ItemSummary]:
    item_summaries = response.get("itemSummaries", [])
    items = [ItemSummary.from_dict(item_summary) for item_summary in item_summaries]

    if skip_items_without_price:
        items = [item for item in items if item.price.currency and item.price.value]

    # Sort by price
    items.sort(key=lambda item: item.price.value)

    return items
