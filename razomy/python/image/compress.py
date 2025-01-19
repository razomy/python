from PIL import Image
from razomy.python.byte_ import print_lib
from razomy.python.fs import size
from razomy.python.logging import print_class
from razomy.python.pipes.booleans import execute_lib, all_lib
from razomy.python.languages.programming.fs import is_dist, is_packages


def is_image(ctx: size.IterateCtx):
  return ctx.file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))


def get_size_pipe(ctx: size.IterateCtx):
  return all_lib.all_(ctx, [
    execute_lib.not_(size.is_symbolic_link),
    execute_lib.not_(is_packages.is_in_packages),
    execute_lib.not_(is_dist.is_in_dist),
    execute_lib.result(size.add_to_total_size, True),
    is_image,
    execute_lib.result(compress, True),
  ])


def print_compress(dir_path: str):
  ctx = size.iterate_bool(dir_path, get_size_pipe)
  print(print_lib.print_bytes(ctx.total_size))
  print_class.print_class(ctx)


def compress(ctx):
  try:
    with Image.open(ctx.file_path) as img:
      img.save(ctx.file_path, optimize=True, quality=85)
  except Exception as e:
    print(f"Error processing {ctx.file_path}: {e}")
