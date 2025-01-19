from typing import List, Callable

type Execute[I,O] = Callable[[I], O]

def execute(arr: List[Callable[[], None]]):
  for fn in arr:
    fn()


def execute_ctx[T](arr: List[Callable[[T], None]], ctx: T):
  for fn in arr:
    fn(ctx)
