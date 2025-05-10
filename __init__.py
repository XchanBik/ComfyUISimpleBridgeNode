"""
@title: SimpleBridgeNode
@nickname: SimpleBridgeNode
@description: A custom node for ComfyUI to store and retrieve data dynamically.
"""
from .Text import LoraTextLoader
from .Bridge import SimpleBridgeStoreNode, SimpleBridgeLoadNode

def __init__(self):
    pass

# --- Logique d'installation ---
# Ce code s'exécute lorsque ComfyUI charge ce fichier depuis custom_nodes.
if PROMPT_SERVER_INSTANCE:
    # Crée une instance de notre intercepteur
    minimal_interceptor_instance = MinimalWorkflowInterceptor()
    # Installe le hook
    minimal_interceptor_instance.install()
else:
    # Ce message est important pour que l'utilisateur le voie si la configuration échoue.
    print("\n" + "="*70)
    print("MINIMAL HOOK EXTENSION: Instance de PromptServer NON TROUVÉE au chargement du module.")
    print("Le hook pour 'queue_prompt' N'A PAS ÉTÉ INSTALLÉ.")
    print("Cela signifie généralement que l'environnement du serveur ComfyUI n'est pas celui attendu,")
    print("ou que ce script est chargé avant que 'PromptServer.instance' ne soit prêt.")
    print("Si ComfyUI démarre normalement, vérifiez la console pour les messages 'MINIMAL HOOK' précédents.")
    print("="*70 + "\n")

# Message final pour confirmer le chargement du module
print("MINIMAL HOOK EXTENSION: Module chargé.")

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

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
