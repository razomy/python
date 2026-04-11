import re

def pascal_case(text: str) -> str:
    """
    Converts a given string to PascalCase by splitting it into words
    (handling spaces, underscores, and camelCase/UPPERCASE boundaries),
    capitalizing the first letter of each word, lowercasing the rest,
    and joining them together without any separator.

    Args:
        text (str): The string to convert.

    Returns:
        str: The pascal cased string.

    Examples:
        >>> pascal_case('foo bar')
        'FooBar'
        >>> pascal_case('foo_bar')
        'FooBar'
        >>> pascal_case('FOO BAR')
        'FooBar'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # This regex captures sequences that resemble words in various casings:
    # 1. [A-Z][a-z]+: A standard capitalized word (e.g., "Word")
    # 2. [A-Z]+(?=[A-Z][a-z]): An acronym followed by a word (e.g., "API" in "APIName")
    # 3. [A-Z]+: A sequence of all caps (e.g., "FOO")
    # 4. [a-z]+: A lowercase word (e.g., "word")
    # 5. [0-9]+: A sequence of numbers (e.g., "123")
    words = re.findall(r'[A-Z][a-z]+|[A-Z]+(?=[A-Z][a-z])|[A-Z]+|[a-z]+|[0-9]+', text)
    
    # Map each found word to title case (first letter upper, rest lower)
    return "".join(word[0].upper() + word[1:].lower() for word in words)