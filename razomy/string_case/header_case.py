import re

def header_case(text: str) -> str:
    """
    Convert string to Header-Case (Train-Case).

    Converts a given string into Header-Case (also known as Train-Case), where each word is capitalized
    and separated by hyphens. The function handles various input formats including camelCase, snake_case,
    and strings with arbitrary delimiters by first splitting the text into individual words, capitalizing
    the first letter of each word, lowercasing the rest, and then joining them with hyphens.

    Args:
        text (str): The text to convert.

    Returns:
        str: The header cased string.

    Examples:
        >>> header_case('hello world')
        'Hello-World'
        >>> header_case('camelCaseString')
        'Camel-Case-String'
        >>> header_case('session_id')
        'Session-Id'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # Insert space before capital letters following a lowercase letter
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Replace non-alphanumeric characters (and multiple spaces) with a single space
    text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
    
    # Trim leading/trailing spaces
    text = text.strip()
    
    # Split into words and capitalize each word
    words = text.split()
    
    # Capitalize the first letter and lowercase the rest of each word
    capitalized_words = [word.capitalize() for word in words]
    
    # Join with hyphens
    return '-'.join(capitalized_words)