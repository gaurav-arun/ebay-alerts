import random
import re
import secrets
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import ClientCredentialsAuthentication
from .serializers import AccessTokenSerializer


class ClientCredentials(APIView):
    """
    View to acquire an application access token.
    """

    authentication_classes = [ClientCredentialsAuthentication]

    def post(self, request, format=None):
        response = {
            "access_token": f"v^1.1#i^1#p^3#r^1#{secrets.token_urlsafe(32)}",
            "expires_in": 120,
            "token_type": "Application Access Token",
        }
        serializer = AccessTokenSerializer(data=response)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyAPI(APIView):
    @classmethod
    def _generate_random_numbers(
        cls, lower_bound=None, upper_bound=None, sample_size=20
    ) -> list[int]:
        if not lower_bound:
            lower_bound = 1

        if not upper_bound:
            upper_bound = lower_bound + sample_size + (sample_size // 2)

        return random.sample(range(lower_bound, upper_bound + 1), sample_size)

    @classmethod
    def _sanitize_search_phrase(cls, search_phrase: str) -> str:
        # Remove special characters (keep only alphabets, space, and underscore)
        sanitized_phrase = re.sub(r"[^a-zA-Z _]", "", search_phrase)

        # Trim the phrase and replace multiple spaces with a single underscore
        sanitized_phrase = (
            re.sub(r"\s+", " ", sanitized_phrase).strip().replace(" ", "_")
        )

        return sanitized_phrase.lower()

    def _get_item_title(self, search_phrase, id: int) -> str:
        search_phrase = self._sanitize_search_phrase(search_phrase)
        product_id = "_".join([search_phrase, str(id)])
        return product_id

    @classmethod
    def _get_item_price(cls, lowest_price=10, highest_price=1000) -> str:
        return str(random.randint(lowest_price, highest_price))

    def generate_items(self, search_phrase, sample_size=20):
        products = []
        random_ids = self._generate_random_numbers(sample_size=sample_size)
        for id in random_ids:
            title = (self._get_item_title(search_phrase=search_phrase, id=id),)
            product = {
                "itemId": "|".join(["v1", title, "0"]),
                "title": title,
                "price": {"value": self._get_item_price(), "currency": "USD"},
            }
            products.append(product)

        # Sort products by price
        products_sorted_by_price = sorted(
            products, key=lambda product: Decimal(product["price"]["value"])
        )

        return products_sorted_by_price

    def get(self, request, format=None):
        q = request.query_params.get("q")
        limit = request.query_params.get("limit", 20)
        data = {
            "href": f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={q}&limit={limit}&offset=0&sort=-price",
            "total": 260202,
            "next": f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={q}&limit={limit}&offset=20=-price&sort=-price",
            "limit": 20,
            "offset": 0,
            "itemSummaries": self.generate_items(
                search_phrase=q, sample_size=int(limit)
            ),
        }
        return Response(data=data, status=status.HTTP_200_OK)
