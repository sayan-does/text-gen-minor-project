# import os
# import pathlib


# def list_directory_branches(directory, level=0, prefix=''):
#     """
#     Recursively list directory branches, ignoring specified directories
#     """
#     # Directories to ignore
#     IGNORE_DIRS = {
#         'node_modules',
#         'packages',
#         '.git',
#         '.venv',
#         'venv',
#         '__pycache__',
#         'dist',
#         'build',
#         '.next',
#         '.nuxt',
#         '.svelte-kit',
#         'target'
#     }

#     try:
#         # Convert to Path object
#         path = pathlib.Path(directory)

#         # List all entries, sorted alphabetically
#         entries = sorted(
#             [entry for entry in path.iterdir()
#              if entry.name not in IGNORE_DIRS and
#              not entry.name.startswith('.')],
#             key=lambda x: x.name
#         )

#         # Total entries for last item tracking
#         total_entries = len(entries)

#         # Iterate through entries
#         for index, entry in enumerate(entries):
#             # Determine branch markers
#             is_last = (index == total_entries - 1)

#             # Create branch prefix
#             if is_last:
#                 branch_marker = '└── '
#                 new_prefix = prefix + '    '
#             else:
#                 branch_marker = '├── '
#                 new_prefix = prefix + '│   '

#             # Print current entry
#             print(f"{prefix}{branch_marker}{entry.name}")

#             # Recursively explore subdirectories
#             if entry.is_dir():
#                 list_directory_branches(entry, level + 1, new_prefix)

#     except PermissionError:
#         print(f"Permission denied to access: {directory}")
#     except FileNotFoundError:
#         print(f"Directory not found: {directory}")


# def main():
#     # Specify the directory to explore (current directory by default)
#     directory_path = '.'

#     print("Directory Structure:")
#     # Start listing directory branches
#     list_directory_branches(directory_path)


# if __name__ == "__main__":
#     main()
import os


def check_structure(base_path, expected_structure, parent_path=""):
    """
    Recursively checks the directory structure and files.
    Returns a list of missing items or discrepancies.
    """
    issues = []

    for key, value in expected_structure.items():
        current_path = os.path.join(base_path, key)
        relative_path = os.path.join(parent_path, key)

        if isinstance(value, dict):  # It's a directory
            if not os.path.isdir(current_path):
                issues.append(f"Missing directory: {relative_path}")
            else:
                sub_issues = check_structure(
                    current_path, value, relative_path)
                issues.extend(sub_issues)
        elif value == "File":  # It's a file
            if not os.path.isfile(current_path):
                issues.append(f"Missing file: {relative_path}")
        else:
            issues.append(
                f"Invalid structure type for {relative_path}: {value}")
    return issues


# Define the expected directory structure
expected_structure = {
    "backend": {
        "app": {
            "__init__.py": "File",
            "main.py": "File",
            "api": {
                "__init__.py": "File",
                "endpoints": {
                    "__init__.py": "File",
                    "chat.py": "File",
                    "document.py": "File",
                },
            },
            "core": {
                "__init__.py": "File",
                "config.py": "File",
                "settings.py": "File",
            },
            "models": {
                "__init__.py": "File",
                "chat.py": "File",
            },
            "services": {
                "__init__.py": "File",
                "audio_transcription.py": "File",
                "document_processing.py": "File",
                "language_model.py": "File",
                "plagiarism_detector.py": "File",
                "vector_store.py": "File",
            },
            "utils": {
                "__init__.py": "File",
                "file_handlers.py": "File",
            },
        },
        "requirements.txt": "File",
    },
    "frontend": {
        "README.md": "File",
        "eslint.config.js": "File",
        "package-lock.json": "File",
        "package.json": "File",
        "public": {
            "vite.svg": "File",
        },
        "src": {
            "App.css": "File",
            "App.jsx": "File",
            "assets": {
                "react.svg": "File",
            },
            "components": {
                "ChatSection.jsx": "File",
                "FileUpload.jsx": "File",
                "PlagiarismModal.jsx": "File",
            },
            "index.css": "File",
            "index.html": "File",
            "main.jsx": "File",
        },
        "vite.config.js": "File",
    },
    "directory_copy.py": "File",
}

# Path to your project directory
project_path = os.getcwd()  # Use the current directory or specify a custom path

# Check the structure
discrepancies = check_structure(project_path, expected_structure)

# Output results
if discrepancies:
    print("Discrepancies found in the directory structure:")
    for issue in discrepancies:
        print(f"- {issue}")
else:
    print("Directory structure matches the expected structure!")
