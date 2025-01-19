from razomy.python.pipes.booleans import execute_lib


def any_[T](ctx: T, nexts: [execute_lib.Execute[T]]):
  for next_ in nexts:
    is_complete = next_(ctx)
    if is_complete:
      return True
  return False
