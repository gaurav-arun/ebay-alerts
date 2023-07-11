import requests

from . import constants as ebay_constants
from . import utils as ebay_utils
from .auth import Auth


class BuyApi:
    URL = ebay_utils.get_base_url() + "/buy/browse/v1/item_summary/search"

    @classmethod
    def find_items_by_keyword(
        cls,
        keyword: str,
        offset: int = 0,
        limit: int = 20,
        sort_by: str | None = None,
        marketplace_id: str = "EBAY_US",
        refresh_token=False,
    ) -> dict:
        auth_token = Auth.get_token(
            ebay_constants.API_CLIENT_CACHE_KEY_MAP["find_items_by_keyword"],
            force_token_refresh=refresh_token,
        )

        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": marketplace_id,
            # TODO: Add X-EBAY-C-ENDUSERCTX
        }

        params = {
            "q": keyword,
            "limit": limit,
            "offset": offset,
        }

        if sort_by:
            params["sort"] = sort_by

        response = requests.get(cls.URL, headers=headers, params=params)
        response.raise_for_status()

        return response.json()
