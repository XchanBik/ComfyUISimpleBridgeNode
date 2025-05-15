import os
import logging
from comfy.cli_args import args # For your custom path logic

if args.base_directory:
    user_base_path = os.path.abspath(args.base_directory)
else:
    user_base_path = os.path.dirname(os.path.realpath(__file__))
user_models_dir = os.path.join(user_base_path, "models")

# Log the determined models_dir for easier debugging by the 
logging.info(f"[SimpleTextFileSelector] Initialized. Custom 'user_models_dir' is set to: {user_models_dir}")

# --- Utility Function to List .txt Files ---
def get_files_with_ext(folder_name: str, extension: str) -> list[str]:
    """
    Scans a specific folder within the 'user_models_dir' for .{extension} files.
    Returns a list of filenames (relative to that subfolder) for the dropdown.
    """
    # user_models_dir is the global one defined above
    full_scan_path = os.path.join(user_models_dir, folder_name)
    
    if not os.path.isdir(full_scan_path):
        logging.warning(f"[SimpleTextFileSelector] Target subfolder for .txt files not found: {full_scan_path}. "
                        f"(This path is 'user_models_dir' / '{folder_name}')")
        return ["None"] # ComfyUI dropdowns expect a list; "None" is a safe default.
    
    txt_files_found = []
    try:
        for dirpath, _, filenames in os.walk(full_scan_path, followlinks=True):
            for filename in filenames:
                if filename.lower().endswith(extension):
                    relative_file_path = os.path.relpath(os.path.join(dirpath, filename), full_scan_path)
                    txt_files_found.append(relative_file_path)
    except Exception as e:
        logging.error(f"[SimpleTextFileSelector] Error occurred while scanning directory {full_scan_path}: {e}")
        return ["None"] 
    
    if not txt_files_found:
        logging.info(f"[SimpleTextFileSelector] No .txt files were found in {full_scan_path}.")
        return ["None"]
    
    logging.debug(f"[SimpleTextFileSelector] Found these .txt files in {full_scan_path}: {sorted(txt_files_found)}")
    return sorted(txt_files_found)
