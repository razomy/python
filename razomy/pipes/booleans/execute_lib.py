from razomy.python.pipes import execute_lib

type Execute[I] = execute_lib.Execute[I, bool]


def result[T](next_: execute_lib.Execute[T, any], result_: bool):
  def true_fn(ctx: T):
    next_(ctx)
    return result_

  return true_fn


def map_[T](next_: execute_lib.Execute[T, any], true_then_result: bool = True, false_then_result: bool = False):
  def map_fn(ctx: T):
    if next_(ctx):
      return true_then_result
    return false_then_result

  return map_fn


def not_[T](next_: execute_lib.Execute[T, any]):
  return map_(next_, true_then_result=False, false_then_result=True)
