bridge_store = {}

class BridgeStoreNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL", ),            
                "data": (["LATENT", "CONDITIONING", "IMAGE", "STRING", "ANY"],),
                "bridge_id": ("STRING", {"default": "my_key"})
            },
            "optional": {
                "vae": ("VAE",),
            }
        }
    RETURN_TYPES = ()
    FUNCTION = "store"

    CATEGORY = "SimpleBridgeNode"

    def store(self, data, bridge_id):
        # Store both data and its type for later use
        bridge_store[bridge_id] = {
            "data": data,
            "type": type(data).__name__
        }
        return ()


class BridgeLoadNode:
    @classmethod
    def INPUT_TYPES(cls):
        # Gather current keys in the store for dropdown UI
        key_list = list(bridge_store.keys())
        if not key_list:
            key_list = ["<no_data>"]

        return {
            "required": {
                "bridge_id": (key_list,)
            }
        }

    # Dynamically determine output type
    def get_return_types(self, bridge_id=None):
        if bridge_id in bridge_store:
            type_name = bridge_store[bridge_id]["type"]
            # Fallback: return as ANY if unknown
            return (type_name,) if type_name in {"LATENT", "CONDITIONING", "IMAGE", "STRING"} else ("ANY",)
        return ("ANY",)

    RETURN_TYPES = ("ANY",)  # Default/fallback
    RETURN_NAMES = ("data",)
    FUNCTION = "load"

    CATEGORY = "SimpleBridgeNode"

    def load(self, bridge_id):
        if bridge_id not in bridge_store:
            raise ValueError(f"[BridgeLoadNode] ID '{bridge_id}' not found.")
        return (bridge_store[bridge_id]["data"],)


NODE_CLASS_MAPPINGS = {
    "SimpleBridgeStore": BridgeStoreNode,
    "SimpleBridgeLoad": BridgeLoadNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleBridgeStore": "Simple Bridge Store",
    "SimpleBridgeLoad": "Simple Bridge Load",
}

NODE_CATEGORY_MAPPINGS = {
    "SimpleBridgeStore": "SimpleBridgeNode",
    "SimpleBridgeLoad": "SimpleBridgeNode",
}
