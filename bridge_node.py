# ComfyUI - mxToolkit - Max Smirnov 2024
import nodes

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")
