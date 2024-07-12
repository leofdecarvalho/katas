# pylint: disable=too-few-public-methods
from dataclasses import dataclass, field

class Command:
    pass

@dataclass
class SomeCommand(Command):
    someField: str = None