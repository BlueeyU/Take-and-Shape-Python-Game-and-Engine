from dataclasses import dataclass, field
from enum import Enum
from ECS.System import System

class SystemType(Enum):
    RENDERING = 0
    PHYSICS = 1
    TICK = 2
    BACKGROUND = 3

@dataclass
class SystemManager:
    RenderingSystems: list = field(default_factory=list)
    PhysicsSystems: list = field(default_factory=list)
    TickSystems: list = field(default_factory=list)
    BackgroundSystems: list = field(default_factory=list)

    def addSystem(self, system: System, systemtype: SystemType):
        if systemtype == systemtype.RENDERING:
            
            if system not in self.RenderingSystems:
                self.RenderingSystems.append(system)
            else:
                raise Exception("System already added")

        elif systemtype == systemtype.PHYSICS:

            if system not in self.PhysicsSystems:
                self.PhysicsSystems.append(system)
            else:
                raise Exception("System already added")

        elif systemtype == systemtype.TICK:

            if system not in self.TickSystems:
                self.TickSystems.append(system)
            else:
                raise Exception("System already added")

        elif systemtype == systemtype.BACKGROUND:

            if system not in self.BackgroundSystems:
                self.BackgroundSystems.append(system)
            else:
                raise Exception("System already added")

    def removeSystem(self, system):
        if system in self.RenderingSystems:
            self.RenderingSystems.remove(system)

        elif system in self.PhysicsSystems:
            self.PhysicsSystems.remove(system)

        elif system in self.TickSystems:
            self.TickSystems.remove(system)

        elif system in self.BackgroundSystems:
            self.BackgroundSystems.remove(system)

        else:
            raise Exception("System already added")

    def clear(self):
        self.RenderingSystems = []
        self.PhysicsSystems = []
        self.TickSystems = []
        self.BackgroundSystems = []

    def RenderingTick(self):
        for system in self.RenderingSystems:
            system.update()

    def PhysicsTick(self):
        for system in self.PhysicsSystems:
            system.update()

    def Tick(self):
        for system in self.TickSystems:
            system.update()

    def BackgroundTick(self):
        for system in self.BackgroundSystems:
            system.update()