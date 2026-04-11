def similarity(str1: str, str2: str) -> float:
    """
    Calculate the similarity ratio between two strings.
    Computes a similarity score between 0 and 1 for two strings based on their Levenshtein distance. 
    A score of 1 indicates identical strings, while 0 indicates no commonality.

    Args:
        str1: The first string to compare.
        str2: The second string to compare.

    Returns:
        A number between 0 and 1 representing the similarity ratio.

    Example:
        similarity('hello', 'hello')  # => 1
        similarity('hello', 'hallo')  # => 0.8
        similarity('test', '')         # => 0

    Complexity:
        Time: O(n * m)
        Memory: O(n * m)
    """
    max_length = max(len(str1), len(str2))

    if max_length == 0:
        return 1.0

    distance = string.levenshtein_distance(str1, str2)

    return 1.0 - (distance / max_length)