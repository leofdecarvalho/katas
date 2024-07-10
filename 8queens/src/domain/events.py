# pylint: disable=too-few-public-methods
from dataclasses import dataclass, field

class Event:
    pass

@dataclass
class SomeEvent(Event):
    someField: str