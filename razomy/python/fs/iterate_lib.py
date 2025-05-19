import typing
import os

from razomy.python.pipes.booleans import execute_lib


class WithFilePath(typing.Protocol):
  file_path: str


class WithIterator(typing.Protocol):
  directories: [str]
  filenames: [str]
  dir_path: str


def get_path_slugs(file_path: str) -> typing.List[str]:
  return os.path.normpath(file_path).split(os.sep)


def is_symbolic_link(ctx: WithFilePath):
  return os.path.islink(ctx.file_path)


def iterate_bool[T:WithIterator and WithFilePath](dir_path, execute_bool: execute_lib.Execute[T], ctx: T):
  for dir_path, directories, filenames in os.walk(dir_path):
    ctx.directories = directories
    ctx.filenames = filenames
    ctx.dir_path = dir_path

    for f in filenames:
      ctx.file_path = str(os.path.join(dir_path, f))

      if execute_bool(ctx):
        continue
      else:
        # todo: break is not processing child files check js impl
        break

  return ctx
