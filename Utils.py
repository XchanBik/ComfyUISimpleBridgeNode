from folder_paths import recursive_search, folder_names_and_paths
import os
import time
import mimetypes
import logging
from typing import Literal, List
from collections.abc import Collection

def filter_files_by_extension(files: Collection[str], extensions: Collection[str]) -> list[str]:
    return sorted(list(filter(lambda a: os.path.splitext(a)[-1].lower() in extensions or len(extensions) == 0, files)))
  
def get_filename_list(folder_name: str, extension: str) -> tuple[list[str], dict[str, float], float]:
    output_list = set()
    global folder_names_and_paths
    folders = folder_names_and_paths[folder_name]
    output_folders = {}

    # Let's manually handle the extension filtering inside this loop
    for x in folders[0]:
        files, folders_all = recursive_search(x, excluded_dir_names=[".git"])
        
        # Debug print to verify filenames
        print(f"[get_filename_list] Files found: {files}")    
        
        # Instead of using filter_files_extensions, we now manually filter files by extensions
        extension_filtered_files = filter_files_by_extension(files, extension)  # Assuming folders[1] contains the extensions
        
        # Update the output list with the filtered files
        output_list.update(extension_filtered_files)
        
        # Merge folder info into output_folders
        output_folders.update(folders_all)

    return sorted(list(output_list)), output_folders, time.perf_counter()
