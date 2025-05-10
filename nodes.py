bridge_store = {}
class BridgeStoreNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bridge_id": ("STRING", {"default": "my_key"}),
            },
            "optional": {
                "data_vae": ("VAE",),
                "data_model": ("MODEL",),
                "data_latent": ("LATENT",),
                "data_conditioning": ("CONDITIONING",),
                "data_image": ("IMAGE",),
                "data_string": ("STRING",),
                "data_any": ("ANY",),  # To accept any arbitrary type
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "store"
    CATEGORY = "SimpleBridgeNode"

    def store(self, bridge_id, data_vae=None, data_model=None, data_latent=None, data_conditioning=None, data_image=None, data_string=None, data_any=None):
        # Handle dynamic data type storage
        data = None
        data_type = None

        # Check which data is provided and store it
        if data_vae is not None:
            data = data_vae
            data_type = "VAE"
        elif data_model is not None:
            data = data_model
            data_type = "MODEL"
        elif data_latent is not None:
            data = data_latent
            data_type = "LATENT"
        elif data_conditioning is not None:
            data = data_conditioning
            data_type = "CONDITIONING"
        elif data_image is not None:
            data = data_image
            data_type = "IMAGE"
        elif data_string is not None:
            data = data_string
            data_type = "STRING"
        elif data_any is not None:
            data = data_any
            data_type = "ANY"
        else:
            raise ValueError("No valid data provided for the bridge store.")

        # Store the data with its type
        bridge_store[bridge_id] = {
            "data": data,
            "type": data_type
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

    RETURN_TYPES = ("ANY",)  # Default/fallback
    RETURN_NAMES = ("data",)
    FUNCTION = "load"
    CATEGORY = "SimpleBridgeNode"
    
    def load(self, bridge_id):
        if bridge_id not in bridge_store:
            raise ValueError(f"[BridgeLoadNode] ID '{bridge_id}' not found.")
        data = bridge_store[bridge_id]["data"]
        return (data,)

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
