import re

def swap_case(text: str) -> str:
    """
    Convert string by swapping the case of every character.
    Uppercase becomes lowercase, and lowercase becomes uppercase.
    
    Args:
        text (str): The text to convert.
        
    Returns:
        str: The swapped case string.
        
    Examples:
        >>> swap_case('Hello World')
        'hELLO wORLD'
        >>> swap_case('camelCase')
        'CAMELcASE'
        >>> swap_case('123 ABC xyz')
        '123 abc XYZ'
        
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    def swap(char: str) -> str:
        """Helper function to swap case of a single character."""
        lower = char.lower()
        return char.upper() if char == lower else lower
        
    return ''.join(swap(char) for char in text)