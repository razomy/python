def is_upper_case(text: str) -> bool:
    """
    Checks if a string is upper case.

    Determines whether the given string is entirely in upper case by comparing it to its upper-cased transformation. 
    Returns true only if every character in the string is already upper case (i.e., the string is identical to the result of calling str.upper() on it).

    Args:
        text (str): The string to check.

    Returns:
        bool: True if the string is upper case.

    Examples:
        >>> is_upper_case('HELLO')
        True
        >>> is_upper_case('Hello')
        False
        >>> is_upper_case('hello')
        False

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text == text.upper()