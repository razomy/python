from razomy.python.logging import logger_lib
from razomy.python.logging.logger_lib import Logger


class StackLoggerEntity:
    nodes: [Logger]

    def __init__(self, root_logger: Logger):
        self.loggers = [root_logger]


class StackLogger(StackLoggerEntity):
    def last(self):
        return self.loggers[-1]

    def get_stack_path(self):
        stack_paths = [i.name for i in self.loggers]
        path = '.'.join(stack_paths)
        return path

    def info(self, *messages):
        return logger_lib.info(self.last(), *messages)

    def error(self, *messages):
        return logger_lib.error(self.last(), *messages)

    def debug(self, *messages):
        return logger_lib.debug(self.last(), *messages)

    def create(self, name: str):
        create_logger(self, name)
        return self

    def destroy(self, name: str):
        destroy_logger(self, name)
        return self


def create_logger(self: StackLogger, name: str):
    logger = Logger()
    logger.name = name
    logger.stack_path = self.get_stack_path()
    logger.level = self.last().level
    self.loggers.append(logger)
    return logger


def destroy_logger(self: StackLogger, name: str):
    if name != self.last():
        assert 'Logger not closed!'
    self.loggers.pop()
