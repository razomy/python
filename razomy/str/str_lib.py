import re


def add_margin_spaces(text: str, left_margin: int):
    margin = (' ' * left_margin)
    return add_margin(text, margin)


def add_margin(text: str, margin):
    lines = text.split('\n')
    shifted_lines = [margin + line for line in lines]
    return '\n'.join(shifted_lines)


def enumerate_lines_list(lines: list[str], start=0, div='. '):
    result = ''
    for ix, i in enumerate(lines):
        result += str(ix + start) + div + i + '\n'
    return result


def enumerate_lines(text: str):
    lines = text.split('\n')
    return enumerate_lines_list(lines)


def find_most_similar_key(obj, key_to_match):
    max_similarity = 0
    most_similar_key = None

    for key in obj:
        similarity = calculate_similarity(key + '_', key_to_match)

        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_key = key

    return most_similar_key


def calculate_similarity(str1: str, str2: str):
    i = 0
    while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
        i += 1
    return i


def string_to_function_name(result_string):
    result_string = result_string.strip()
    result_string = re.sub(r'\s+', '_', result_string)
    result_string = result_string.lower()
    result_string = re.sub(r'[^a-z_:,]', '', result_string)
    return result_string


def try_split_by_dot(path: str or [str]):
    if isinstance(path, list):
        return path
    keys = path.split('.')
    return keys


def short(txt, star_l=13, end_l=3):
    max_l = star_l + end_l
    if len(txt) < max_l:
        return txt
    left = txt[:star_l]
    right = txt[-end_l:]
    return f"{left}_{right}"


def wrap_str_array(left, right, texts: [str]):
    first = left + texts[0]
    last = texts[-1] + right

    texts = [first] + list(texts[1:-1]) + [last]
    return texts
