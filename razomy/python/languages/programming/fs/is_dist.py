from razomy.python.fs import size

def is_in_dist(ctx: size.IterateCtx) -> bool:
  return any(element in ctx.file_path for element in ['dist', 'obj', 'out', 'build'])
