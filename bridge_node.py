import comfy.model_management as model_management
import torch
import numpy as np
import os
import sys
import folder_paths
import copy
import json
import traceback
from server import PromptServer

# Global bridge storage
class BridgeStorage:
    def __init__(self):
        self.storage = {}
    
    def store(self, name, data):
        self.storage[name] = data
    
    def get(self, name):
        return self.storage.get(name)
    
    def has(self, name):
        return name in self.storage

# Create a global bridge storage instance
bridge_storage = BridgeStorage()

# Store Bridge Node
class SimpleBridgeStoreNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_name": ("STRING", {"default": "bridge1"})
            },
            "optional": {
                "value": (any, {}),
            }
        }
    
    RETURN_TYPES = (any,)
    RETURN_NAMES = ("value",)
    FUNCTION = "store_value"
    CATEGORY = "utils"
    
    def store_value(self, bridge_name, value=None):
        # Store the value in the bridge storage
        if value is not None:
            bridge_storage.store(bridge_name, value)
        
        # Return the value directly (passthrough)
        return (value,)

# Load Bridge Node
class SimpleBridgeLoadNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_name": ("STRING", {"default": "bridge1"})
            }
        }
    
    RETURN_TYPES = (any,)
    RETURN_NAMES = ("value",)
    FUNCTION = "load_value"
    CATEGORY = "utils"
    
    def load_value(self, bridge_name):
        # Get the value from the bridge storage
        value = bridge_storage.get(bridge_name)
        
        if value is None:
            print(f"Bridge '{bridge_name}' has no stored value")
        
        return (value,)

# Advanced version with dynamic output type
class SimpleBridgeDynamic:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_name": ("STRING", {"default": "bridge1"})
            }
        }
    
    # Use dynamic return types based on what's stored
    RETURN_TYPES = None
    FUNCTION = "load_value"
    CATEGORY = "utils"
    
    @classmethod
    def IS_CHANGED(cls, bridge_name):
        # This forces the node to always refresh
        return float("NaN")
    
    def load_value(self, bridge_name):
        value = bridge_storage.get(bridge_name)
        
        # Dynamic type handling
        if value is None:
            self.__class__.RETURN_TYPES = ("STRING",)
            return ("No value stored",)
        
        # Determine the return type based on the stored value
        if isinstance(value, torch.Tensor):
            self.__class__.RETURN_TYPES = ("TENSOR",)
        elif isinstance(value, str):
            self.__class__.RETURN_TYPES = ("STRING",)
        elif isinstance(value, int):
            self.__class__.RETURN_TYPES = ("INT",)
        elif isinstance(value, float):
            self.__class__.RETURN_TYPES = ("FLOAT",)
        elif isinstance(value, list):
            self.__class__.RETURN_TYPES = ("LIST",)
        else:
            # Default case
            self.__class__.RETURN_TYPES = (any,)
        
        return (value,)

# Node mapping
NODE_CLASS_MAPPINGS = {
    "SimpleBridgeStoreNode": SimpleBridgeStoreNode,
    "SimpleBridgeLoadNode": SimpleBridgeLoadNode,
    "SimpleBridgeDynamic": SimpleBridgeDynamic
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleBridgeStoreNode": "SimpleBridge Store",
    "SimpleBridgeLoadNode": "SimpleBridge Load",
    "SimpleBridgeDynamic": "SimpleBridge Dynamic"
}
