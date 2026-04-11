import re
from typing import List

def path_case(text: str) -> str:
    """
    Convert string to path/case.
    
    Converts a given string into path/case format by splitting it on camelCase boundaries,
    non-alphanumeric characters, and whitespace, then joining the resulting lowercase words with forward slashes.
    
    Args:
        text (str): The text to convert.
        
    Returns:
        str: The path cased string.
        
    Examples:
        >>> path_case('Hello World')
        'hello/world'
        >>> path_case('camelCaseString')
        'camel/case/string'
        >>> path_case('foo_bar')
        'foo/bar'
        
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # Replace camelCase patterns with spaces
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Replace non-alphanumeric characters with spaces
    text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    # Split on whitespace and join with forward slashes
    return '/'.join(word.lower() for word in text.split())
