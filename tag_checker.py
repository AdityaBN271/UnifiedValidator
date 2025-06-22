from lxml import etree

def validate_tags(tree, allowed_tags=None, non_closing_tags=None, line_mapping=None):
    """Validates XML tags and corrects line numbers using line_mapping if available."""
    errors = []
    if tree is None:
        return errors

    non_closing_tags = non_closing_tags or set()
    root = tree.getroot()

    # 🔍 Unknown tag check
    for elem in root.iter():
        if allowed_tags and elem.tag not in allowed_tags and elem.tag not in non_closing_tags:
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
            tag_stack.append(tag)
        elif event == "end":
            if tag in non_closing_tags:
                if tag in tag_stack:
                    tag_stack.remove(tag)
                continue

            if not tag_stack or tag_stack[-1] != tag:
                expected = tag_stack[-1] if tag_stack else "(none)"
                errors.append(("Reptag", line, col,
                               f"Misnested tag </{tag}> — expected </{expected}>"))

            if tag_stack:
                tag_stack.pop()

    return errors
