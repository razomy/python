def split_lines(text: str) -> list[str]:
    """
    Split string by newline characters.

    Args:
        text: The string to split.

    Returns:
        An array of lines.

    Example:
        split_lines('Line 1\nLine 2')  # => ['Line 1', 'Line 2']
        split_lines('A\r\nB\nC')        # => ['A', 'B', 'C']
        split_lines('One')            # => ['One']
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.split(/\r\n|\r|\n/)