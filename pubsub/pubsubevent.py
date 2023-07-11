from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from dataclasses_json import dataclass_json


class PubSubEventType(Enum):
    ALERT_CREATED = "alert-created"
    ALERT_UPDATED = "alert-updated"
    ALERT_DELETED = "alert-deleted"
    NEW_PRODUCTS = "new-products"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


@dataclass_json
@dataclass
class PubSubEvent:
    type: PubSubEventType
    payload: dict
    timestamp: datetime = field(default_factory=datetime.now)
