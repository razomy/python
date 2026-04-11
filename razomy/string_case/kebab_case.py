import re

def kebab_case(text: str) -> str:
    """
    Converts a given string to kebab-case by handling acronyms, camelCase, letter-number boundaries,
    and various delimiters (spaces, underscores, hyphens, dots). Leading and trailing separators are stripped,
    and the result is lowercased.

    Args:
        text (str): The text to convert.

    Returns:
        str: The kebab cased string.

    Examples:
        >>> kebab_case('fooBar')
        'foo-bar'
        >>> kebab_case('Foo Bar')
        'foo-bar'
        >>> kebab_case('__FOO_BAR__')
        'foo-bar'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # 1. Handle Acronyms: 'JSONData' -> 'JSON-Data'
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1-\2', text)

    # 2. Handle CamelCase: 'camelCase' -> 'camel-Case'
    text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)

    # 3. Handle Letters to Numbers: 'version2' -> 'version-2'
    text = re.sub(r'([a-zA-Z])([0-9])', r'\1-\2', text)

    # 4. Handle Numbers to Letters: '2beta' -> '2-beta'
    text = re.sub(r'([0-9])([a-zA-Z])', r'\1-\2', text)

    # 5. Replace delimiters (spaces, hyphens, dots) with a single hyphen
    # This collapses multiple separators (e.g. ' - ' becomes '-')
    text = re.sub(r'[ |_\\-\\.]+', '-', text)

    # Remove leading and trailing hyphens/underscores
    text = re.sub(r'^[_-]+|[_-]+$', '', text)

    # 6. Final lowercase
    return text.lower()