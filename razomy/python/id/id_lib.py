import uuid


def create_id():
    return str(uuid.uuid4())


def create_id_short():
    return create_id()[0:8]


def increment_str(prev_number: str):
    next_number = int(prev_number) + 1
    return str(next_number)


def id_to_title(id_str: str):
    return id_to_text(id_str).title()


def id_to_text(id_str: str):
    return id_str.replace('_', ' ').replace('.', ': ')


def text_to_id(id_str: str):
    return id_str.replace(' ', '_').replace(': ', '.')


def title_to_id(title: str):
    return text_to_id(title).lower()
