# ComfyUI/custom_nodes/minimal_hook_extension.py

import types
import json # Pour un affichage lisible du workflow

# --- Récupération de l'instance de PromptServer ---
# Ceci est la manière standard dont les composants de ComfyUI accèdent à l'instance du serveur.
# Cela suppose que server.py de ComfyUI a initialisé PromptServer.instance.
PROMPT_SERVER_INSTANCE = None
try:
    # Importe le module 'server' de ComfyUI
    import server
    if hasattr(server, 'PromptServer') and hasattr(server.PromptServer, 'instance'):
        PROMPT_SERVER_INSTANCE = server.PromptServer.instance
        print("MINIMAL HOOK: Instance de PromptServer trouvée.")
    else:
        print("MINIMAL HOOK: 'server.PromptServer.instance' non trouvée après l'import du module 'server'.")
except ImportError:
    print("MINIMAL HOOK: Impossible d'importer le module 'server'. Le hook ne peut pas être installé de cette manière.")
except Exception as e:
    print(f"MINIMAL HOOK: Erreur lors de la récupération de l'instance du serveur : {e}")

# --- Classe pour gérer l'interception ---
class MinimalWorkflowInterceptor:
    def __init__(self):
        self.original_queue_prompt_method = None
        if PROMPT_SERVER_INSTANCE:
            # Stocke la méthode originale. Elle est déjà liée à PROMPT_SERVER_INSTANCE.
            self.original_queue_prompt_method = PROMPT_SERVER_INSTANCE.queue_prompt
            print("MINIMAL HOOK (init): Méthode originale 'queue_prompt' stockée.")
        else:
            print("MINIMAL HOOK (init): Instance de PromptServer non disponible lors de l'initialisation de l'intercepteur.")

    def hooked_queue_prompt(self, server_instance_passed_by_type, *args, **kwargs):
        """
        Cette méthode remplacera PromptServer.instance.queue_prompt.
        Le premier argument 'server_instance_passed_by_type' sera l'instance de PromptServer,
        car types.MethodType lie cette méthode à cette instance.
        'self' ici est l'instance de MinimalWorkflowInterceptor.
        """
        print("\n=====================================================================")
        print(f"MINIMAL HOOK: Appel à 'queue_prompt' intercepté ! (ID intercepteur: {id(self)})")
        # print(f"Instance de PromptServer sur laquelle le hook est appelé: {id(server_instance_passed_by_type)}")

        if args:
            workflow = args[0]  # Le 'prompt' (workflow) est généralement le premier argument.
            client_id = args[1] if len(args) > 1 else "ID Client Inconnu"

            print(f"ID Client: {client_id}")
            print(f"Type de données du Workflow: {type(workflow)}")

            if isinstance(workflow, dict):
                print(f"Nombre de nœuds dans le workflow: {len(workflow)}")
                print("Les 3 premiers nœuds (ou tous si moins de 3):")
                node_count = 0
                for node_id, node_data in workflow.items():
                    print(f"  ID Nœud: {node_id}")
                    print(f"    Type de Classe: {node_data.get('class_type', 'N/A')}")
                    # Pourrait être verbeux : print(f"    Inputs: {node_data.get('inputs', {})}")
                    node_count += 1
                    if node_count >= 3:
                        if len(workflow) > 3:
                            print("    ... (et potentiellement d'autres nœuds)")
                        break
                # Option pour afficher une partie du JSON (peut être très long pour de gros workflows)
                # print("Workflow (extrait JSON du premier noeud):")
                # if workflow:
                #     first_node_id = next(iter(workflow))
                #     print(json.dumps({first_node_id: workflow[first_node_id]}, indent=2, default=str))
            else:
                print(f"Données du workflow (brutes): {workflow}")
        else:
            print("MINIMAL HOOK: Aucun argument positionnel reçu dans le hook.")

        print("MINIMAL HOOK: Appel de la méthode originale 'queue_prompt'...")
        print("=====================================================================\n")

        if self.original_queue_prompt_method:
            # Appelle la méthode originale stockée.
            # Elle est déjà liée à la bonne instance de PromptServer.
            return self.original_queue_prompt_method(*args, **kwargs)
        else:
            # Cela ne devrait pas arriver si l'installation a réussi.
            print("ERREUR MINIMAL HOOK: Méthode originale 'queue_prompt' non trouvée dans l'instance de l'intercepteur!")
            raise RuntimeError("MINIMAL HOOK: Méthode originale 'queue_prompt' non disponible.")

    def install(self):
        """Installe le hook sur l'instance de PromptServer."""
        if not PROMPT_SERVER_INSTANCE:
            print("MINIMAL HOOK (install): Instance de PromptServer non disponible. Le hook ne peut pas être installé.")
            return

        if not self.original_queue_prompt_method:
            print("MINIMAL HOOK (install): Méthode 'queue_prompt' originale non capturée lors de l'init. Installation annulée.")
            return
        
        # Vérifier si le hook est déjà le nôtre pour éviter de patcher plusieurs fois
        # Note: PROMPT_SERVER_INSTANCE.queue_prompt.__func__ == self.hooked_queue_prompt ne marche pas directement
        # à cause de la liaison par types.MethodType. Une façon simple est d'utiliser un flag.
        if hasattr(PROMPT_SERVER_INSTANCE.queue_prompt, '_hooked_by_minimal_interceptor'):
             print("MINIMAL HOOK (install): Hook déjà installé par MinimalWorkflowInterceptor. Annulation.")
             return

        try:
            # Remplace la méthode sur l'instance de PROMPT_SERVER_INSTANCE par notre méthode 'hooked_queue_prompt'.
            # types.MethodType fait en sorte que 'hooked_queue_prompt' se comporte comme une méthode de PROMPT_SERVER_INSTANCE.
            PROMPT_SERVER_INSTANCE.queue_prompt = types.MethodType(self.hooked_queue_prompt, PROMPT_SERVER_INSTANCE)
            
            # Marquer la méthode hookée pour éviter de la patcher à nouveau
            PROMPT_SERVER_INSTANCE.queue_prompt._hooked_by_minimal_interceptor = True
            
            print("MINIMAL HOOK: Hook 'queue_prompt' installé avec succès sur PromptServer.instance.")
        except Exception as e:
            print(f"MINIMAL HOOK: Échec de l'installation du hook : {e}")
            # Tenter de restaurer si le patch a échoué et que l'original a été stocké
            if self.original_queue_prompt_method:
                PROMPT_SERVER_INSTANCE.queue_prompt = self.original_queue_prompt_method
                print("MINIMAL HOOK: Tentative de restauration de la méthode originale 'queue_prompt' suite à une erreur d'installation.")
