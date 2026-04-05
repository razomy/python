from razomy.python.fs import size_lib
from razomy.python.fs import iterate_lib

js_output = ['dist']
java_output = ['out']
python_output = ['build']
rust_output = ['target']
razomy_output = ['release', 'releases']
known_output = js_output + java_output + python_output + rust_output + razomy_output


def is_in_output(ctx: size_lib.WithFilePath) -> bool:
  path_components = iterate_lib.get_path_slugs(ctx.file_path)
  return any(element in path_components for element in known_output)
