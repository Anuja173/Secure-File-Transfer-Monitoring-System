import hashlib
from pathlib import Path


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


if __name__ == "__main__":
    file_name = input("Enter the file path: ").strip().strip('"')
    path = Path(file_name)

    if path.is_file():
        file_hash = calculate_sha256(path)

        print("\nFile:", path.name)
        print("SHA-256:", file_hash)
    else:
        print("Error: File not found. Please check the path.")