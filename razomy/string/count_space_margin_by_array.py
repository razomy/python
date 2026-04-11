def count_space_margin_by_array(strings: list[str]) -> list[int]:
    """
    Count leading space margins for each string in an array.

    Args:
        strings: The array of strings to count leading space margins for.

    Returns:
        A list of numbers where each number is the leading space count of the corresponding string.

    Example:
        count_space_margin_by_array(['  hello', '    world', 'foo'])  # => [2, 4, 0]
        count_space_margin_by_array(['', '   ', ' a'])              # => [0, 3, 1]
        count_space_margin_by_array([])                             # => []
    
    Complexity:
        Time: O(n * m) where n is the array length and m is the average string length
        Memory: O(n)
    """
    return [count_space_margin(s) for s in strings]