from razomy.python.byte_ import print_lib
from razomy.python.fs import size_lib
from razomy.python.fs import iterate_lib
from razomy.python.languages.programming.fs import is_source_lib
from razomy.python.logging import print_class
from razomy.python.pipes.booleans import all_lib

print_size_pipes = is_source_lib.is_source_pipes + size_lib.size_pipes


class PrintCtx(size_lib.WithTotalSize, size_lib.WithFilePath, iterate_lib.WithIterator):
  pass


def print_size(dir_path: str, pipes=print_size_pipes, ctx=PrintCtx()):
  ctx = iterate_lib.iterate_bool(dir_path, lambda c: all_lib.all_(c, pipes), ctx)
  print(print_lib.print_bytes(ctx.total_size))
  print_class.print_class(ctx)
