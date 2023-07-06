from django.conf import settings
import requests
from django.core.cache import cache
from django.conf import settings
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import logging
import base64
from dataclasses_json import LetterCase, config, dataclass_json


@dataclass_json
@dataclass
class AccessToken:
    access_token: str
    token_type: str
    expires_in: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Image:
    image_url: str


@dataclass_json
@dataclass
class Price:
    currency: str
    value: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ItemSummary:
    item_id: str
    title: str
    price: Price
    image: Image
