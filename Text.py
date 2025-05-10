cat = "XchanBik/Text"

import os
import folder_paths

def filter_files_by_extension(files: list[str], extension: str) -> list[str]:
    # Call the existing function
    filename_list, folders_all, timestamp = folder_paths.get_filename_list_("loras")
    
    # Filter the result by extension outside the base code
    return [file for file in filename_list if file.endswith(str)]
    
class LoraTextLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_file": (['None'] + filter_files_by_extension("loras", extension=".txt")),  # Load .txt files
            }
        }

    RETURN_TYPES = ("STRING",)  # We return the text as a string
    FUNCTION = "load_text"  # The function that will load the text	
    CATEGORY = cat

    def load_text(self, text_file):
        # Make sure the file is selected and exists
        if text_file == 'None' or not os.path.isfile(text_file):
            print(f"[LoraTextLoader] Error: The file {text_file} is not valid.")
            return ("",)  # Return an empty string in case of error

        try:
            # Read the content of the text file
            with open(text_file, "r") as f:
                content = f.read()
                print(f"[LoraTextLoader] Successfully loaded content from {text_file}")
                return (content,)  # Return the content as a string
        except Exception as e:
            print(f"[LoraTextLoader] Error loading file {text_file}: {e}")
            return ("",)
