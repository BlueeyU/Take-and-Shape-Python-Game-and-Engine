from dataclasses import dataclass

@dataclass
class Command:
    pass

@dataclass
class SceneTermination(Command):
    Scene = None

@dataclass
class SceneLoaded(Command):
    Scene = None