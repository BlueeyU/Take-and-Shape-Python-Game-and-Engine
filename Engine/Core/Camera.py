from dataclasses import dataclass
from Math import Math as math

@dataclass
class Camera:
    position: math.Vector2
    rotation: math.Degrees
    zoom: float
