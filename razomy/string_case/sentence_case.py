import re

def sentence_case(text: str) -> str:
    """
    Converts a string to Sentence case.

    Only the first letter of the result is capitalized, the rest is lowercase.

    Args:
        text (str): The text to convert.

    Returns:
        str: The sentence cased string.

    Examples:
        >>> sentence_case('helloWorld')
        'Hello world'
        >>> sentence_case('HELLO WORLD')
        'Hello world'
        >>> sentence_case('foo_bar_baz')
        'Foo bar baz'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    cleaned_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    cleaned_text = re.sub(r'[^a-zA-Z0-9]+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip().lower()

    if not cleaned_text:
        return ""

    return cleaned_text[0].upper() + cleaned_text[1:]