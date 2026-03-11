"""
Part B - Backup Manager with Rotation
Copies .csv and .json files from source to backup directory,
appends timestamps to filenames, and keeps only last 5 backups per file.
Usage: python backup_manager.py <source_directory> <backup_directory>
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime


# Only backup files with these extensions
BACKUP_EXTENSIONS = [".csv", ".json"]

# Keep only the last N backups per original file
MAX_BACKUPS = 5

# Log file
LOG_FILE = "backup_log.txt"


def log_message(message):
    """Append a timestamped message to backup_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())


def get_timestamp_suffix():
    """Return current datetime as a string suffix for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup_file(source_file, backup_dir):
    """Copy a file to backup_dir with a timestamp suffix in the filename."""
    stem = source_file.stem        # filename without extension
    suffix = source_file.suffix    # extension like .csv
    timestamp = get_timestamp_suffix()

    # Example: sales_20250118_143000.csv
    new_name = f"{stem}_{timestamp}{suffix}"
    destination = backup_dir / new_name

    shutil.copy2(source_file, destination)
    log_message(f"Backed up: {source_file.name} -> {new_name}")


def rotate_backups(original_stem, backup_dir, extension):
    """Delete older backups if count exceeds MAX_BACKUPS."""
    # Find all backups that match pattern: original_stem_YYYYMMDD_HHMMSS.ext
    pattern = f"{original_stem}_*{extension}"
    existing_backups = sorted(backup_dir.glob(pattern))

    if len(existing_backups) > MAX_BACKUPS:
        # Delete oldest ones (sorted alphabetically = chronologically by timestamp)
        to_delete = existing_backups[: len(existing_backups) - MAX_BACKUPS]
        for old_file in to_delete:
            old_file.unlink()
            log_message(f"Deleted old backup: {old_file.name}")


def run_backup(source_dir_str, backup_dir_str):
    """Main backup function."""
    source_dir = Path(source_dir_str)
    backup_dir = Path(backup_dir_str)

    # Validate source directory
    if not source_dir.exists() or not source_dir.is_dir():
        log_message(f"ERROR: Source directory does not exist: {source_dir}")
        return

    # Create backup directory if it doesn't exist
    backup_dir.mkdir(parents=True, exist_ok=True)

    log_message(f"Starting backup: {source_dir} -> {backup_dir}")

    files_backed_up = 0

    # Iterate over files in source directory
    for file in source_dir.iterdir():
        if file.is_file() and file.suffix in BACKUP_EXTENSIONS:
            backup_file(file, backup_dir)
            rotate_backups(file.stem, backup_dir, file.suffix)
            files_backed_up += 1

    if files_backed_up == 0:
        log_message("No .csv or .json files found in source directory.")
    else:
        log_message(f"Backup complete. {files_backed_up} file(s) backed up.")


def main():
    if len(sys.argv) != 3:
        print("Usage: python backup_manager.py <source_directory> <backup_directory>")
        sys.exit(1)

    source = sys.argv[1]
    backup = sys.argv[2]

    run_backup(source, backup)


if __name__ == "__main__":
    main()
