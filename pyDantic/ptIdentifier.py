class TypeIdentifier:
    def __init__(self, name: str):
        self.name: str = name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"TypeIdentifier({self.name})"