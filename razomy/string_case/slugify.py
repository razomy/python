import unicodedata
import re

def slugify(text: str) -> str:
    """
    Converts a given string into a URL-friendly slug by normalizing unicode characters
    (removing diacritics/accents), converting to lowercase, replacing non-alphanumeric
    characters with hyphens, and trimming leading/trailing hyphens.

    Args:
        text: The text to slugify.

    Returns:
        The slugified string.

    Examples:
        >>> slugify('Hello World')
        'hello-world'
        >>> slugify('Foo & Bar')
        'foo-bar'
        >>> slugify('Crème Brûlée')
        'creme-brulee'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text