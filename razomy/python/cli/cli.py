import importlib
import inspect

from razomy.python.key.assign import assign


async def cli(terminal_args):
  print('razomy:python:cli:start')

  rootpath = terminal_args[0]
  key_name = str.split(rootpath, assign)[-1]
  value_arguments = terminal_args[1:]

  module_name = 'razomy.python' + rootpath.replace(assign, '.')
  package_impl = importlib.import_module(module_name)
  result = getattr(package_impl, key_name)(*value_arguments)

  if inspect.iscoroutinefunction(result):
    await result

  print('razomy:python:cli:finish')
  return result
