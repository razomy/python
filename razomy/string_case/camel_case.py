import re

def camel_case(text: str) -> str:
    """
    Converts a string to camel case.
    
    Takes an input string in any common format (space-separated, kebab-case, snake_case, PascalCase, etc.)
    and converts it to camelCase. The function first normalizes the string by identifying word boundaries
    (including transitions between acronyms, letters/numbers, and common delimiters like spaces, hyphens, dots, and underscores),
    then joins the segments together with the first segment in lowercase and each subsequent segment capitalized.
    
    Args:
        text (str): The text to convert.
        
    Returns:
        str: The camel cased string.
        
    Examples:
        >>> camel_case('Foo Bar')
        'fooBar'
        >>> camel_case('--foo-bar--')
        'fooBar'
        >>> camel_case('__FOO_BAR__')
        'fooBar'
        
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    # 1-5. Normalize the string using the same logic as snake_case
    # This breaks the string into segments separated by underscores
    
    # Handle Acronyms: 'JSONData' -> 'JSON_Data'
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1_\2', text)
    
    # Handle CamelCase: 'camelCase' -> 'camel_Case'
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
    
    # Handle Letters to Numbers: 'version2' -> 'version_2'
    text = re.sub(r'([a-zA-Z])([0-9])', r'\1_\2', text)
    
    # Handle Numbers to Letters: '2beta' -> '2_beta'
    text = re.sub(r'([0-9])([a-zA-Z])', r'\1_\2', text)
    
    # Replace delimiters with underscore
    text = re.sub(r'[ |_\-\.]+', '_', text)
    
    # Trim surrounding underscores
    text = re.sub(r'^_+|_+$', '', text)
    
    # Lowercase the entire normalized string first
    text = text.lower()

    # 6. Convert snake_case segments to camelCase
    # Looks for an underscore followed by a character (letter or number)
    return re.sub(r'_([a-z0-z])', lambda match: match.group(1).upper(), text)