from __future__ import annotations
from uuid import uuid4
import logging

from eight_queens.domain.events import BatchEvent
from eight_queens.adapter.repository import AbstractRepository
from eight_queens.adapter import repository

logger = logging.getLogger(__name__)

class Session:
    
    def __init__(self, sessionId):
        self.sessionId = sessionId
        logger.info(f'Session {self.sessionId} started.')
    
    def commit(self):
        logger.info(f'Session {self.sessionId} committed.')
        
    def close(self):
        logger.info(f'Session {self.sessionId} closed.')
        
    def __repr__(self):
        return f"<Session id: {self.sessionId}>"

    def __eq__(self, other):
        if not isinstance(other, Session):
            return False
        return other.sessionId == self.sessionId

    def __hash__(self):
        return hash(self.sessionId.__hash__())

class UOWFactory:
    
    def generate_id(self):
        return str(uuid4())
    
    def getUOW(self, className: str) -> UnitOfWork:
        id = self.generate_id()
        session = Session(id)
        return UnitOfWork(session=session, repository=self.getRepositoryClass(className)(session), id=id) 

    def getRepositoryClass(self, className):
        return getattr(repository, className)   

class UnitOfWork:

    def __init__(self, session, repository, id):
        self.session = session
        self.repository = repository # type: AbstractRepository
        self.uowId = id
    
    def generate_uow_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"<UOW id: {self.uowId}>"

    def __eq__(self, other):
        if not isinstance(other, UnitOfWork):
            return False
        return other.uowId == self.uowId

    def __hash__(self):
        return hash(self.uowId.__hash__())
    
    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        self._close()
        
    def _close(self):
        self.session.close()
        
    
    def commit(self):
        self.session.commit()
        
        
class UOWManager:
    singleEvent: bool = True
    uows: set[UnitOfWork]
    
    def __init__(self):
        self.uows = set[UnitOfWork]()
        self.uowFactory = UOWFactory()
    
    def getUnitOfWork(self, className: str) -> UnitOfWork:
        uow = self.uowFactory.getUOW(className=className)
        self.uows.add(uow)
        return uow
    
    def _getEvent(self, model):

        if self.singleEvent:
            return self._getSingleEvent(model)
        else:
            return self._getBatchEvent(model)

    def _getBatchEvent(self, model):
        length = len(model.events)
        result = []
        for _ in range(length):
            result.append(model.events.pop(0))
        return BatchEvent(events=result)

    def _getSingleEvent(self, model):
        return model.events.pop(0)

    def collectNewEvents(self):
        uowsToCollectEvents = [uow for uow in self.uows]
        for uow in uowsToCollectEvents:
            for model in uow.repository.seen:
                while model.events:
                    yield self._getEvent(model)
        
        self._cleanUows(uowsToCollectEvents)
        
    def _cleanUows(self, uowsCollected):
        for uow in uowsCollected:
            self.uows.remove(uow)
            
            

