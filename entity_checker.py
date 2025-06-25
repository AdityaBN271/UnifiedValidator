import re
from config import CUSTOM_ENTITIES, SUPPORTED_TAGS

DEFAULT_ENTITIES = {
    'amp', 'lt', 'gt', 'quot', 'apos',
    'mdash', 'sect', 'nbsp', 'copy'  # Add more as needed
}

def check_entities(file_content, custom_entities=None):
    """
    Improved entity checker that properly handles:
    - Valid XML/SGML tags
    - Actual unescaped special chars
    - Invalid entities
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
        
        # Check for invalid entities
        for match in entity_pattern.finditer(line):
            entity = match.group(1)
            if not entity.startswith('#') and entity not in allowed_entities:
                # Check if this is inside a tag
                inside_tag = any(start <= match.start() <= end for start, end in tag_positions)
                if not inside_tag:
                    col = match.start() + 1
                    errors.append(("Repent", line_num, col, 
                                 f"Invalid entity '&{entity};'"))

        # Check for unescaped special chars that aren't part of tags
        pos = 0
        while pos < len(line):
            if line[pos] == '<':
                # Check if this is part of a valid tag
                if not any(start <= pos < end for start, end in tag_positions):
                    errors.append(("Repent", line_num, pos + 1,
                                 "Unescaped '<' found - use '&lt;'"))
                pos += 1
            elif line[pos] == '>':
                if not any(start <= pos < end for start, end in tag_positions):
                    errors.append(("Repent", line_num, pos + 1,
                                 "Unescaped '>' found - use '&gt;'"))
                pos += 1
            elif line[pos] == '&':
                # Check if this starts a valid entity or is a legal & usage
                next_chars = line[pos:pos+10]  # Look ahead a bit
                if (not entity_pattern.match(next_chars) and 
                    not re.match(r'&\s', next_chars)):  # Ignore & followed by space
                    errors.append(("Repent", line_num, pos + 1,
                                 "Unescaped '&' found - use '&amp;'"))
                pos += 1
            else:
                pos += 1

    return errors