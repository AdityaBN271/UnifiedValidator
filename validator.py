import os
from collections import defaultdict

from parser import parse_xml, preprocess_file_content
from entity_checker import check_entities
from tag_checker import validate_tags
from config import CUSTOM_ENTITIES, SUPPORTED_TAGS, NON_CLOSING_TAGS


def validate_all_files(folder_path):
    results = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".FNT") or filename.endswith(".xml"):
            print(f"\n🔍 Scanning: {filename}")
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            # Get cleaned content and line mapping
            cleaned_content, line_mapping = preprocess_file_content(raw_content)

            # Parse cleaned content
            tree, parse_errors, _ = parse_xml(raw_content)

            categorized_errors = []
            categorized_errors.extend(parse_errors)

            # ✅ Run entity checker on raw content
            entity_errors = check_entities(raw_content, custom_entities=CUSTOM_ENTITIES)
            categorized_errors.extend(entity_errors)

            # ✅ Run tag checker using original line numbers
            if tree is not None:
                tag_errors = validate_tags(
                    tree,
                    allowed_tags=SUPPORTED_TAGS,
                    non_closing_tags=NON_CLOSING_TAGS,
                    line_mapping=line_mapping
                )
                categorized_errors.extend(tag_errors)

            results[filename] = categorized_errors

    return results


if __name__ == "__main__":
    folder = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples"
    results = validate_all_files(folder)

    print("\n========= ✅ VALIDATION REPORT ✅ =========")
    for fname, errs in results.items():
        if errs:
            print(f"\n❌ {fname} — Errors Found:")
            grouped = defaultdict(list)
            for category, line, col, msg in errs:
                grouped[category].append((line, col, msg))

            for label, header in {
                "Repent": "🔹 Repent (Entity Errors)",
                "Reptag": "🔹 Reptag (Tag Mismatches or Unknown Tags)",
                "CheckSGM": "🔹 CheckSGM (Structural or Attribute Errors)"
            }.items():
                if grouped[label]:
                    print(f"\n{header}")
                    for line, col, msg in grouped[label]:
                        print(f"[Line {line}, Col {col}] {msg}")
        else:
            print(f"\n✅ {fname}: No errors found")

