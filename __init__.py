"""
@title: SimpleBridgeNode
@nickname: SimpleBridgeNode
@description: A custom node for ComfyUI to store and retrieve data dynamically.
"""
from .wai_illustrious_character_select import llm_prompt_gen_node, illustrious_character_select, illustrious_character_select_en, local_llm_prompt_gen
from .image_saver.image_saver import ImageSaver

def __init__(self):
    pass
    
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "IntMultiplication"         : IntMultiplication,

    "ImageSaverMira"                 : ImageSaver,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "IntMultiplication"         : "Integer Multiplication",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

from .xchanbik_nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
