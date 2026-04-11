import re

def alternating_case(text: str) -> str:
    """
    Convert string to aLtErNaTiNg cAsE (SpongeBob case).

    Alternates cases based on the index of the character. Spaces and hyphens are preserved
    and act as separators between blocks where alternation restarts.

    Args:
        text: The text to convert.

    Returns:
        The alternating cased string.

    Examples:
        >>> alternating_case('hello world')
        'hElLo wOrLd'
        >>> alternating_case('typescript')
        'tYpEsCrIpT'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    def process_word(word: str) -> str:
        """Applies alternating case to a single word segment."""
        return "".join(
            char.lower() if index % 2 == 0 else char.upper()
            for index, char in enumerate(word)
        )

    # Split by sequences of whitespace or hyphens, keeping the delimiters
    parts = re.split(r'([ \-]+)', text)
    
    result_parts = []
    for part in parts:
        if re.fullmatch(r'[ \-]+', part):
            # Delimiter (space or hyphen) - keep as is
            result_parts.append(part)
        else:
            # Word segment - apply alternating case
            result_parts.append(process_word(part))
            
    return "".join(result_parts)