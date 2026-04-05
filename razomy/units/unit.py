from razomy.python.number.string.string import string


class Unit:
  def __init__(self, value: float, type: str):
    self.value = value
    self.name = type

  def copy(self):
    return Unit(self.value, self.name)

  def __str__(self):
    return print_unit(self)


def print_unit(m: Unit):
  return m.name + ':' + string(m.value)
