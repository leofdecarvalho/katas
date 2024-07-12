import abc
from typing import Set

class AbstractRepository(abc.ABC):
    
    def __init__(self, session):
        self.seen = set() # type: Set
        self.session = session
        
    def add(self, model):
        self._add(model)
        self.seen.add(model)
    
    def remove(self, model):
        self._remove(model)
        self.seen.add(model)
        
    @abc.abstractmethod
    def _add(self, model):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _remove(self, model):
        raise NotImplementedError
    
    
class ConcreteRepository(AbstractRepository):
    
    def __init__(self, session):
        super().__init__(session)
        
    def _add(self, model):
        pass
    
    def _remove(self, model):
        pass
    
    def get_something(self, someParam: str):
        pass        