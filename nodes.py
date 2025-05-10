import os
import json
from .utils import FlexibleType, any_type, AnyType

# Global storage dictionary for sharing data between nodes
bridge_store = {}

class BridgeStoreNode:
    """Store node that accepts any type of input and saves it with a unique identifier"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_id": ("STRING", {"default": "my_key"})
            },
            "optional": FlexibleType(any_type),
        }
        
    RETURN_TYPES = ()  # Store node doesn't return anything
    FUNCTION = "store"
    CATEGORY = "SimpleBridgeNode"
    
    def store(self, bridge_id, **kwargs):
        """Store any inputs passed to the node"""
        for key, value in kwargs.items():
            if key.startswith("any_") and value is not None:
                # Store both the data and metadata about its type
                bridge_store[bridge_id] = {
                    "data": value,
                    "input_name": key,
                    "type": type(value).__name__
                }
                break  # Only store the first non-None input
        
        return ()

class BridgeLoadNode:
    """Load node that returns data with the correct type based on the bridge_id"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_id": ("STRING", {"default": "my_key"})
            }
        }
        
    RETURN_TYPES = (any_type,)  # Return any type
    RETURN_NAMES = ('*',)
    FUNCTION = "load"
    CATEGORY = "SimpleBridgeNode"
    OUTPUT_NODE = True
    
    def load(self, bridge_id):
        """Load data from the bridge store by bridge_id"""
        if bridge_id not in bridge_store:
            print(f"[BridgeLoadNode] Warning: ID '{bridge_id}' not found.")
            return (None,)
            
        # Return the stored data
        return (bridge_store[bridge_id]["data"],)

# Node class mappings required by ComfyUI
NODE_CLASS_MAPPINGS = {
    "SimpleBridgeStore": BridgeStoreNode,
    "SimpleBridgeLoad": BridgeLoadNode,
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleBridgeStore": "Simple Bridge Store",
    "SimpleBridgeLoad": "Simple Bridge Load",
}

# Category mappings
NODE_CATEGORY_MAPPINGS = {
    "SimpleBridgeStore": "SimpleBridgeNode",
    "SimpleBridgeLoad": "SimpleBridgeNode",
}
