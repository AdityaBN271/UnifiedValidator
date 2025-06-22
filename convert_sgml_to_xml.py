import re
import os

def convert_sgml_to_xml(input_path, output_path):
    open_tags = []
    xml_lines = []

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()

        # Convert [TAG] to <TAG> and track open tags
        tag_match = re.match(r'\[(\w+)\]', stripped)
        if tag_match:
            tag = tag_match.group(1)
            xml_lines.append(f"<{tag}>")
            open_tags.append(tag)
        else:
            xml_lines.append(line.rstrip())

    # Close all tags in reverse order
    for tag in reversed(open_tags):
        xml_lines.append(f"</{tag}>")

    # Write to output XML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))

    print(f"\n✅ Converted XML saved to: {output_path}")

# === Example Usage ===
if __name__ == "__main__":
    input_file = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples\23-4031.FNT"   # Replace with your path
    output_file = r"C:\Users\nbs\OneDrive\Desktop\UnifiedXMLvalidator\Samples\sample_output.xml"
    convert_sgml_to_xml(input_file, output_file)
