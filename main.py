import os
from validator import validate_all_files, print_error_report
from config import CUSTOM_ENTITIES, SUPPORTED_TAGS


def main():
    SAMPLES_FOLDER = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples"
    
    try:
        # Validate files and get results
        results = validate_all_files(SAMPLES_FOLDER)
        
        # Print the report
        print_error_report(results)
    except Exception as e:
        print(f"\n❌ Error during validation: {str(e)}")
        print("Please check your input files and try again.")


if __name__ == "__main__":
    main()