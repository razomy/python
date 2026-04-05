from razomy.python.pipes.booleans import execute_lib


def while_[T](ctx: T, next_: execute_lib.Execute[T]):
  while next_(ctx):
    pass
  return True
