"""
@title: SimpleBridgeNode
@nickname: SimpleBridgeNode
@description: A custom node for ComfyUI to store and retrieve data dynamically.
"""
from .Text import SimpleTextLoader
from .Bridge import SimpleBridgeStoreNode, SimpleBridgeLoadNode

def __init__(self):
    pass
    
# Node mapping
NODE_CLASS_MAPPINGS = {
    "SimpleBridgeStoreNode": SimpleBridgeStoreNode,
    "SimpleBridgeLoadNode": SimpleBridgeLoadNode,
    "SimpleTextLoader": TextLoadNode
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleBridgeStoreNode": "SimpleBridge Store",
    "SimpleBridgeLoadNode": "SimpleBridge Load",
    "SimpleTextLoader": "FileText as String"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
