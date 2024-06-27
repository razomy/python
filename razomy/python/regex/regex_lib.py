import re


def shield(text, letter, search=None):
    if search is None:
        search = letter
    return re.sub(rf'(?<!\\){search}', f'\\{letter}', text, flags=re.RegexFlag.MULTILINE)


def test_shield():
    assert shield("'", "'") == r"\'"
    assert shield(r"\'", "'") == r"\'"
    assert shield(r"\\'", "'") == r"\\'"
    assert shield(r"#", "#") == r"\#"
    assert shield(r"#", "#", '^#') == r"\#"
