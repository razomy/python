from razomy.python.fs import size_lib, copy_lib
from razomy.python.fs.copy_lib import copy_pipes
from razomy.python.languages.programming.fs import print_size_lib


class CopyPrintCtx(print_size_lib.PrintCtx, copy_lib.CopyCtx):
  def __init__(self, from_dir_path, to_dir_path):
    self.from_dir_path = from_dir_path
    self.to_dir_path = to_dir_path


copy_print_pipes = print_size_lib.print_size_pipes + size_lib.size_pipes + copy_pipes
