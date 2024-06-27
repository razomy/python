class WithName:
    name: str


class WithLevel:
    level: int


class WithAnsiColor:
    ansi_color: str


class LogLevel(WithName, WithAnsiColor, WithLevel):
    def __init__(self, name, level, ansi_color):
        self.name = name
        self.level = level
        self.ansi_color = ansi_color
