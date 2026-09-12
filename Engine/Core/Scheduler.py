from dataclasses import dataclass

@dataclass
class Scheduler:
    RenderingFramerate: int = 0 # Set 0 if no Limit
    PhysicsFramerate: int = 60
    TickRate: int = 20
    BackgroundRate: int = 2

    RenderingFrametime: float = 1 / RenderingFramerate if RenderingFramerate != 0 else 0
    PhysicsFrametime: float = 1 / PhysicsFramerate
    TickTime: float = 1 / TickRate
    BackgroundTime: float = 1 / BackgroundRate

    RenderingTimer: float = 0
    PhysicsTimer: float = 0
    TickTimer: float = 0
    BackgroundTimer: float = 0

    def update(self, DeltaTime: float):
        if not self.RenderingFramerate == 0:
            self.RenderingTimer += DeltaTime
        self.PhysicsTimer += DeltaTime
        self.TickTimer += DeltaTime
        self.BackgroundTimer += DeltaTime

    def renderReady(self):
        if self.RenderingFramerate == 0:
            return True

        if self.RenderingTimer >= self.RenderingFrametime:
            self.RenderingTimer -= self.RenderingFrametime
            return True
        return False

    def physicsReady(self):
        if self.PhysicsTimer >= self.PhysicsFrametime:
            self.PhysicsTimer -= self.PhysicsFrametime
            return True
        return False

    def tickReady(self):
        if self.TickTimer >= self.TickTime:
            self.TickTimer -= self.TickTime
            return True
        return False

    def backgroundReady(self):
        if self.BackgroundTimer >= self.BackgroundTime:
            self.BackgroundTimer -= self.BackgroundTime
            return True
        return False


