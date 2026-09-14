from dataclasses import dataclass

from Math import Math as math

@dataclass
class Transform: # A Component which stores the Position of its Entity
    position: math.Vector2
    rotation: math.Degrees
    scale: float

@dataclass
class PreviousTransform: # A Component which stores the Previous Position of its Entity
    position: math.Vector2
    rotation: math.Degrees
    scale: float

@dataclass
class Velocity: # A Component which changes the POSITION of its Entity over time
    velocity: math.Vector2

@dataclass
class Acceleration: # A Component which changes the VELOCITY of its Entity over time
    acceleration: math.Vector2

@dataclass
class Speed: # TEMPORARY -> belongs in FactoryGame Specific Components
    speed: int

@dataclass
class Sprite: # A Component which gives an Entity a sprite that will be rendered
    textureName: str
    flipX: bool = False
    flipY: bool = False
    layer: int = 0

@dataclass
class Collider: # A Component which gives an Entity a collision box that automatically resolves the Collision
    width: float
    height: float
    offsetX: float = 0.0
    offsetY: float = 0.0

@dataclass
class Script: # A Component which uses a Self written Script that can do precise behaviour for many applications of your need but is less performing
    script: list

# Entity Types
@dataclass
class PlayerCharacter: # An Entity which is Standardly Controlled by a Player
    pass

@dataclass
class PlayableCharacter: # An Entity which -can- be controlled but must not
    pass

@dataclass
class IntelligentCharacter: # Needs an AI or some way of Intelligent behaviour
    pass

@dataclass
class Interpolated: # Gets Interpolated in Rendering
    pass

@dataclass
class Element: # An Entity which is either a Container, an UI Element or some sort of Element that does not need physics or does not get rendered
    pass

@dataclass
class NetworkShared: # An Entity which is shared across the Network
    pass
