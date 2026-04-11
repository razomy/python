import re

def title_case(text: str) -> str:
    """
    Converts a string to title case.

    Converts the input string to title case by first lowercasing the entire string,
    then capitalizing the first letter of each word. Word boundaries are determined 
    by the \b regex anchor, so hyphenated words and other non-alphabetic separators 
    only trigger capitalization at the start of each word boundary segment.

    Args:
        text (str): The input string.

    Returns:
        str: The title cased string.

    Examples:
        >>> title_case('foo bar')
        'Foo Bar'
        >>> title_case('HELLO WORLD')
        'Hello World'
        >>> title_case('one-two')
        'One-Two'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return re.sub(r'\b\w', lambda match: match.group(0).upper(), text.lower())