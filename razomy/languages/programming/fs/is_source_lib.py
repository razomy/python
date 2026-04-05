from razomy.python.fs import iterate_lib
from razomy.python.languages.programming.fs import is_packages_lib, is_output_lib
from razomy.python.pipes.booleans import execute_lib

is_source_pipes = [
  execute_lib.not_(iterate_lib.is_symbolic_link),
  execute_lib.not_(is_packages_lib.is_in_packages),
  execute_lib.not_(is_output_lib.is_in_output),
]
