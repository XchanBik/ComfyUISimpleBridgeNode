cat = "XchanBik/Text"

import os
import folder_paths

def filter_files_by_extension(files: list[str], extension: str) -> list[str]:
    # Call the existing function
    filename_list, folders_all, timestamp = folder_paths.get_filename_list_("loras")
    
    # Filter the result by extension
    return [file for file in filename_list if file.endswith(extension)]
    
class LoraTextLoader:
    @classmethod
    def INPUT_TYPES(cls):        
        lora_list = filter_files_by_extension("loras", extension=".txt")
        if 0 == len(lora_list):
            lora_list.insert(0, "None")
        return {
            "required": {
                "lora_name": (lora_list, ),
            }
        }

    RETURN_TYPES = ("STRING",)  # We return the text as a string
    FUNCTION = "load_text"  # The function that will load the text	
    CATEGORY = cat

    def load_text(self, lora_name):
        # Make sure the file is selected and exists
        if "None" == lora_name:
            print(f"[LoraTextLoader] Error: The file {lora_name} is not valid.")
            return ("",)  # Return an empty string in case of error

        lora_path = folder_paths.get_full_path("loras", lora_name)
        try:
            # Read the content of the text file
            with open(lora_path, "r") as f:
                content = f.read()
                print(f"[LoraTextLoader] Successfully loaded content from {lora_path}")
                return (content,)  # Return the content as a string
        except Exception as e:
            print(f"[LoraTextLoader] Error loading file {lora_path}: {e}")
            return ("",)
