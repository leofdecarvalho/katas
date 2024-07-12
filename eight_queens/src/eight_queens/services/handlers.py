from eight_queens.domain import commands, events
from eight_queens.services import unit_of_work
from eight_queens.domain import models
import logging

logger = logging.getLogger(__name__)

def handleSomeCommand(
        cmd: commands.SomeCommand,
        uowManager:  unit_of_work.UOWManager
):
    with uowManager.getUnitOfWork("ConcreteRepository") as uow:
        model = models.ConcreteModel()
        uow.repository.add(model)
        uow.commit()
        
def handleSomeEvent(
        event: events.SomeEvent,
        uowManager:  unit_of_work.UOWManager
):
    with uowManager.getUnitOfWork("ConcreteRepository") as uow:
        logger.info(f"handling event {event}")
        
EVENT_HANDLERS = {
    events.SomeEvent: [handleSomeEvent]
}

COMMAND_HANDLERS = {
    commands.SomeCommand: handleSomeCommand
}