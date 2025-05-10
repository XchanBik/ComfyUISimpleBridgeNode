class AnyType(str):
    """A special class that is always equal in not equal comparisons."""
    
    def __ne__(self, __value: object) -> bool:
        return False

class FlexibleType(dict):
    """
    A special class to make flexible nodes that accept any types.
    This is what enables our bridge store node to accept any input type and out any output type.
    """
    def __init__(self, type):
        self.type = type

    def __getitem__(self, key):
        return (self.type, )

    def __contains__(self, key):
        return True

# Create an instance of AnyType for use in node definitions
any_type = AnyType("*")


class ByPassTypeTuple(tuple):
    """
    A special class that will return additional "AnyType" strings beyond defined values.
    Useful for dynamic outputs.
    """
    def __getitem__(self, index):
        if index > len(self) - 1:
            return AnyType("*")
        return super().__getitem__(index)
