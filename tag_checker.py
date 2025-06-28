from lxml import etree
from entity_checker import check_entities
from config import SUPPORTED_TAGS, NON_CLOSING_TAGS


def validate_tags(tree, allowed_tags=None, non_closing_tags=None, line_mapping=None):
    """Validates XML tags while ignoring specified non-closing tags."""
    errors = []
    if tree is None:
        return errors

    non_closing_tags = non_closing_tags or set()
    root = tree.getroot()

    # Helper function to check if tag matches any non-closing pattern
    def is_non_closing(tag):
        tag_lower = tag.lower()
        return any(
            tag_lower == base_tag.lower() or 
            (base_tag.endswith('*') and tag_lower.startswith(base_tag.rstrip('*').lower())) or
            (base_tag.endswith('*') and tag_lower == base_tag.lower().rstrip('*')) or
            (base_tag[:-1].isdigit() and tag_lower == base_tag.lower()[:-1])
            for base_tag in non_closing_tags
        )

    # 🔍 Unknown tag check
    for elem in root.iter():
        if not is_non_closing(elem.tag) and allowed_tags and elem.tag not in allowed_tags:
            parsed_line = elem.sourceline or 0
            col = getattr(elem, "sourcepos", 0)
            orig_line = line_mapping.get(parsed_line, parsed_line) if line_mapping else parsed_line
            errors.append(("Reptag", orig_line, col, f"Unknown tag <{elem.tag}>"))

    # 🔄 Nesting check
    tag_stack = []
    for event, elem in etree.iterwalk(tree, events=("start", "end")):
        tag = elem.tag
        parsed_line = elem.sourceline or 0
        col = getattr(elem, "sourcepos", 0)
        line = line_mapping.get(parsed_line, parsed_line) if line_mapping else parsed_line

        if event == "start":
            if not is_non_closing(tag):
                tag_stack.append(tag)
        elif event == "end":
            if is_non_closing(tag):
                continue
                
            if not tag_stack or tag_stack[-1] != tag:
                expected = tag_stack[-1] if tag_stack else "(none)"
                errors.append(("Reptag", line, col,
                             f"Misnested tag </{tag}> — expected </{expected}>"))
            else:
                tag_stack.pop()

    return errors