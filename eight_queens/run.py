from eight_queens.bootstrap  import initBus
from eight_queens.domain import commands
from eight_queens.config import dictConfig
import logging
logger = logging.getLogger(__name__)

bus = initBus()

logger.info(f"Running some command eight_queens")
bus.handle(commands.SomeCommand(someField="x"))
