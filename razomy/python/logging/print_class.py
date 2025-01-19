import json


def print_class(string: str):
  print(json.dumps(vars(string), indent=2))
