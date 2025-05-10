cat = "XchanBik/Text"

import os

class TextLoadNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "base.txt"}),  # Path to your text file
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("loaded_text",)
    FUNCTION = "load_text_from_file"
    CATEGORY = cat

    def load_text_from_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return ("",)  # Return an empty string if the file is not found

        with open(file_path, "r") as file:
            loaded_text = file.read()

        return (loaded_text,)  # Return the content of the text file as a string
