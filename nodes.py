"""
SimpleBridge - A node system that allows you to bridge connections across distant parts of a workflow.
Based directly on ComfyUI's Reroute node implementation.
"""

# Global storage dictionary for sharing data between nodes
bridge_store = {}

class BridgeStoreNode:
    """Store node that accepts any input and saves it with a unique identifier"""
     
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}  
    # Flag that tells ComfyUI this node can accept any input type
    INPUT_IS_LIST = True      
    
    RETURN_TYPES = ()
    FUNCTION = "store"
    CATEGORY = "SimpleBridgeNode"
    
    
    def store(self, bridge_id, **kwargs):
        """Store the input data with the given bridge_id"""
        # Extract the first input value that isn't bridge_id
        for key, value in kwargs.items():
            if key != 'bridge_id':
                # Store both the value and its type information
                bridge_store[bridge_id] = {
                    "value": value,
                    "type_name": key  # The key contains the input type information
                }
                break
        
        return ()

class BridgeLoadNode:
    """Load node that returns data with the correct type based on bridge_id"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_id": ("STRING", {"default": "my_key"})
            }
        }
    
    # The wildcard type - tells ComfyUI this can output any type
    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("data",)
    FUNCTION = "load"
    CATEGORY = "SimpleBridgeNode"
    
    def load(self, bridge_id):
        """Load data from the bridge store by bridge_id"""
        if bridge_id not in bridge_store:
            print(f"[BridgeLoadNode] Warning: ID '{bridge_id}' not found.")
            return (None,)
        
        # Return the stored value
        return (bridge_store[bridge_id]["value"],)

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

# Category mappings for organization in the node menu
NODE_CATEGORY_MAPPINGS = {
    "SimpleBridgeStore": "SimpleBridgeNode",
    "SimpleBridgeLoad": "SimpleBridgeNode",
}
