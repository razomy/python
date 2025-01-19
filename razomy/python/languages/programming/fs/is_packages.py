from razomy.python.fs import size

def is_in_packages(ctx: size.IterateCtx) -> bool:
  return any(element in ctx.file_path for element in ['venv', 'node_modules', 'Library'])
