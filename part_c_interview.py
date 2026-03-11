"""
Part C - Interview Ready
Q2: find_large_files() function using pathlib
Q3: Fixed version of merge_csv_files()
"""

import csv
from pathlib import Path


# -------------------------------------------------------
# Q2 - find_large_files(directory, size_mb)
# -------------------------------------------------------

def find_large_files(directory, size_mb):
    """
    Recursively search for files larger than size_mb megabytes.
    Returns a list of (filename, size_in_mb) tuples sorted by size descending.
    """
    result = []
    dir_path = Path(directory)
    size_bytes = size_mb * 1024 * 1024  # convert MB to bytes

    # rglob("*") searches recursively through all subdirectories
    for file in dir_path.rglob("*"):
        if file.is_file():
            file_size = file.stat().st_size
            if file_size > size_bytes:
                size_in_mb = round(file_size / (1024 * 1024), 2)
                result.append((file.name, size_in_mb))

    # Sort by size descending
    result.sort(key=lambda x: x[1], reverse=True)
    return result


# -------------------------------------------------------
# Q3 - Fixed merge_csv_files()
# -------------------------------------------------------
# Bug 1: Missing import csv at top
# Bug 2: Missing newline='' in open() calls -> causes blank rows on Windows
# Bug 3: Header row is included from every file -> duplicated headers in output

def merge_csv_files(file_list):
    """
    Merges multiple CSV files into a single merged.csv.
    Fix 1: Added import csv at the top of the file.
    Fix 2: Added newline='' to both open() calls.
    Fix 3: Skip header row for all files except the first one.
    """
    all_data = []
    header_written = False

    for i, filename in enumerate(file_list):
        # Fix 2: newline='' prevents extra blank rows on Windows
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

            if not rows:
                continue

            if i == 0:
                # Include header only from the first file
                all_data.extend(rows)
                header_written = True
            else:
                # Fix 3: Skip the header row (index 0) for subsequent files
                all_data.extend(rows[1:])

    # Fix 2: newline='' on write as well
    with open("merged.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)

    return len(all_data)


# -------------------------------------------------------
# Demo / test
# -------------------------------------------------------

if __name__ == "__main__":
    # Test find_large_files
    print("=== Q2: find_large_files Demo ===")
    # Search current directory for files > 0.001 MB (1 KB) for demo purposes
    results = find_large_files(".", 0.001)
    if results:
        for name, size in results:
            print(f"  {name} -> {size} MB")
    else:
        print("  No files found above the threshold.")

    # Test merge_csv_files
    print("\n=== Q3: merge_csv_files Demo ===")
    files = ["data1.csv", "data2.csv", "data3.csv"]
    count = merge_csv_files(files)
    print(f"  Total rows written (including header): {count}")
    print("  Output saved to merged.csv")
