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
                print(f"[SimpleBridge] Signaled completion for '{name}'")
    
    def get(self, name):
        with self.lock:
            # If data already exists, return it immediately
            if name in self.storage:
                print(f"[SimpleBridge] Retrieved existing data for '{name}'")
                return self.storage.get(name)
            
            # Create an event if it doesn't exist
            if name not in self.completion_events:
                self.completion_events[name] = threading.Event()
            
            # Return a blocker that will wait for the data
            print(f"[SimpleBridge] Created blocker for '{name}'")
            return BridgeExecutionBlocker(name, self)
    
    def wait_for_data(self, name, timeout=300):
        """Wait for data to be stored under the given name"""
        event = self.completion_events.get(name)
        if not event:
            return False
        
        result = event.wait(timeout)
        if result:
            return self.storage.get(name)
        return None
    
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
    def __init__(self, bridge_name, storage):
        self.bridge_name = bridge_name
        self.storage = storage
        print(f"[SimpleBridge] Load '{bridge_name}' waiting for store...")
    
    def wait(self):
        """Wait for data to be available and return success/failure"""
        value = self.storage.wait_for_data(self.bridge_name)
        if value is not None:
            print(f"[SimpleBridge] Load '{self.bridge_name}' received data")
            return True
        
        print(f"[SimpleBridge] Error: Timeout waiting for '{self.bridge_name}'")
        return False
    
    def get_execution_blockers(self):
        """Return this object as the blocker"""
        return [self]

    def get_value(self):
        """Get the value after waiting (called by ComfyUI)"""
        return self.storage.get(self.bridge_name)

# Reset bridge events when workflow starts
@PromptServer.instance.routes.post("/prompt")
async def bridge_reset_on_workflow_start(request):
    try:
        bridge_storage.reset()
        print("[SimpleBridge] Reset for new workflow execution")
    except Exception as e:
        print(f"[SimpleBridge] Reset error: {str(e)}")
    
    # Make sure we call the original handler
    orig_handler = getattr(PromptServer.instance, "orig_prompt_route", None)
    if orig_handler:
        return await orig_handler(request)
    
    # Fallback if original handler not found
    handler = PromptServer.instance.routes._resources[0]._routes[("POST", "/prompt")].handler
    return await handler(request)

# Store original handler if not already done
if not hasattr(PromptServer.instance, "orig_prompt_route"):
    PromptServer.instance.orig_prompt_route = PromptServer.instance.routes._resources[0]._routes[("POST", "/prompt")].handler

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
        try:
            if value is not None:
                bridge_storage.store(bridge_name, value)
                print(f"[SimpleBridge] Stored value under '{bridge_name}': {type(value)}")
            else:
                print(f"[SimpleBridge] Warning: Tried to store None under '{bridge_name}'")
        except Exception as e:
            print(f"[SimpleBridge] Store error: {str(e)}")
            traceback.print_exc()
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
        try:
            # Get the value from the bridge storage (might return a blocker)
            value = bridge_storage.get(bridge_name)
            
            # Return the value (or blocker)
            return (value,)
            
        except Exception as e:
            print(f"[SimpleBridge] Load error: {str(e)}")
            traceback.print_exc()
            # Return an empty list to avoid errors
            return ([],)
