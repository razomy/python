import re
def constant_case(text: str) -> str:
    """
    Convert string to CONSTANT_case (macro case).
    Converts a given string from any common casing convention (camel_case, kebab-case,
    snake_case, space-separated, etc.) to CONSTANT_CASE (also known as macro case or screaming snake case),
    where all letters are uppercase and words are separated by underscores.
    Args:
        text (str): The text to convert.
    Returns:
        str: The constant cased string.
    Examples:
        >>> constant_case('hello world')
        'HELLO_WORLD'
        >>> constant_case('camelCaseString')
        'CAMEL_CASE_STRING'
        >>> constant_case('kebab-case-test')
        'KEBAB_CASE_TEST'
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # Insert space between lowercase and uppercase letters
    # (camelCase -> camel Case)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Replace all non-alphanumeric characters with space
    text = re.sub(r'[^a-zA-Z0-9]+', ' ', text).strip()
    # Split by whitespace to handle multi-word input
    return '_'.join(word.upper() for word in text.split())