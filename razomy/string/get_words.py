def get_words(value: str) -> list[str]:
    """
    Splits string into an array of its words by matching sequences of letters or numbers.

    Args:
        value: The string to process.

    Returns:
        An array of words found in the string.

    Example:
        get_words('fred, barney, & pebbles')  # => ['fred', 'barney', 'pebbles']
        get_words('camelCase')  # => ['camel', 'Case']
        get_words('nested_snake_case')  # => ['nested', 'snake', 'case']
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    word_pattern = r"[A-Z]{2,}(?=[A-Z][a-z]+|\b)|[A-Z]?[a-z]+|[A-Z]+|\d+"
    matches = value.match(word_pattern)
    if (!matches) {
        return []
    )
    return matches