from dataclasses import dataclass, field

from Engine.Core.EngineContext import EngineContext
from Engine.Core.Scenes import SceneManager
from Engine.Core.Scheduler import Scheduler
from Engine.Game.GameLoop import GameLoop
from Engine.Game.GameSetup import GameSetup

import pygame

@dataclass
class Game:
    EngineContext: EngineContext
    SceneManager: SceneManager
    Scheduler: Scheduler

    DISPLAY_WIDTH: int = 800
    DISPLAY_HEIGHT: int = 600

    Clock: pygame.time.Clock = field(default_factory =
        pygame.time.Clock()
    )

    RUNNING: bool = False

    def __post_init__(self):
        self.GameLoop: GameLoop = GameLoop(
            self.EngineContext,
            self.SceneManager,
            self.Scheduler
        )

    def build(self):
        pygame.init()

        self.EngineContext.RenderContext.Display = pygame.display.set_mode(
            (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        )

        self.RUNNING = True

    def run(self):
        while self.RUNNING:
            self.EngineContext.Time.deltaTime = self.Clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING = False

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.RUNNING = False

            self.GameLoop.update()

        self.shutdown()

        pygame.quit()

    def shutdown(self):
        if self.RUNNING:
            self.RUNNING = False

        self.EngineContext.SaveManager.save(
            self.EngineContext.Logger.saveLog(), "save"
        )

    def profiling(self):
        pass

def main() -> None:
    Setup = GameSetup()
    game = Setup.initializeEngine()

    game.build()
    game.run()

