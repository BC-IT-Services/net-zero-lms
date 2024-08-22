import os
import zipfile
import shutil
import re

def unzip_all_files(directory):
    """Unzips all .zip files in the current directory."""

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)

        if full_path.endswith('.zip'):            
            with zipfile.ZipFile(full_path, 'r') as zip_ref:
                zip_ref.extractall(directory)  # Extract to the current directory

def remove_files_except_raw(directory, is_parent=True):
    """
    Recursively removes all files in subdirectories except those containing 'raw' 
    in their filename. Skips file removal in the parent directory.

    Args:
        directory: The path to the directory to process.
        is_parent: Flag to indicate if the current directory is the parent.
    """

    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)

        if os.path.isfile(full_path):
            if not is_parent and 'raw' not in full_path and '.venv' not in full_path and '.git' not in full_path and full_path[2:8] != 'module' and full_path[2:8] != 'modiwl':
                os.remove(full_path)
            elif is_parent and '.zip' in full_path:
                os.remove(full_path)
        elif os.path.isdir(full_path):
            remove_files_except_raw(full_path, is_parent=False)

def unzip_recursively():

    directory = '.'
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)

        if os.path.isdir(full_path) and '.git' not in full_path and '.venv' not in full_path and full_path[2:8] != 'module' and full_path[2:8] != 'modiwl':
            print(full_path)
            if 'module' in full_path.lower():
                module_slug = f"module-{full_path.split("\\")[1].split(' - ')[0].split(" ")[1].replace('.','-')}"
            elif 'modiwl' in full_path.lower():
                module_slug = f"modiwl-{full_path.split("\\")[1].split(' - ')[0].split(" ")[1].replace('.','-')}"
            new_path = os.path.join(directory, module_slug)
            os.rename(full_path, new_path)
            unzip_all_files(new_path)
            move_content_up(new_path)
            remove_zip_in_module_dirs(new_path)
    
def move_content_up(root_dir):
    """
    Moves all files from 'content' subdirectories up one level in the given root directory.
    """

    for module_dir in os.listdir(root_dir):
        module_path = os.path.join(root_dir, module_dir)
        if os.path.isdir(module_path):  # Ensure it's a directory
            if os.path.exists(module_path):
                for item in os.listdir(module_path):
                    item_path = os.path.join(module_path, item)
                    shutil.move(item_path, root_dir)  # Move item up one level
                os.rmdir(module_path)  # Remove empty 'content' directory

def remove_zip_in_module_dirs(root_dir):
    """
    Recursively enters directories starting with 'module-' and removes any '.zip' files found within.
    """

    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)

        if full_path[2:8] == 'module' or full_path[2:8] == 'modiwl':
            if full_path.lower().endswith('.zip'):
                os.remove(full_path)

unzip_all_files('.')
remove_files_except_raw('.')
unzip_recursively()