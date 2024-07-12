from kata_template.bootstrap  import initBus
from kata_template.domain import commands
from kata_template.config import dictConfig
import logging
logger = logging.getLogger(__name__)

bus = initBus()

logger.info(f"Running some command kata-template")
bus.handle(commands.SomeCommand(someField="x"))
