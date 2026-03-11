"""
Part A - Multi-Source Data Merger
Reads 3 CSV files, merges them, removes duplicates,
calculates revenue per product, and exports results.
"""

import csv
import json
from pathlib import Path
from datetime import datetime


def read_csv_files(folder_path):
    """Read all CSV files matching data*.csv from the given folder."""
    folder = Path(folder_path)
    all_rows = []

    # Use glob to find all matching files automatically
    csv_files = sorted(folder.glob("data*.csv"))
    files_processed = len(csv_files)

    for file in csv_files:
        with open(file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_rows.append(row)

    return all_rows, files_processed


def remove_duplicates(rows):
    """Remove duplicate rows where all fields (date, product, qty, price) match."""
    seen = set()
    unique_rows = []

    for row in rows:
        # Create a tuple key from all 4 fields
        key = (row["date"], row["product"], row["qty"], row["price"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    return unique_rows


def calculate_revenue(rows):
    """Calculate total revenue per product: qty * price."""
    revenue = {}

    for row in rows:
        product = row["product"]
        qty = int(row["qty"])
        price = float(row["price"])
        rev = qty * price

        if product in revenue:
            revenue[product] += rev
        else:
            revenue[product] = rev

    return revenue


def export_merged_csv(rows, output_path):
    """Export unique rows sorted by date to merged_sales.csv."""
    # Sort rows by date
    sorted_rows = sorted(rows, key=lambda r: r["date"])

    with open(output_path, "w", newline="") as f:
        fieldnames = ["date", "product", "qty", "price"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_rows)


def export_revenue_json(revenue, files_processed, total_rows, output_path):
    """Export revenue summary with metadata to revenue_summary.json."""
    total_revenue = sum(revenue.values())

    output = {
        "metadata": {
            "files_processed": files_processed,
            "total_rows": total_rows,
            "total_revenue": round(total_revenue, 2),
            "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        },
        "revenue_by_product": {k: round(v, 2) for k, v in revenue.items()}
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)


def main():
    folder = Path(".")

    print("Reading CSV files...")
    all_rows, files_processed = read_csv_files(folder)
    print(f"  Total rows read (with duplicates): {len(all_rows)}")

    print("Removing duplicates...")
    unique_rows = remove_duplicates(all_rows)
    print(f"  Unique rows after deduplication: {len(unique_rows)}")

    print("Calculating revenue per product...")
    revenue = calculate_revenue(unique_rows)
    for product, rev in revenue.items():
        print(f"  {product}: {rev:.2f}")

    print("Exporting merged_sales.csv...")
    export_merged_csv(unique_rows, "merged_sales.csv")

    print("Exporting revenue_summary.json...")
    export_revenue_json(revenue, files_processed, len(unique_rows), "revenue_summary.json")

    print("\nDone! Files created: merged_sales.csv, revenue_summary.json")


if __name__ == "__main__":
    main()
