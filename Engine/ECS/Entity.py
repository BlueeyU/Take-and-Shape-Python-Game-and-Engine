from dataclasses import dataclass

@dataclass
class Entity:
    id: int

# An Entity is a Single ID, it allows for optimal Cache efficiency