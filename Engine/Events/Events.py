from dataclasses import dataclass
from Math import Math as math

@dataclass
class Event:
    pass

@dataclass
class KeyPressedEvent(Event):
    key: str

@dataclass
class MousePressedEvent(Event):
    key: str
    pos: math.Vector2

@dataclass
class SceneTerminationEvent(Event):
    Scene = None

@dataclass
class SceneLoadedEvent(Event):
    Scene = None

@dataclass
class LoadingEvent(Event):
    pass