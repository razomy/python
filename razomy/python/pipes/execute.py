from typing import List, Callable, TypeVar


def execute(arr: List[Callable[[], None]]):
  for fn in arr:
    fn()

