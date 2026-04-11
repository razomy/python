import re

def snake_case(text: str) -> str:
    """
    Converts a given string to snake_case format.

    Converts a string to snake_case by handling acronyms, camelCase,
    letter-to-number and number-to-letter boundaries, and replacing common delimiters
    (spaces, hyphens, dots) with underscores. The result is trimmed of leading/trailing
    underscores and converted to lowercase.

    Args:
        text (str): The string to convert.

    Returns:
        str: The snake cased string.

    Examples:
        >>> snake_case('fooBar')
        'foo_bar'
        >>> snake_case('Foo Bar')
        'foo_bar'
        >>> snake_case('FOO-BAR')
        'foo_bar'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # 1. Handle Acronyms: 'JSONData' -> 'JSON_Data'
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1_\2', text)

    # 2. Handle CamelCase: 'camelCase' -> 'camel_Case'
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)

    # 3. Handle Letters to Numbers: 'version2' -> 'version_2'
    text = re.sub(r'([a-zA-Z])([0-9])', r'\1_\2', text)

    # 4. Handle Numbers to Letters: '2beta' -> '2_beta'
    text = re.sub(r'([0-9])([a-zA-Z])', r'\1_\2', text)

    # 5. Replace delimiters (spaces, hyphens, dots) with a single underscore
    text = re.sub(r'[ |_\-.]+', '_', text)

    # Trim surrounding underscores
    text = re.sub(r'^_+|_+$', '', text)

    # 6. Final lowercase
    return text.lower()