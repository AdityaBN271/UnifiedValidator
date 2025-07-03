from lxml import etree
from entity_checker import check_entities
from config import SUPPORTED_TAGS, NON_CLOSING_TAGS, TAG_RELATIONSHIPS
from lxml.etree import _Element

def validate_tag_relationships(tree, line_mapping=None):
    """Validates tag relationships based on configuration rules."""
    errors = []
    if tree is None:
        return errors

    for elem in tree.iter():
        tag = elem.tag
        if tag not in TAG_RELATIONSHIPS:
            continue

        rules = TAG_RELATIONSHIPS[tag]
        parent = elem.getparent()
        parent_tag = parent.tag if parent is not None else None

        # Get line/col information
        parsed_line = elem.sourceline or 0
        col = getattr(elem, "sourcepos", 0)
        line = line_mapping.get(parsed_line, parsed_line) if line_mapping else parsed_line

        # Check fnt is inside FN
        if tag == 'fnt' and rules.get('required_parent'):
            if parent_tag != rules['required_parent']:
                errors.append(("Reptag", line, col, 
                             f"<{tag}> must be inside <{rules['required_parent']}> tags"))

        # Check fnr is not inside FN
        if tag == 'fnr' and rules.get('forbidden_parent'):
            if parent_tag == rules['forbidden_parent']:
                errors.append(("Reptag", line, col,
                             f"<{tag}> must not be inside <{rules['forbidden_parent']}> tags"))

    return errors


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

    # 🔍 Tag validation
    for elem in root.iter():
        tag = elem.tag
        parent = elem.getparent()
        parent_tag = parent.tag if parent is not None else None
        
        parsed_line = elem.sourceline or 0
        col = getattr(elem, "sourcepos", 0)
        orig_line = line_mapping.get(parsed_line, parsed_line) if line_mapping else parsed_line

        # Unknown tag check
        if not is_non_closing(tag) and allowed_tags and tag not in allowed_tags:
            errors.append(("Reptag", orig_line, col, f"Unknown tag <{tag}>"))
        
        # Check tags inside FN blocks
        if parent_tag == 'FN':
            if tag.lower() != 'fnt':
                errors.append(("Reptag", orig_line, col, 
                             f"Only <fnt> tags are allowed inside <FN> blocks, found <{tag}>"))
        
        # Check fnt tags outside FN blocks
        if tag.lower() == 'fnt' and parent_tag != 'FN':
            errors.append(("Reptag", orig_line, col, 
                         f"<fnt> must be inside <FN> tags"))

    # 🔄 Nesting check (existing code remains unchanged)
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