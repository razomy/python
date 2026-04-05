from razomy.python.logging import log_lib
from razomy.python.logging import log_levels_lib


def print_log(log: log_lib.Log):
    print(log.name, log.message, flush=True)
