"""
Part D - AI-Augmented Task
Auto-detects CSV delimiter and converts CSV to JSON.
Prompt used: "Write a Python script that reads a CSV file, automatically detects
the delimiter (comma, tab, semicolon, or pipe), and converts the data into a
properly formatted JSON file. Use csv.Sniffer() if possible."
"""

import csv
import json
import sys
from pathlib import Path


def detect_delimiter(file_path):
    """
    Use csv.Sniffer to automatically detect the delimiter.
    Falls back to manual detection if Sniffer fails.
    """
    with open(file_path, "r", newline="") as f:
        sample = f.read(2048)  # read a chunk for sniffing

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        return dialect.delimiter
    except csv.Error:
        # Manual fallback: count which delimiter appears most in the header line
        first_line = sample.split("\n")[0]
        candidates = {",": first_line.count(","),
                      "\t": first_line.count("\t"),
                      ";": first_line.count(";"),
                      "|": first_line.count("|")}
        return max(candidates, key=candidates.get)


def csv_to_json(input_path, output_path=None):
    """
    Read a CSV file, detect its delimiter, and convert it to JSON.
    Output file defaults to same name with .json extension.
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(f"Error: File not found - {input_path}")
        sys.exit(1)

    # Auto-detect delimiter
    delimiter = detect_delimiter(input_file)
    delimiter_names = {",": "comma", "\t": "tab", ";": "semicolon", "|": "pipe"}
    print(f"Detected delimiter: {delimiter_names.get(delimiter, repr(delimiter))}")

    # Read CSV rows into list of dicts
    rows = []
    with open(input_file, "r", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            rows.append(dict(row))

    print(f"Rows read: {len(rows)}")

    # Determine output path
    if output_path is None:
        output_path = input_file.with_suffix(".json")

    # Write JSON output
    with open(output_path, "w") as f:
        json.dump(rows, f, indent=2)

    print(f"JSON saved to: {output_path}")
    return rows


# -------------------------------------------------------
# Demo: create test files with different delimiters
# -------------------------------------------------------

def create_test_files():
    """Create two test CSV files using different delimiters."""

    # File 1: semicolon-delimited
    with open("test_semicolon.csv", "w") as f:
        f.write("name;age;city\n")
        f.write("Alice;30;Mumbai\n")
        f.write("Bob;25;Delhi\n")
        f.write("Carol;35;Bangalore\n")

    # File 2: pipe-delimited
    with open("test_pipe.csv", "w") as f:
        f.write("id|product|price\n")
        f.write("1|Laptop|45000\n")
        f.write("2|Mouse|600\n")
        f.write("3|Keyboard|1200\n")

    print("Test files created: test_semicolon.csv, test_pipe.csv")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Normal usage: python part_d_csv_to_json.py <input.csv>
        csv_to_json(sys.argv[1])
    else:
        # Demo mode: test with two auto-created files
        print("=== Part D Demo: Auto-delimiter CSV to JSON ===\n")
        create_test_files()

        print("\n--- Test 1: Semicolon-delimited ---")
        result1 = csv_to_json("test_semicolon.csv", "test_semicolon_out.json")
        print("Output:", json.dumps(result1, indent=2))

        print("\n--- Test 2: Pipe-delimited ---")
        result2 = csv_to_json("test_pipe.csv", "test_pipe_out.json")
        print("Output:", json.dumps(result2, indent=2))
