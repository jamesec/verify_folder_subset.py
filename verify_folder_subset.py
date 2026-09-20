from pathlib import Path
import hashlib
from collections import defaultdict
import sys

if len(sys.argv) != 3:
    print("Usage: python3 compare_folders.py folder_001 folder_002")
    sys.exit(1)

FOLDER_001 = Path(sys.argv[1])
FOLDER_002 = Path(sys.argv[2])

CHUNK_SIZE = 1024 * 1024  # 1 MB


def sha256(path):
    """Return the SHA-256 hash of a file."""
    h = hashlib.sha256()

    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            h.update(chunk)

    return h.hexdigest()


def get_files(folder):
    """Return all regular files recursively."""
    return [
        p for p in folder.rglob("*")
        if p.is_file()
    ]


print("Scanning folders...\n")

files_001 = get_files(FOLDER_001)
files_002 = get_files(FOLDER_002)

print(f"Files in {FOLDER_001}: {len(files_001)}")
print(f"Files in {FOLDER_002}: {len(files_002)}")
print()

# Build a hash → list of files mapping for folder_001.
# Using a list handles duplicate files correctly.
hashes_001 = defaultdict(list)

print(f"Hashing {FOLDER_001}...")

for i, path in enumerate(files_001, 1):
    file_hash = sha256(path)
    hashes_001[file_hash].append(path)

    print(
        f"\r  {i}/{len(files_001)}",
        end="",
        flush=True
    )

print("\n")

# Check every file in folder_002 against folder_001
missing = []
matches = []

print(f"Checking {FOLDER_002}...\n")

for i, path in enumerate(files_002, 1):
    file_hash = sha256(path)

    if file_hash in hashes_001:
        matches.append((path, hashes_001[file_hash]))
    else:
        missing.append(path)

    print(
        f"\r  {i}/{len(files_002)}",
        end="",
        flush=True
    )

print("\n")
print("=" * 70)

print(f"Files in {FOLDER_002}:       {len(files_002)}")
print(f"Content matches found:     {len(matches)}")
print(f"Content NOT found:         {len(missing)}")

print("=" * 70)


if missing:
    print(f"\n❌ CONTENT MISSING FROM {FOLDER_001}:\n")

    for path in missing:
        print(f"  {path}")

else:
    print(f"\n✅ Every file in {FOLDER_002} exists in {FOLDER_001}.")
    print("   Filenames and folder locations were ignored.")
