# verify_folder_subset.py — One-Way Folder Content Checker
## Purpose
Use this script when you have two versions of a folder and already expect that the newer folder contains everything from the older folder, possibly with:
- New files added
- Files moved to different subfolders
- Files renamed
- Different folder structures

The script checks file contents, not filenames or locations.

For example:
```
folder_001 = newer / updated folder
folder_002 = older folder
```

The question being answered is:
> Does folder_001 contain every file that exists in folder_002?

## Usage
Place compare_folders.py somewhere convenient, then run:
```
python3 compare_folders.py folder_001 folder_002
```

The order matters:
```
first argument  = newer / destination folder
second argument = older / source folder
```

For example:
```
python3 compare_folders.py folder_001 folder_002
```

means:
> Check whether every file in folder_002 also exists somewhere inside folder_001.

## How the comparison works
The script recursively scans both folders and calculates a SHA-256 hash for every regular file.

It does **not** require:
- The same filename
- The same file extension
- The same subfolder
- The same directory structure

For example, these can still be recognized as the same file:
```
folder_002/old/report.pdf
folder_001/archive/2025/final_report.pdf
```

provided their contents are identical.

## Successful result
If everything from the older folder exists in the newer folder, the script reports:
```
✅ Every file in folder_002 exists in folder_001.
   Filenames and folder locations were ignored.
```

This means folder_002 is a content subset of folder_001.

If files are missing
If some files from folder_002 cannot be found by content in folder_001, the script reports:

```
❌ CONTENT MISSING FROM folder_001:
```

followed by the affected files.

Those files should be investigated before treating folder_002 as redundant.

## Important
This script compares regular file contents only.

It does not compare:
- Empty directories
- Directory structure
- Filenames
- File permissions
- File creation/modification dates
- Symlinks

Therefore, a successful result means:
> Every regular file's content in the older folder exists somewhere in the newer folder.

It does not mean the two folders are otherwise identical.

## Typical use case
If you have:
```
folder_001/    ← newer, larger, updated version
folder_002/    ← older version
```

run:
```
python3 compare_folders.py folder_001 folder_002
```

If the result is:
```
✅ Every file in folder_002 exists in folder_001.
   Filenames and folder locations were ignored.
```

then folder_002 contains no unique regular-file content that isn't already present in folder_001.
