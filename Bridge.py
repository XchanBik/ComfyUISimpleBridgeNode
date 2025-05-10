import comfy.model_management as model_management
import torch
import numpy as np
import os
import sys
import folder_paths
import copy
import json
import threading
import time
import traceback
from server import PromptServer
from nodes import ExecutionBlocker

cat = "XchanBik/Bridge"

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

# Enhanced global bridge storage with execution control
class BridgeStorage:
    def __init__(self):
        self.storage = {}
        self.completion_events = {}
        self.lock = threading.Lock()
    
    def store(self, name, data):
        with self.lock:
            self.storage[name] = data
            # Signal completion if there are waiting loads
            if name in self.completion_events:
                self.completion_events[name].set()
    
    def get(self, name):
        # Create an event if it doesn't exist
        with self.lock:
            if name not in self.completion_events:
                self.completion_events[name] = threading.Event()
            
            # If data already exists, return it immediately
            if name in self.storage:
                return self.storage.get(name)
            
            # Otherwise return a special object that will block execution
            return BridgeExecutionBlocker(name, self.completion_events[name])
    
    def has(self, name):
        return name in self.storage
    
    def reset(self):
        with self.lock:
            # Reset events but keep data for potential reuse
            for event in self.completion_events.values():
                event.clear()

# Create a global bridge storage instance
bridge_storage = BridgeStorage()

# Special execution blocker that works with ComfyUI's execution system
class BridgeExecutionBlocker(ExecutionBlocker):
    def __init__(self, bridge_name, event):
        self.bridge_name = bridge_name
        self.completion_event = event
        print(f"[SimpleBridge] Load '{bridge_name}' waiting for store...")
    
    def wait(self):
        timeout = 300  # 5 minute timeout
        while timeout > 0:
            if self.completion_event.wait(1):  # Wait up to 1 second
                print(f"[SimpleBridge] Load '{self.bridge_name}' received data")
                return True
            timeout -= 1
        
        print(f"[SimpleBridge] Error: Timeout waiting for '{self.bridge_name}' after 5 minutes")
        return False
    
    def get_execution_blockers(self):
        return [self]

# Reset bridge events when workflow starts
@PromptServer.instance.routes.post("/prompt")
async def bridge_reset_on_workflow_start(request):
    bridge_storage.reset()
    # Let the original handler process the request
    return await PromptServer.instance.orig_prompt_route(request)

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
        return ()

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
        # Get the value from the bridge storage - this may return a blocker
        value = bridge_storage.get(bridge_name)
        
        # If we get a normal value, just return it
        if not isinstance(value, BridgeExecutionBlocker):
            return (value,)
        
        # If we get a blocker, ComfyUI will handle it properly
        return (value,)
