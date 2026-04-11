import re

def dot_case(text: str) -> str:
    """
    Converts a given string into dot.case format by splitting the input on
    camelCase boundaries, non-alphanumeric characters, and whitespace, then joining
    the resulting lowercase words with dots.

    Args:
        text (str): The text to convert.

    Returns:
        str: The dot cased string.

    Examples:
        >>> dot_case('Hello World')
        'hello.world'
        >>> dot_case('camelCaseString')
        'camel.case.string'
        >>> dot_case('foo_bar')
        'foo.bar'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # Insert space before uppercase letter if preceded by a lowercase letter
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Replace non-alphanumeric characters (and multiple spaces resulting from previous steps) with a single space
    text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
    
    # Trim leading/trailing whitespace
    text = text.strip()
    
    # Split by spaces, convert to lowercase, and join with dots
    return ".".join(word.lower() for word in text.split())