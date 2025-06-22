import re
from config import CUSTOM_ENTITIES

# Standard XML-safe named entities
DEFAULT_ENTITIES = {
    'amp', 'lt', 'gt', 'quot', 'apos',
    'mdash', 'sect'
}

def check_entities(file_content, custom_entities=None):
    """
    Detects invalid or unescaped entities in the raw file content.
    Returns: List of ("Repent", line, column, message) tuples.
    """
    errors = []
    lines = file_content.splitlines()

    # Combine standard + custom allowed entities
    allowed_entities = DEFAULT_ENTITIES.union(custom_entities or set())

    # Matches named and numeric entities like &name; or &#160;
    named_entity_pattern = re.compile(r'&([a-zA-Z0-9]+);')

    for line_num, line in enumerate(lines, 1):

        # Detect malformed or unknown named entities
        for match in named_entity_pattern.finditer(line):
            entity = match.group(1)
            if not entity.startswith('#') and entity not in allowed_entities:
                col = match.start() + 1
                errors.append(("Repent", line_num, col, f"Invalid entity '&{entity};'"))

        # Detect stray unescaped ampersands (&) not part of any entity
        for match in re.finditer(r'&', line):
            pos = match.start()
            after = line[pos + 1] if pos + 1 < len(line) else ''
            before = line[pos - 1] if pos > 0 else ''

            # Skip allowed forms:
            if before == ' ' and after == ' ':
                continue  # case: " & "
            if pos == 0 and after == ' ':
                continue  # case: line starts with "& "

            # Check if this is part of a valid named entity
            if not named_entity_pattern.match(line[pos:]):
                errors.append(("Repent", line_num, pos + 1, "Unescaped '&' found — use '&amp;'"))

        # Unescaped < not starting a tag
        if '<' in line and not line.strip().startswith('<'):
            col = line.find('<') + 1
            errors.append(("Repent", line_num, col, "Unescaped '<' found — use '&lt;'"))

        # Unescaped > not ending a tag
        if '>' in line and not line.strip().endswith('>') and not line.strip().startswith('<'):
            col = line.find('>') + 1
            errors.append(("Repent", line_num, col, "Unescaped '>' found — use '&gt;'"))

    return errors
