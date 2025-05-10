"""
@title: SimpleBridgeNode
@nickname: SimpleBridgeNode
@description: A custom node for ComfyUI to store and retrieve data dynamically.
"""

WEB_DIRECTORY = "./js"

from .bridge_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
