import os
from pathlib import Path
import sys


def generate_directory_structure(startpath, exclude_dirs=None):
    """
    Generate a tree-like directory structure string.

    Args:
        startpath (str): The root directory to start mapping
        exclude_dirs (list): List of directory names to exclude (e.g., ['venv', '__pycache__'])
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '__pycache__', '.git', 'node_modules']

    # Convert startpath to absolute path
    startpath = os.path.abspath(startpath)

    # Check if path exists
    if not os.path.exists(startpath):
        print(f"Error: Directory '{startpath}' does not exist")
        print(f"Current working directory: {os.getcwd()}")
        sys.exit(1)

    output = []
    output.append(f"Project structure for: {startpath}\n")

    for root, dirs, files in os.walk(startpath):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level

        # Only add directory name, not full path
        dirname = os.path.basename(root)
        if dirname:  # Skip empty directory names
            output.append(f'{indent}├── {dirname}/')

        subindent = '│   ' * (level + 1)
        for file in sorted(files):  # Sort files for consistent output
            if not any(file.endswith(ext) for ext in ['.pyc']):
                output.append(f'{subindent}├── {file}')

    return '\n'.join(output)


# Example usage
if __name__ == "__main__":
    # Get the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        print("Django Project Structure:")
        print(generate_directory_structure(script_dir))
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script location: {script_dir}")