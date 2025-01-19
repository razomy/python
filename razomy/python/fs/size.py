import os
import typing

from razomy.python.exeptions import exeption_lib


class WithTotalSize(typing.Protocol):
  total_size: int


class WithFilePath(typing.Protocol):
  file_path: str


class WithIterator(typing.Protocol):
  directories: [str]
  filenames: [str]
  dir_path: str


def get(file_path: str) -> int:
  try:
    return os.path.getsize(file_path)
  except FileNotFoundError as error:
    raise exeption_lib.ArgumentException(f"File {file_path} not found.", error)


class IterateCtx(WithTotalSize, WithFilePath, WithIterator):
  def __init__(self, total_size: int, path: str):
    self.total_size = total_size
    self.path = path


def add_to_total_size(ctx: IterateCtx):
  ctx.total_size += get(ctx.file_path)


def is_symbolic_link(ctx: IterateCtx):
  return os.path.islink(ctx.file_path)


def iterate_bool(dir_path, execute_bool, ctx: IterateCtx = IterateCtx(0, '')):
  for dir_path, directories, filenames in os.walk(dir_path):
    ctx.directories = directories
    ctx.filenames = filenames
    ctx.dir_path = dir_path

    for f in filenames:
      ctx.file_path = str(os.path.join(dir_path, f))

      if execute_bool(ctx):
        continue
      else:
        break

  return ctx
