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

        # Clean the message by removing "XML Syntax error: " prefix
        msg = msg.replace("XML Syntax error: ", "")
        msg_lower = msg.lower()

        if category == "Repent" or any(kw in msg_lower for kw in ["unescaped", "xmlparseentityref", "no name", "amp", "lt", "gt", "semicolon"]):
            categorized["REPENT"].append((line, msg))  # Removed column number
        elif category == "Reptag" or any(kw in msg_lower for kw in [
            "tag mismatch", "misnested", "unknown tag", "must be inside", "must not be inside"
        ]):
            categorized["REPTAG"].append((line, msg))  # Removed column number
        else:
            categorized["CHECKSGM"].append((line, msg))  # Removed column number

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
    
    # Clean parse errors before extending
    cleaned_parse_errors = []
    for error in parse_errors:
        if len(error) == 4:
            cat, line, col, msg = error
            cleaned_parse_errors.append((cat, line, msg.replace("XML Syntax error: ", "")))
        else:
            line, col, msg = error
            cleaned_parse_errors.append((line, msg.replace("XML Syntax error: ", "")))
    
    all_errors.extend(cleaned_parse_errors)

    # Step 4: Stop here if not parsable
    if tree is None:
        return categorize_errors(all_errors)

    # Step 5: Entity validation on raw content
    entity_errors = check_entities(raw_content, custom_entities or CUSTOM_ENTITIES)
    all_errors.extend([(line, msg) for _, line, _, msg in entity_errors])  # Remove column

    # Step 6: Tag validation with corrected line numbers
    tag_errors = validate_tags(
        tree,
        allowed_tags=required_tags or SUPPORTED_TAGS,
        non_closing_tags=NON_CLOSING_TAGS,
    )
    all_errors.extend([(line, msg) for _, line, _, msg in tag_errors])  # Remove column

    return categorize_errors(all_errors)


def print_error_report(results: Dict[str, Dict[str, List[Tuple]]]):
    """Prints the validation report in the new format"""
    print("\n" + "=" * 40)
    print("✅ XML VALIDATION REPORT".center(40))
    print("=" * 40)

    for filename, error_categories in results.items():
        total_errors = sum(len(errs) for errs in error_categories.values())

        if total_errors == 0:
            print(f"\n✔ {filename}: CLEAN - No issues found")
            continue

        print(f"\n❌ {filename}: {total_errors} ISSUES FOUND")

        for category, errors in error_categories.items():
            if not errors:
                continue

            # Color coding
            colors = {
                "REPENT": "\033[91m",     # Red
                "REPTAG": "\033[93m",     # Yellow
                "CHECKSGM": "\033[96m"    # Cyan
            }
            reset = "\033[0m"

            print(f"\n{colors.get(category, '')}══ {category.upper()} ERRORS ({len(errors)}) ══{reset}")

            for err in errors:
                if len(err) == 2:
                    line, msg = err
                else:
                    line = err[0]
                    msg = err[-1]
                
                print(f"Line {line} | {msg}")
                print()  # Blank line between errors