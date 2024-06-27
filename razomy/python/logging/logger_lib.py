from razomy.python.logging import log_level_lib
from razomy.python.logging import print_log_lib
from razomy.python.logging.log_levels_lib import LogLevels
from razomy.python.logging.log_lib import Log


class Logger:
    name: str = None
    stack_path: str = None
    level: LogLevels or int


def create_log(logger: Logger, level: log_level_lib.LogLevel, messages: [str]):
    _log = Log()
    text_messages = ' '.join([str(i) for i in messages])
    _log.message = ''.join([level.ansi_color, text_messages, LogLevels.debug.ansi_color])
    _log.level = level.level
    _log.name = level.name + logger.stack_path + '.' + logger.name
    return _log


def try_print_log(logger: Logger, level: log_level_lib.LogLevel, *messages: [str]):
    if logger.level > level.level:
        return
    return print_log_lib.print_log(create_log(logger, LogLevels.debug, messages))


def debug(logger: Logger, *messages: [str]):
    return try_print_log(logger, LogLevels.debug, messages)


def info(logger: Logger, *messages: [str]):
    return try_print_log(logger, LogLevels.info, messages)


def error(logger: Logger, *messages: [str]):
    return try_print_log(logger, LogLevels.error, messages)
