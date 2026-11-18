from pathlib import Path
from integrity import calculate_sha256
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
WATCH_FOLDER = BASE_DIR / "monitored_files"
LOG_FOLDER = BASE_DIR / "logs"

LOG_FOLDER.mkdir(exist_ok=True)

REPORT_FILE = LOG_FOLDER / "integrity_report.txt"


def generate_report():
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write("SECURE FILE INTEGRITY REPORT\n")
        report.write("=" * 40 + "\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        for file_path in WATCH_FOLDER.rglob("*"):
            if file_path.is_file():
                try:
                    file_hash = calculate_sha256(file_path)
                    report.write(f"File: {file_path.name}\n")
                    report.write(f"SHA-256: {file_hash}\n")
                    report.write("-" * 40 + "\n")
                except OSError as error:
                    report.write(
                        f"Could not read {file_path.name}: {error}\n"
                    )

    print(f"Integrity report created: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()