from razomy.python.fs import size_lib
from razomy.python.fs import iterate_lib

python_cache = ['__pycache__']
js_angular_cache = ['.angular']
csharp_cache = ['obj']
dart_cache = ['.dart_tool']
dart_firebase_cache = ['.firebase']
known_cache = python_cache + js_angular_cache + csharp_cache + dart_cache + dart_firebase_cache


def is_in_cache(ctx: size_lib.WithFilePath) -> bool:
  path_components = iterate_lib.get_path_slugs(ctx.file_path)
  return any(element in path_components for element in known_cache)
