class TerminalColors:
    GREEN = '\033[32m'
    RED = '\033[91m'
    END = '\033[0m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def green_wrap(message: str):
    return TerminalColors.GREEN + message + TerminalColors.END
