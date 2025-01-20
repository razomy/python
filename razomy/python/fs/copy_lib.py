import os
import shutil
from razomy.python.fs import iterate_lib
from razomy.python.pipes.booleans import execute_lib


class CopyCtx:
  from_dir_path: str
  to_dir_path: str


def copy(from_dir_path: str, to_dir_path: str, file_path: str):
  new_file_path = file_path.replace(from_dir_path, to_dir_path)
  dir_path = os.path.dirname(new_file_path)
  if not os.path.isdir(dir_path):
    os.makedirs(dir_path)
  shutil.copy2(file_path, new_file_path)


def copy_p(ctx: CopyCtx and iterate_lib.WithFilePath):
  copy(ctx.from_dir_path, ctx.to_dir_path, ctx.file_path)


copy_pipes = [
  execute_lib.result(copy_p, True),
]
