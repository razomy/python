from razomy.python.pipes.booleans import execute_lib


def all_[T](ctx: T, nexts: [execute_lib.Execute[T]]):
  for next_ in nexts:
    is_complete = next_(ctx)
    if not is_complete:
      return False
  return True
