from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
LOG_FOLDER = BASE_DIR / "logs"
LOG_FOLDER.mkdir(exist_ok=True)

AUDIT_FILE = LOG_FOLDER / "security_audit.log"


def record_audit_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} | {event}\n")

    print("Audit event recorded.")


if __name__ == "__main__":
    record_audit_event("Security audit system test")