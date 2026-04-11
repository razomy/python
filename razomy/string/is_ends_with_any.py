def is_ends_with_any(text: str, targets: list[str], position: int = -1) -> bool:
    """
    Checks if string ends with any of the given target strings.

    Args:
        text: The string to inspect.
        targets: The list of strings to search for.
        position: Optional position to search up to for the ending check (affects behavior of string.endsWith). Defaults to -1 (full string check).

    Returns:
        Returns true if string ends with any of the targets, else false.

    Example:
        is_ends_with_any('image.jpg', ['.jpg', '.png'])  # => True
        is_ends_with_any('image.gif', ['.jpg', '.png']) # => False
        is_ends_with_any('abc', ['a', 'b'], 2)          # => True
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    for target in targets:
        if text.endswith(target, position):
            return True
    return False