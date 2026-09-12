from dataclasses import dataclass

from Engine.Core.EngineContext import EngineContext
from Engine.Core.Scenes import SceneManager
from Engine.Core.Scheduler import Scheduler


@dataclass
class GameLoop:
    EngineContext: EngineContext
    SceneManager: SceneManager
    Scheduler: Scheduler

    MAX_PHYSICS_LOOPS: int = 2
    MAX_TICK_LOOPS: int = 2
    MAX_BACKGROUND_LOOPS: int = 3

    def update(self):
        Scene = self.SceneManager.ActiveScene

        if Scene is None:
            return

        scheduler = self.Scheduler

        scheduler.update(
            self.EngineContext.Time.deltaTime
        )

        self.EngineContext.InputManager.update()

        backgroundLoopCount = 0
        while scheduler.backgroundReady() and backgroundLoopCount < self.MAX_BACKGROUND_LOOPS:
            Scene.SystemManager.BackgroundTick()
            backgroundLoopCount += 1

        tickLoopCount = 0
        while scheduler.tickReady() and tickLoopCount < self.MAX_TICK_LOOPS:
            Scene.SystemManager.Tick()
            tickLoopCount += 1

        physicsLoopCount = 0
        while scheduler.physicsReady() and physicsLoopCount < self.MAX_PHYSICS_LOOPS:
            Scene.SystemManager.PhysicsTick()
            physicsLoopCount += 1

        self.EngineContext.RenderContext.Alpha = (
            scheduler.PhysicsTimer / scheduler.PhysicsFrametime
        )

        if scheduler.renderReady():
            Scene.SystemManager.RenderingTick()

        self.EngineContext.EventBus.clear()

