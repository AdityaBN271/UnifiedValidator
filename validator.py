import os
import re
from collections import defaultdict
from parser import parse_xml, preprocess_file_content
from entity_checker import check_entities
from tag_checker import validate_tags
from config import CUSTOM_ENTITIES, SUPPORTED_TAGS, NON_CLOSING_TAGS


def validate_all_files(folder_path):
    results = {}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.fnt', '.xml')):
            print(f"\n🔍 Scanning: {filename}")
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            # Extract page numbers from P20 tags
            page_numbers = {}
            for match in re.finditer(r'<P20>(\d+)</P20>', raw_content):
                page_numbers[match.start()] = match.group(1)

            # Get cleaned content and line mapping
            cleaned_content = preprocess_file_content(raw_content)
            line_mapping = {}

            # Parse cleaned content
            tree, parse_errors, _ = parse_xml(cleaned_content)

            categorized_errors = []
            
            # Process parse errors with page numbers and context
            for error in parse_errors:
                if len(error) == 4:
                    cat, line, col, msg = error
                    # Find closest page number
                    page = next((p for pos, p in sorted(page_numbers.items()) if pos <= line*100), "?")
                    msg = msg.replace("XML Syntax error: ", "")
                    categorized_errors.append((cat, line, page, msg, raw_content.splitlines()[line-1].strip()))
                else:
                    line, col, msg = error
                    page = next((p for pos, p in sorted(page_numbers.items()) if pos <= line*100), "?")
                    msg = msg.replace("XML Syntax error: ", "")
                    categorized_errors.append(("Reptag", line, page, msg, raw_content.splitlines()[line-1].strip()))

            # Entity checks with page numbers and context
            entity_errors = check_entities(raw_content, custom_entities=CUSTOM_ENTITIES)
            for err in entity_errors:
                if len(err) == 4:
                    _, line, col, msg = err
                    page = next((p for pos, p in sorted(page_numbers.items()) if pos <= line*100), "?")
                    categorized_errors.append(("Repent", line, page, msg, raw_content.splitlines()[line-1].strip()))

            # Tag validation with page numbers and context
            if tree is not None:
                tag_errors = validate_tags(
                    tree,
                    allowed_tags=SUPPORTED_TAGS,
                    non_closing_tags=NON_CLOSING_TAGS,
                    line_mapping=line_mapping
                )
                for err in tag_errors:
                    if len(err) == 4:
                        _, line, col, msg = err
                        page = next((p for pos, p in sorted(page_numbers.items()) if pos <= line*100), "?")
                        categorized_errors.append(("Reptag", line, page, msg, raw_content.splitlines()[line-1].strip()))

            results[filename] = categorized_errors

    return results


def print_error_report(results):
    """Prints the validation report with context and page numbers"""
    print("\n" + "=" * 40)
    print("✅ XML VALIDATION REPORT".center(40))
    print("=" * 40)

    for filename, errors in results.items():
        if not errors:
            print(f"\n✅ {filename}: No errors found")
            continue

        print(f"\n❌ {filename}: {len(errors)} ISSUES FOUND")
        
        # Group errors by category
        error_groups = defaultdict(list)
        for error in errors:
            if len(error) == 5:
                category, line, page, msg, context = error
                error_groups[category].append((line, page, msg, context))
            else:
                error_groups["Other"].append((0, "?", str(error), "No context available"))

        # Print errors by category
        for category, errors in error_groups.items():
            # Color coding
            colors = {
                "Repent": "\033[91m",    # Red
                "Reptag": "\033[93m",    # Yellow
                "CheckSGM": "\033[96m",  # Cyan
                "Other": "\033[90m"      # Gray
            }
            reset = "\033[0m"

            print(f"\n{colors.get(category, '')}══ {category.upper()} ERRORS ({len(errors)}) ══{reset}")
            
            for line, page, msg, context in errors:
                print(f"  [Page {page}, Line {line}] {msg}")
                print(f"       Context: '{context[:100]}'...")
                print()  # Blank line after each error

    # Print summary
    total_files = len(results)
    total_errors = sum(len(errs) for errs in results.values())
    print("\n" + "=" * 40)
    print(f"📊 SUMMARY: {total_files} files scanned, {total_errors} total issues")
    print("=" * 40)


if __name__ == "__main__":
    folder = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples"
    results = validate_all_files(folder)
    print_error_report(results)