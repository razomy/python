import re

def humanize(text: str) -> str:
    """
    Convert a string to a human-readable form.

    Transforms a string from common programming naming conventions (camelCase, snake_case, kebab-case)
    into a human-readable sentence. It splits words by detecting camelCase boundaries, underscores, and hyphens,
    normalizes whitespace, converts the result to lowercase, and capitalizes the first letter.

    Args:
        text (str): The string to humanize.

    Returns:
        str: The humanized string.

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # Simulate the behavior of the external 'capitalize' function.
    # In idiomatic Python, this is usually done with str.capitalize()
    def capitalize(s: str) -> str:
        if not s:
            return s
        return s[0].upper() + s[1:]

    # Replace camelCase transitions with space
    separated = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Replace underscores and hyphens with space
    separated = re.sub(r'[_-]+', ' ', separated)
    
    # Normalize multiple whitespace characters to a single space
    separated = re.sub(r'\s+', ' ', separated)
    
    # Trim leading/trailing whitespace and convert to lowercase
    separated = separated.strip().lower()
    
    # Capitalize the first letter of the resulting string
    return capitalize(separated)