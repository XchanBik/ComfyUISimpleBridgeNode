cat = "XchanBik/Text"

import os
import folder_paths
from .Utils import get_files_with_ext
    
class LoraTextLoader:
    @classmethod
    def INPUT_TYPES(cls):        
        lora_list = get_files_with_ext("loras", ".txt")
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
