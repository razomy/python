import os
from razomy.python.byte_ import print_lib
from razomy.python.fs import size
from razomy.python.logging import print_class
from razomy.python.pipes.booleans import execute_lib, all_lib
from razomy.python.languages.programming.fs import is_dist, is_packages
import shutil


def copy_f(from_dir_path, to_dir_path):
  def copy(ctx: size.IterateCtx):
    print(ctx.file_path)
    new_file_path = ctx.file_path.replace(from_dir_path, to_dir_path)
    dir_path = os.path.dirname(new_file_path)
    if not os.path.isdir(dir_path):
      os.makedirs(dir_path)
    shutil.copy2(ctx.file_path, new_file_path)

  return copy


def copy(dir_path: str, to_path: str):
  def get_size_pipe(ctx: size.IterateCtx):
    return all_lib.all_(ctx, [
      execute_lib.not_(size.is_symbolic_link),
      execute_lib.not_(is_packages.is_in_packages),
      execute_lib.not_(is_dist.is_in_dist),
      execute_lib.result(size.add_to_total_size, True),
      execute_lib.result(copy_f(dir_path, to_path), True),
    ])

  ctx = size.iterate_bool(dir_path, get_size_pipe)
  print(print_lib.print_bytes(ctx.total_size))
  print_class.print_class(ctx)
