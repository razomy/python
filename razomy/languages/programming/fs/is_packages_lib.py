from razomy.python.fs import size_lib
from razomy.python.fs import iterate_lib

python_dependencies = ['venv']
nodejs_dependencies = ['node_modules']
unity_dependencies = ['Library']
known_dependencies = python_dependencies + nodejs_dependencies + unity_dependencies


def is_in_packages(ctx: size_lib.WithFilePath) -> bool:
  path_components = iterate_lib.get_path_slugs(ctx.file_path)
  return any(element in path_components for element in known_dependencies)
