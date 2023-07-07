from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime


@dataclass_json
@dataclass
class Event:
    type: str
    payload: dict
    timestamp: datetime = field(default_factory=datetime.now)
