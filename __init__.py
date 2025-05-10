"""
@title: SimpleBridgeNode
@nickname: SimpleBridgeNode
@description: A custom node for ComfyUI to store and retrieve data dynamically.
"""
from .Text import LoraTextLoader
from .Bridge import SimpleBridgeStoreNode, SimpleBridgeLoadNode
from .Hook import MinimalWorkflowInterceptor

def __init__(self):
    pass

# Node mapping
NODE_CLASS_MAPPINGS = {
    "SimpleBridgeStoreNode": SimpleBridgeStoreNode,
    "SimpleBridgeLoadNode": SimpleBridgeLoadNode,
    "LoraTextLoader": LoraTextLoader
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleBridgeStoreNode": "SimpleBridge Store",
    "SimpleBridgeLoadNode": "SimpleBridge Load",
    "LoraTextLoader": "LoraTextFile as String"
}

# Crée une instance de notre intercepteur
minimal_interceptor_instance = MinimalWorkflowInterceptor()
# Installe le hook
minimal_interceptor_instance.install()

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
