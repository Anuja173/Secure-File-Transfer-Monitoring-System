import json
from pathlib import Path
from integrity import calculate_sha256

BASE_DIR = Path(__file__).resolve().parent
WATCH_FOLDER = BASE_DIR / "monitored_files"
LOG_FOLDER = BASE_DIR / "logs"

LOG_FOLDER.mkdir(exist_ok=True)

BASELINE_FILE = LOG_FOLDER / "hash_baseline.json"


def get_current_hashes():
    hashes = {}

    for file_path in WATCH_FOLDER.rglob("*"):
        if file_path.is_file():
            try:
                relative_path = str(file_path.relative_to(WATCH_FOLDER))
                hashes[relative_path] = calculate_sha256(file_path)
            except OSError:
                print(f"Could not read: {file_path.name}")

    return hashes


def main():
    current_hashes = get_current_hashes()

    if not BASELINE_FILE.exists():
        with open(BASELINE_FILE, "w", encoding="utf-8") as file:
            json.dump(current_hashes, file, indent=4)

        print("Initial hash baseline saved.")
        print("Run this program again later to check for changes.")
        return

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        old_hashes = json.load(file)

    for name in current_hashes:
        if name not in old_hashes:
            print(f"NEW FILE: {name}")
        elif current_hashes[name] != old_hashes[name]:
            print(f"FILE CHANGED: {name}")

    for name in old_hashes:
        if name not in current_hashes:
            print(f"FILE MISSING: {name}")

    print("Change detection complete.")


if __name__ == "__main__":
    main()