def truncate(text: str, length: int, omission: str = '...') -> str:
    """
    Truncates string if it's longer than the given maximum string length.
    Truncates the input string to a specified length, appending an omission string if truncation occurs.

    Args:
        text: The string to truncate.
        length: The maximum desired length of the resulting string (excluding the omission string).
        omission: The string to be appended to indicate truncation. Defaults to '...'.

    Returns:
        The truncated string.

    Example:
        truncate('hello world', 5)  # => 'he...'
        truncate('hello', 10)  # => 'hello'
        truncate('hello world', 7, '...')  # => 'hello...'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    if len(text) <= length:
        return text

    return text[:length - len(omission)] + omission