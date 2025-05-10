cat = "XchanBik/Bridge"

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




class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

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
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "store_value"
    CATEGORY = cat

    def store_value(self, bridge_name, value=None):
        if value is not None:
            bridge_storage.store(bridge_name, value)
            print(f"[SimpleBridge] Stored value under '{bridge_name}': {type(value)}")
        else:
            print(f"[SimpleBridge] Tried to store None under '{bridge_name}'")
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
    CATEGORY = cat

    def load_value(self, bridge_name):
        # Get the value from the bridge storage
        value = bridge_storage.get(bridge_name)

        if value is None:
            print(f"[SimpleBridge] '{bridge_name}' has no stored value")



        return (value,)
