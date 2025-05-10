"""
Custom Reroute Node - A simple reroute node implementation for ComfyUI
"""

class CustomReroute:
    """A custom implementation of a reroute node"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}
    
    RETURN_TYPES = ("*",)
    FUNCTION = "reroute"
    CATEGORY = "SimpleBridgeNode"
    
    # This flag tells ComfyUI this node can receive any input type
    INPUT_IS_LIST = True
    
    def reroute(self, **kwargs):
        """Simply pass through whatever input is received"""
        # Get the first value from kwargs (if any)
        for value in kwargs.values():
            return (value,)
        
        # If no inputs connected, return None
        return (None,)

# These mappings are required by ComfyUI to register your nodes
NODE_CLASS_MAPPINGS = {
    "CustomReroute": CustomReroute
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomReroute": "Custom Reroute"
}

# Category mappings for organization in the node menu
NODE_CATEGORY_MAPPINGS = {
    "CustomReroute": "SimpleBridgeNode"
}
