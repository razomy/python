import time


class Stopwatch:
    def __init__(self):
        self.start_time = time.time()


def reset(self: Stopwatch):
    self.start_time = time.time()


def track_str(self: Stopwatch):
    delta = time.time() - self.start_time
    return "Track: %s seconds." % delta
