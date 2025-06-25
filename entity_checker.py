import re
from config import CUSTOM_ENTITIES

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
    allowed_entities = DEFAULT_ENTITIES.union(custom_entities or set())
    named_entity_pattern = re.compile(r'&([a-zA-Z0-9]+);')

    for line_num, line in enumerate(lines, 1):

        # Valid named entities
        for match in named_entity_pattern.finditer(line):
            entity = match.group(1)
            if not entity.startswith('#') and entity not in allowed_entities:
                col = match.start() + 1
                errors.append(("Repent", line_num, col, f"Invalid entity '&{entity};'"))

        # Raw & checks — skip valid forms
        for match in re.finditer(r'&', line):
            idx = match.start()
            before = line[idx - 1] if idx > 0 else ''
            after = line[idx + 1] if idx + 1 < len(line) else ''

            if (before == ' ' and after == ' ') or (idx == 0 and after == ' '):
                continue  # safe

            if not named_entity_pattern.match(line[idx:]):
                errors.append(("Repent", line_num, idx + 1, "Unescaped '&' found — use '&amp;'"))

        # Raw < checks
        if '<' in line and not line.strip().startswith('<'):
            col = line.find('<') + 1
            errors.append(("Repent", line_num, col, "Unescaped '<' found — use '&lt;'"))

        # Raw > checks
        if '>' in line and not line.strip().endswith('>') and not line.strip().startswith('<'):
            col = line.find('>') + 1
            errors.append(("Repent", line_num, col, "Unescaped '>' found — use '&gt;'"))

    return errors
