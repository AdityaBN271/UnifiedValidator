import re
from config import CUSTOM_ENTITIES, SUPPORTED_TAGS

DEFAULT_ENTITIES = {
    'amp', 'lt', 'gt', 'quot', 'apos',
    'mdash', 'sect', 'nbsp', 'copy'  # Add more as needed
}

def check_entities(file_content, custom_entities=None):
    """
    Entity checker that focuses ONLY on invalid entities (ignores unescaped chars)
    Checks for:
    - Invalid named entities
    - Does NOT check for unescaped <, >, or & characters
    """
    errors = []
    lines = file_content.splitlines()
    allowed_entities = DEFAULT_ENTITIES.union(custom_entities or set())
    
    # Pattern to match XML/SGML tags
    tag_pattern = re.compile(r'<\/?[a-zA-Z][a-zA-Z0-9]*(\s+[^>]*)?>')
    # Pattern to match both named and numeric entities
    entity_pattern = re.compile(r'&(#[0-9]+|#x[0-9a-fA-F]+|[a-zA-Z0-9]+);')

    for line_num, line in enumerate(lines, 1):
        # First find all valid tags in the line
        tag_positions = []
        for match in tag_pattern.finditer(line):
            tag_positions.append((match.start(), match.end()))
        
        # Check for invalid named entities only
        for match in entity_pattern.finditer(line):
            entity = match.group(1)
            # Only validate named entities (ignore numeric entities)
            if not entity.startswith('#') and entity not in allowed_entities:
                # Check if this is inside a tag (like an attribute)
                inside_tag = any(start <= match.start() <= end for start, end in tag_positions)
                if not inside_tag:
                    col = match.start() + 1
                    errors.append(("Repent", line_num, col, 
                                 f"Invalid entity '&{entity};'"))

    return errors