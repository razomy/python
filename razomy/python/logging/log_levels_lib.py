from razomy.python.exeptions import exeption_lib
from razomy.python.logging import log_level_lib
from razomy.python.terminal import terminal_color_lib


class LogLevels:
    debug = log_level_lib.LogLevel('DEBUG', 0, terminal_color_lib.TerminalColors.END)
    info = log_level_lib.LogLevel('INFO', 1, terminal_color_lib.TerminalColors.BLUE)
    error = log_level_lib.LogLevel('ERROR', 2, terminal_color_lib.TerminalColors.RED)
