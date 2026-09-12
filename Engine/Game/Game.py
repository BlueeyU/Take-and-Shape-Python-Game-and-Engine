from dataclasses import dataclass

from Engine.Core.EngineContext import EngineContext, RenderContext
from Engine.Core.Scenes import SceneManager
from Engine.Core.Scheduler import Scheduler
from Engine.Game.GameLoop import GameLoop

from Events.CommandBus import CommandBus
from Events.EventBus import EventBus
from Debug.Logger import Logger
from Debug.DebugManager import DebugManager
from Engine.Core.SaveManager import SaveManager
from Assets.AssetManager import AssetManager
from Inputs.InputManager import InputManager
from Engine.Core.Time import Time

import pygame

@dataclass
class Game:
    EngineContext: EngineContext
    SceneManager: SceneManager
    Scheduler: Scheduler

    DISPLAY_WIDTH: int = 800
    DISPLAY_HEIGHT: int = 600

    Clock: pygame.time.Clock = pygame.time.Clock()

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

        self.EngineContext.SaveManager.save(
            self.EngineContext.Logger.saveLog(), "save"
        )

        pygame.quit()

def main() -> None:
    SavePath = r"C:\Users\luisk\User provided code\Python Projects\Factory Engine\Engine\SaveFile\Savefile.json"
    LogPath = r"C:\Users\luisk\User provided code\Python Projects\Factory Engine\Engine\SaveFile\Logfile.txt"

    game = Game(
        EngineContext(
            EventBus(),
            CommandBus(),
            Logger(),
            DebugManager(),
            Time(),
            SaveManager(SavePath, LogPath),
            InputManager(),
            AssetManager(),
            RenderContext()
        ),
        SceneManager(),
        Scheduler()
    )

    game.build()
    game.run()

