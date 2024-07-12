import inspect
from kata_template.services import handlers, messagebus, unit_of_work
import logging

logger = logging.getLogger(__name__)

def initBus(
    uowManager: unit_of_work.UOWManager = unit_of_work.UOWManager()
) -> messagebus.MessageBus:
    
    dependencies = {"uowManager": uowManager}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uowManager=uowManager,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
