from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth.models import User
from .authentication import ClientCredentialsAuthentication
from .serializers import AccessTokenSerializer
import secrets
import random
import re
from decimal import Decimal


class ClientCredentials(APIView):
    """
    View to acquire an application access token.
    """
    authentication_classes = [ClientCredentialsAuthentication]

    def post(self, request, format=None):
        response = {
            "access_token": f"v^1.1#i^1#p^3#r^1#{secrets.token_urlsafe(32)}",
            "expires_in": 120,
            "token_type": "Application Access Token"
        }
        serializer = AccessTokenSerializer(data=response)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


sample_response = {
    "href": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3&offset=0",
    "total": 260202,
    "next": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3&offset=3",
    "limit": 20,
    "offset": 0,
    "itemSummaries": [
        {
            "itemId": "v1|1**********1|0",
            "title": "Syma X5SW-V3 Wifi FPV RC Drone Quadcopter 2.4Ghz 6-Axis Gyro with Headless Mode",
            "price": {
                "value": "59.99",
                "currency": "USD"
            },
            "buyingOptions": [
                "FIXED_PRICE",
                "BEST_OFFER"
            ],
            "listingMarketplaceId": "EBAY_US"
        },
        {
            "itemId": "v1|3**********8|0",
            "title": "2022 New RC Drone 4k HD Wide Angle Camera WIFI FPV Foldable Camera Quadcopter US",
            "price": {
                "value": "46.99",
                "currency": "USD"
            },
            "buyingOptions": [
                "FIXED_PRICE",
                "BEST_OFFER"
            ],
            "listingMarketplaceId": "EBAY_US"
        },
        {
            "itemId": "v1|3**********1|0",
            "title": "WiFi FPV RC Drone with 4K HD Camera, 40 Mins Flight Time, Foldable Drone",
            "price": {
                "value": "49.99",
                "currency": "USD"
            },
            "buyingOptions": [
                "FIXED_PRICE"
            ],
            "listingMarketplaceId": "EBAY_US"
        }
    ]
}


class BuyAPI(APIView):
    @classmethod
    def _generate_random_numbers(cls, lower_bound=None, upper_bound=None, sample_size=20) -> list[int]:
        if not lower_bound:
            lower_bound = 1

        if not upper_bound:
            upper_bound = lower_bound + sample_size + (sample_size//2)

        return random.sample(range(lower_bound, upper_bound + 1), sample_size)

    @classmethod
    def _sanitize_search_phrase(cls, search_phrase: str) -> str:
        # Remove special characters (keep only alphabets, space, and underscore)
        sanitized_phrase = re.sub(r'[^a-zA-Z _]', '', search_phrase)

        # Trim the phrase and replace multiple spaces with a single underscore
        sanitized_phrase = re.sub(r'\s+', ' ', sanitized_phrase).strip().replace(' ', '_')

        return sanitized_phrase.lower()

    def _get_item_title(self, search_phrase, id:int) -> str:
        search_phrase = self._sanitize_search_phrase(search_phrase)
        product_id = '_'.join([search_phrase, str(id)])
        return product_id

    @classmethod
    def _get_item_price(cls, lowest_price=10, highest_price=1000) -> str:
        return str(random.randint(lowest_price, highest_price))

    def generate_items(self, search_phrase, sample_size=20):
        products = []
        random_ids = self._generate_random_numbers(sample_size=sample_size)
        for id in random_ids:
            title = self._get_item_title(search_phrase=search_phrase, id=id),
            product = {
                "itemId": '|'.join(['v1', title, '0']),
                "title": title,
                "price": {
                    "value": self._get_item_price(),
                    "currency": "USD"
                },
            }
            products.append(product)

        # Sort products by price
        products_sorted_by_price = sorted(products, key=lambda product: Decimal(product["price"]["value"]))

        return products_sorted_by_price

    def get(self, request, format=None):
        q = request.query_params.get('q')
        data = {
            "href": f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={q}&limit=20&offset=0&sort=-price",
            "total": 260202,
            "next": f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={q}&limit=20&offset=20=-price&sort=-price",
            "limit": 20,
            "offset": 0,
            "itemSummaries": self.generate_items(search_phrase=q)
        }
        return Response(data=data, status=status.HTTP_200_OK)
