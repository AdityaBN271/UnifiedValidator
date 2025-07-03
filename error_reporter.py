from typing import List, Tuple, Dict
from parser import parse_xml, preprocess_file_content
from config import CUSTOM_ENTITIES, DEFAULT_REQUIRED_TAGS, NON_CLOSING_TAGS, SUPPORTED_TAGS
from entity_checker import check_entities
from tag_checker import validate_tags


def categorize_errors(errors: List[Tuple]) -> Dict[str, List[Tuple]]:
    """Categorizes errors into REPENT, REPTAG, CHECKSGM."""
    categorized = {
        "REPENT": [],
        "REPTAG": [],
        "CHECKSGM": []
    }

    for error in errors:
        if len(error) == 4:
            category, line, col, msg = error
        else:
            line, col, msg = error
            category = None

        msg_lower = msg.lower()

        if category == "Repent" or any(kw in msg_lower for kw in ["unescaped", "xmlparseentityref", "no name", "amp", "lt", "gt", "semicolon"]):
            categorized["REPENT"].append((line, col, msg))
        elif category == "Reptag" or any(kw in msg_lower for kw in [
            "tag mismatch", "misnested", "unknown tag", "must be inside", "must not be inside"
        ]):
            categorized["REPTAG"].append((line, col, msg))
        else:
            categorized["CHECKSGM"].append((line, col, msg))

    return categorized


def run_all_checks(file_path, custom_entities=None, required_tags=None) -> Dict[str, List[Tuple]]:
    """
    Main validation function.
    Uses raw content for line references,
    but parses cleaned content for XML structure.
    """
    all_errors = []

    # Step 1: Read raw content
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # Step 2: Preprocess content for parsing, keep line mapping
    cleaned_content = preprocess_file_content(raw_content)

    # Step 3: Parse cleaned XML
    tree, parse_errors, _ = parse_xml(raw_content)
    all_errors.extend(parse_errors)

    # Step 4: Stop here if not parsable
    if tree is None:
        return categorize_errors(all_errors)

    # Step 5: Entity validation on raw content
    entity_errors = check_entities(raw_content, custom_entities or CUSTOM_ENTITIES)
    all_errors.extend(entity_errors)

    # Step 6: Tag validation with corrected line numbers
    tag_errors = validate_tags(
        tree,
        allowed_tags=required_tags or SUPPORTED_TAGS,
        non_closing_tags=NON_CLOSING_TAGS,
    )
    all_errors.extend(tag_errors)

    return categorize_errors(all_errors)