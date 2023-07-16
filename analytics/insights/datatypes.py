from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json(letter_case="camel")
@dataclass(frozen=True)
class Image:
    image_url: str


@dataclass(frozen=True)
class Price:
    value: str
    currency: str


@dataclass_json(letter_case="camel")
@dataclass(frozen=True)
class ItemSummary:
    item_id: str
    title: str
    image: Image
    price: Price
    item_web_url: str


@dataclass_json
@dataclass(frozen=True)
class AlertEventPayload:
    id: int
    email: str = field(default="")
    keywords: str = field(default="")
    frequency: int = field(default="2")


@dataclass_json
@dataclass(frozen=True)
class NewProductsEventPayload:
    id: int
    email: str
    keywords: str
    frequency: int
    items: list[ItemSummary] = field(default_factory=list)
