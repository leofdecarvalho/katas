import abc
from dataclasses import dataclass, field
from eight_queens.domain.events import Event, SomeEvent

class Model(abc.ABC):
    def __init__(self):
        self.events = list[Event]()

class ConcreteModel(Model):
    someField: str
    
    def __init__(self):
        super().__init__()
        self.someField = "Y"
        self.events.append(SomeEvent(someField=self.someField))
    
    def __repr__(self):
        return f"<ConcreteModel: {self.someField}>"

    def __eq__(self, other):
        if not isinstance(other, ConcreteModel):
            return False
        return other.someField == self.someField

    def __hash__(self):
        return hash(f'{self.someField}')