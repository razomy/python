def is_null_or_empty(str: str | None | int | float | bytes | bool | None) -> bool:
    """
    Check if the string is null, undefined, or empty (including whitespace).

    Args:
        str: The value to check.

    Returns:
        True if the string is null, undefined, or consists only of whitespace.

    Example:
        isNullOrEmpty(None)  # => True
        isNullOrEmpty('   ')  # => True
        isNullOrEmpty('razomy')  # => False
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    if str is None:
        return True
    if isinstance(str, str):
        return str.strip() == ''
    return True