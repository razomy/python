
def to_number(value, default_value):
    if value is None:
        return default_value
    try:
        return int(value)
    except ValueError:
        return default_value


primitives = (bool, str, int, float, type(None))


def is_primitive(obj):
    return isinstance(obj, primitives)
