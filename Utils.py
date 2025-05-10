import os
import time
import mimetypes
import logging
from typing import Literal, List
from collections.abc import Collection

# --base-directory - Resets all default paths configured in folder_paths with a new base path
if args.base_directory:
    base_path = os.path.abspath(args.base_directory)
else:
    base_path = os.path.dirname(os.path.realpath(__file__))
models_dir = os.path.join(base_path, "models")

def recursive_search(directory: str) -> tuple[list[str], dict[str, float]]:
    if not os.path.isdir(directory):
        return [], {}
    result = []
    dirs = {}
    # Attempt to add the initial directory to dirs with error handling
    try:
        dirs[directory] = os.path.getmtime(directory)
    except FileNotFoundError:
        logging.warning(f"Warning: Unable to access {directory}. Skipping this path.")

    logging.debug("recursive file list on directory {}".format(directory))
    dirpath: str
    subdirs: list[str]
    filenames: list[str]

    for dirpath, subdirs, filenames in os.walk(directory, followlinks=True, topdown=True):
        subdirs[:] = [d for d in subdirs]
        for file_name in filenames:
            try:
                relative_path = os.path.relpath(os.path.join(dirpath, file_name), directory)
                result.append(relative_path)
            except:
                logging.warning(f"Warning: Unable to access {file_name}. Skipping this file.")
                continue

        for d in subdirs:
            path: str = os.path.join(dirpath, d)
            try:
                dirs[path] = os.path.getmtime(path)
            except FileNotFoundError:
                logging.warning(f"Warning: Unable to access {path}. Skipping this path.")
                continue
    logging.debug("found {} files".format(len(result)))
    return result, dirs

def filter_files_by_extension(files: Collection[str], extensions: Collection[str]) -> list[str]:
    return sorted(list(filter(lambda a: os.path.splitext(a)[-1].lower() in extensions or len(extensions) == 0, files)))
  
def get_filename_list(folder_name: str, extension: str) -> tuple[list[str], dict[str, float], float]:
    full_path = os.path.join(models_dir, folder_name)
    output_list = set
    folders = full_path
    output_folders = {}
    
    # Let's manually handle the extension filtering inside this loop
    files, folders_all = recursive_search(full_path)
        
    # Debug print to verify filenames
    print(f"[get_filename_list] Files found: {files}")    
        
    # Instead of using filter_files_extensions, we now manually filter files by extensions
    extension_filtered_files = filter_files_by_extension(files, extension)  # Assuming folders[1] contains the extensions
        
    # Update the output list with the filtered files
    output_list.update(extension_filtered_files)
        
    # Merge folder info into output_folders
    output_folders.update(folders_all)

    return sorted(list(output_list)), output_folders, time.perf_counter()
