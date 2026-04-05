from PIL import Image
from razomy.python.fs import iterate_lib
from razomy.python.pipes.booleans import execute_lib


def is_image(ctx: iterate_lib.WithFilePath):
  return ctx.file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))


def compress(ctx: iterate_lib.WithFilePath):
  try:
    with Image.open(ctx.file_path) as img:
      img.save(ctx.file_path, optimize=True, quality=85)
  except Exception as e:
    print(f"Error processing {ctx.file_path}: {e}")


compress_pipes = [
  is_image,
  execute_lib.result(compress, True),
]
