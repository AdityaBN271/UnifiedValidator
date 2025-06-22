import os
from error_reporter import run_all_checks
from config import CUSTOM_ENTITIES, SUPPORTED_TAGS


def print_error_report(results, folder_path):
    """Prints validation results with accurate line numbers and context."""
    print("\n" + "=" * 40)
    print("✅ XML VALIDATION REPORT".center(40))
    print("=" * 40)

    for filename, error_categories in results.items():
        file_path = os.path.join(folder_path, filename)
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

            print(f"\n{colors.get(category.upper(), '')}══ {category.upper()} ERRORS ({len(errors)}) ══{reset}")

            for err in errors:
                # Support (line, col, msg) or (cat, line, col, msg)
                line, col, msg = err if len(err) == 3 else (err[1], err[2], err[3])
                print(f"  Line {line:4}, Col {col:3} │ {msg}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if 0 < line <= len(lines):
                            context = lines[line - 1].strip()
                            print(f"       Context: '{context[:100]}'...")
                except Exception:
                    pass
                print() # This line adds the extra one-line gap after each error's context.


def validate_all_files(folder_path):
    """Runs all checks on valid files in the folder."""
    results = {}
    SAMPLES_FOLDER = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples"


    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(('.fnt', '.xml')):
            file_path = os.path.join(folder_path, filename)
            print(f"🔍 Scanning: {filename}", end='\r')

            results[filename] = run_all_checks(
                file_path,
                custom_entities=CUSTOM_ENTITIES,
                required_tags=SUPPORTED_TAGS
            )

    return results


if __name__ == "__main__":
    SAMPLES_FOLDER = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples"
    results = validate_all_files(SAMPLES_FOLDER)
    print_error_report(results, SAMPLES_FOLDER)

    print("\n" + "=" * 40)
    print(f"📊 SUMMARY: {len(results)} files scanned, {sum(len(errs) for res in results.values() for errs in res.values())} total issues")
    print("=" * 40)