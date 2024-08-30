# region Logger
from razomy.python.units.unit import Unit


class Log:
  logs = {}

  def log(self, m: Unit):
    if not m.name in self.logs:
      self.logs[m.name] = []

    self.logs[m.name].append(m.copy())
