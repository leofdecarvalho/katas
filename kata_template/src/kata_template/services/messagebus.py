# pylint: disable=broad-except, attribute-defined-outside-init
from __future__ import annotations
import logging
from typing import Callable, Dict, List, Union, Type
from kata_template.domain import commands, events
from kata_template.services import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]
class MessageBus:
    def __init__(
        self,
        uowManager: unit_of_work.UOWManager,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],      
    ):
        self.uowManager = uowManager
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self.uowManager.collectNewEvents())
            except Exception as e:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uowManager.collectNewEvents())
        except Exception as e:
            logger.exception("Exception handling command %s", command)
            raise
