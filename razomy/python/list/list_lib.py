import typing


def get_from_list(data, path, default_fn, nesting_with='.'):
    keys = path.split(nesting_with)
    current = data

    for key in keys:
        current = next((v for (k, v) in current if k == key), None)
        if current is None:
            return None

    return current or default_fn()


def after[T](data: [T], condition: typing.Callable[[T], bool]) -> T or None:
    is_next = False
    for i in data:
        if is_next:
            return i
        if condition(i):
            is_next = True
    return None


def merge_list(*dicts: list[[str, str] or None]):
    result = []
    for d in dicts:
        if d is None:
            continue
        for key, value in d:
            result.append([key, value])
    return result
