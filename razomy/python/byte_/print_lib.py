def print_bytes(size_in_bytes: int):
  """
  Converts a size in bytes to a human-readable string with subtypes (e.g., GB, MB, KB, B).
  """
  units = [("TB", 1024 ** 4), ("GB", 1024 ** 3), ("MB", 1024 ** 2), ("KB", 1024), ("B", 1)]
  result = []

  for unit, factor in units:
    value = size_in_bytes // factor
    if value > 0:
      result.append(f"{value}{unit}")
      size_in_bytes %= factor

  return ".".join(result)
