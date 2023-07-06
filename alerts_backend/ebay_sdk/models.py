from dataclasses import dataclass, field
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
    price: Price = field(default_factory=lambda: Price(currency='', value=0.0))
    image: Image = field(default_factory=lambda: Image(image_url=''))
