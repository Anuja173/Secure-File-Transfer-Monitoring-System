from datetime import datetime
from pathlib import Path
from integrity import calculate_sha256
from security_audit import record_audit_event
import logging
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Get the main project folder
BASE_DIR = Path(__file__).resolve().parent

# Folders used by our project
WATCH_FOLDER = BASE_DIR / "monitored_files"
LOG_FOLDER = BASE_DIR / "logs"

# Create folders if they do not exist
WATCH_FOLDER.mkdir(exist_ok=True)
LOG_FOLDER.mkdir(exist_ok=True)

# Save activity records in this file
LOG_FILE = LOG_FOLDER / "activity.log"
SENSITIVE_KEYWORDS = [
    "password",
    "confidential",
    "secret",
    "private",
]

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8"
)


class FileActivityHandler(FileSystemEventHandler):

    def record(self, action, file_path):
        message = f"{action}: {file_path}"
        print(message)
        logging.info(message)
        record_audit_event(message)
        file_name = Path(file_path).name.lower()

        if any(keyword in file_name for keyword in SENSITIVE_KEYWORDS):
            alert = f"ALERT: Sensitive filename detected: {file_name}"
            print(alert)
            logging.warning(alert)
            record_audit_event(alert)

        if any(keyword in file_name for keyword in SENSITIVE_KEYWORDS):
            alert = f"ALERT: Sensitive filename detected: {file_name}"
            print(alert)
            logging.warning(alert)

        if action in ("FILE CREATED", "FILE MODIFIED"):
            path = Path(file_path)

            if path.is_file():
                try:
                    file_hash = calculate_sha256(path)
                    hash_message = f"SHA-256: {file_hash}"
                    print(hash_message)
                    logging.info(hash_message)
                except OSError as error:
                    logging.warning(f"Could not calculate hash: {error}")

    def on_created(self, event):
        if not event.is_directory:
            self.record("FILE CREATED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.record("FILE MODIFIED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.record("FILE DELETED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.record(
                "FILE MOVED",
                f"{event.src_path} -> {event.dest_path}"
            )


if __name__ == "__main__":
    handler = FileActivityHandler()
    observer = Observer()

    observer.schedule(
        handler,
        str(WATCH_FOLDER),
        recursive=True
    )

    observer.start()

    print("Secure File Transfer Monitoring System started!")
    print(f"Monitoring folder: {WATCH_FOLDER}")
    print("Press Ctrl+C to stop monitoring.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")

    observer.join()