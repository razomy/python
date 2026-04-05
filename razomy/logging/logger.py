from razomy.python.logging import logger_lib
from razomy.python.logging.log_levels_lib import LogLevels
from razomy.python.logging import stack_logger_lib

logger = logger_lib.Logger()
logger.level = LogLevels.debug.level
logger.name = ''
logger.stack_path = ''
stack_logger = stack_logger_lib.StackLogger(logger)

info = stack_logger.info
error = stack_logger.error
debug = stack_logger.debug
create = stack_logger.create
destroy = stack_logger.destroy
