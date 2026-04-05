import re


def set_to_dict(data, path: str, value, merge=False):
    keys = path.split('.')
    root = data
    current = data

    for key in keys[:-1]:
        current = current.setdefault(key, {})

    key = keys[-1]
    if current.get(key, False) and merge:
        current[key] += value
    else:
        current[key] = value
    return root


def parse_start_caret_equal(input_str: str):
    if input_str[0] != '.':
        input_str = '.' + input_str
    result = {}
    pattern = re.compile(r'\.(.*?):(.*?)(?=\n\.|$)', re.DOTALL)
    matches = pattern.findall(input_str)

    for match in matches:
        tool_name = match[0].strip()
        arg_name = match[1].strip() if match[1] else None
        result = set_to_dict(result, tool_name, arg_name, True)

    return result


def get_from_dict(data: dict, path: str, default_fn=None, nesting_with='.'):
    keys = path.split(nesting_with)
    current = data

    for key in keys:
        current = current.get(key) or None
        if current is None:
            break

    return current or default_fn()


def get_from_dict_data_and_path_tail(data: dict, path: str, nesting_with='.'):
    keys = path.split(nesting_with)
    current = data

    i = 0
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current.get(key)
            i += 1
        else:
            break

    path_tail = str.join('.', keys[i:])
    return current, path_tail


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}"
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def interpolate_value_with_dict(data: list, with_data: dict = None):
    if isinstance(data, list):
        data = [interpolate_value_with_dict(d, with_data) for d in data]
        return data

    elif isinstance(data, str):
        return interpolate_from_str_with_dict(data, with_data)

    return data


def interpolate_from_str_with_dict(data: str, with_data: dict = None):
    if not with_data:
        return data
    flatted = flatten_dict(with_data)
    if with_data is not None:
        for key, value in flatted.items():
            data = str.replace(data, key, str(value))

    return data.replace("' ", '')


def merge_dict(*dicts: dict or None):
    result = {}
    for d in dicts:
        if d is None:
            continue
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dict(result[key], value)
            else:
                result[key] = value or result.get(key)
    return result


def group_by(data: list[dict], key: str):
    grouped_data = {}

    # Loop through each item in the data
    for item in data:
        category = item[key]

        # If the category doesn't exist in the grouped_data, create a list for it
        if category not in grouped_data:
            grouped_data[category] = []

        # Append the current item to the list for its category
        grouped_data[category].append(item)
    return grouped_data


def get_by_key_or_default(array: list, key: str, value: str):
    for item in array:
        if item.get(key) == value:
            return item
    return None
