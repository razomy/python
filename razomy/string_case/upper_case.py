def upper_case(text: str) -> str:
    """
    Converts string to upper case.

    Converts all characters in the given string to their upper-case equivalents
    using the built-in str.upper() method. The original string is not modified;
    a new upper-cased string is returned.

    Args:
        text (str): The input string.

    Returns:
        str: The upper-cased string.

    Examples:
        >>> upper_case('test')
        'TEST'
        >>> upper_case('Hello World')
        'HELLO WORLD'
        >>> upper_case('razomy')
        'RAZOMY'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.upper()