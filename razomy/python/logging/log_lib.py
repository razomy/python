from razomy.python.logging import log_level_lib


class WithName:
    name: str


class WithMessage:
    message: str


class Log(WithName, log_level_lib.WithLevel, WithMessage):
    pass
