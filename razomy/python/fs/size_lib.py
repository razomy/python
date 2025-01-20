import os
import typing

from razomy.python.exeptions import exeption_lib
from razomy.python.fs.iterate_lib import WithFilePath
from razomy.python.pipes.booleans import execute_lib


class WithTotalSize(typing.Protocol):
  total_size: int = 0


def get(file_path: str) -> int:
  try:
    return os.path.getsize(file_path)
  except FileNotFoundError as error:
    raise exeption_lib.ArgumentException(f"File {file_path} not found.", error)


def add_to_total_size(ctx: WithTotalSize and WithFilePath):
  ctx.total_size += get(ctx.file_path)


size_pipes = [
  execute_lib.result(add_to_total_size, True),
]
