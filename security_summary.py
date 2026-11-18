from pathlib import Path
from collections import Counter
from contextlib import redirect_stdout

BASE_DIR = Path(__file__).resolve().parent
LOG_FOLDER = BASE_DIR / "logs"
AUDIT_FILE = BASE_DIR / "logs" / "security_audit.log"

def generate_summary():
    if not AUDIT_FILE.exists():
        print("Security audit log not found.")
        return

    with open(AUDIT_FILE, "r", encoding="utf-8") as file:
        entries = file.readlines()

    print("\nSECURITY ACTIVITY SUMMARY")
    print("=" * 35)
    print(f"Total audit entries: {len(entries)}")

    event_types = Counter()

    for entry in entries:
        if " | " in entry:
            event = entry.split(" | ", 1)[1]

            if "ALERT:" in event:
                event_types["Sensitive file alerts"] += 1
            elif "FILE CREATED:" in event:
                event_types["Files created"] += 1
            elif "FILE MODIFIED:" in event:
                event_types["Files modified"] += 1
            elif "FILE DELETED:" in event:
                event_types["Files deleted"] += 1
            elif "FILE MOVED:" in event:
                event_types["Files moved"] += 1

    for event, count in event_types.items():
        print(f"{event}: {count}")

if __name__ == "__main__":
    report_file = LOG_FOLDER / "security_summary.txt"

    with open(report_file, "w", encoding="utf-8") as report:
        with redirect_stdout(report):
            generate_summary()

    print(f"Security summary saved to: {report_file}")