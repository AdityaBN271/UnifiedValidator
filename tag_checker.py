from lxml import etree
from entity_checker import check_entities
from config import SUPPORTED_TAGS, NON_CLOSING_TAGS, TAG_RELATIONSHIPS
from lxml.etree import _Element
import logging



logger = logging.getLogger(__name__)

def validate_tags(tree, allowed_tags=None, non_closing_tags=None, line_mapping=None):
    errors = []
    if tree is None:
        return errors

    root = tree.getroot()

    def is_fnt_variant(tag):
        """Returns True if tag is any fnt variant (fnt, fnt*, fnt1, fnt2, etc.)"""
        tag_lower = tag.lower()
        return (tag_lower.startswith('fnt') and 
                (tag_lower in {'fnt', 'fnt*'} or 
                 tag_lower[3:].isdigit()))  # Matches fnt followed by digits

    def is_non_closing(tag):
        """Returns True if tag is a non-closing tag (fnt*, fnr*, etc.)"""
        tag_lower = tag.lower()
        non_closing_tags_lower = {t.lower() for t in (non_closing_tags or NON_CLOSING_TAGS)}
        return any(
            tag_lower == base_tag.lower() or
            (base_tag.endswith('*') and tag_lower.startswith(base_tag.rstrip('*').lower())) or
            (base_tag[:-1].isdigit() and tag_lower == base_tag.lower()[:-1])
            for base_tag in non_closing_tags_lower
        )

    # First pass: Validate all elements
    for elem in root.iter():
        tag = elem.tag
        parent = elem.getparent()
        parent_tag = parent.tag if parent is not None else None

        line = elem.sourceline or 0
        col = getattr(elem, "sourcepos", 0)
        orig_line = line_mapping.get(line, line) if line_mapping else line

        # Rule 1: Any fnt variant must be inside FN
        if is_fnt_variant(tag) and parent_tag != 'FN':
            errors.append((
                "Reptag",
                orig_line,
                col,
                f"<{tag}> must be inside <FN> tags (found outside)"
            ))

        # Rule 2: fnt variants cannot have closing tags (even inside FN)
        if is_fnt_variant(tag) and elem.tail and '</' + tag.lower() + '>' in elem.tail.lower():
            errors.append((
                "Reptag",
                orig_line,
                col,
                f"<{tag}> is a non-closing tag (do not use </{tag}>)"
            ))

        # Rule 3: Only fnt variants allowed inside FN
        if parent_tag == 'FN' and not is_fnt_variant(tag) and tag.lower() != 'fn':
            errors.append((
                "Reptag",
                orig_line,
                col,
                f"Only <fnt*> tags allowed inside <FN>, found <{tag}>"
            ))

    # Second pass: Validate FN nesting structure
    fn_stack = []
    for event, elem in etree.iterwalk(tree, events=("start", "end")):
        tag = elem.tag
        line = elem.sourceline or 0
        col = getattr(elem, "sourcepos", 0)
        orig_line = line_mapping.get(line, line) if line_mapping else line

        if event == "start":
            if tag == 'FN':
                fn_stack.append((elem, orig_line, col))
        elif event == "end":
            if tag == 'FN' and fn_stack:
                fn_elem, fn_line, fn_col = fn_stack.pop()
                # Check if FN contains any non-fnt elements
                if any(not is_fnt_variant(child.tag) for child in fn_elem):
                    errors.append((
                        "Reptag",
                        orig_line,
                        col,
                        f"<FN> contains invalid child elements"
                    ))

    return errors
    