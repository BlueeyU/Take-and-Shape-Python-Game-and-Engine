from dataclasses import dataclass, field

from Engine.Core.EngineContext import EngineContext, RenderContext
from Engine.Core.Scenes import SceneManager
from Engine.Core.Scheduler import Scheduler
from Engine.Game import Game

from Events.CommandBus import CommandBus
from Events.EventBus import EventBus
from Debug.Logger import Logger
from Debug.DebugManager import DebugManager
from Engine.Core.SaveManager import SaveManager
from Assets.AssetManager import AssetManager
from Inputs.InputManager import InputManager
from Engine.Core.Time import Time
from FactoryGame.GameRegistration import AssetRegistry, SceneRegistry

import pygame

@dataclass
class GameSetup:
    EngineContext: EngineContext = field(default_factory = lambda:
        EngineContext(
            EventBus(),
            CommandBus(),
            Logger(),
            DebugManager(),
            Time(),
            SaveManager(),
            InputManager(),
            AssetManager(),
            RenderContext()
        )
    )

    SceneManager: SceneManager = field(default_factory =
        SceneManager
    )

    Scheduler: Scheduler = field(default_factory =
        Scheduler
    )

    def initializeScenes(self):
        SceneRegistry.register(self.SceneManager, self.EngineContext)

    def initializeAssets(self):
        AssetRegistry.register(self.EngineContext.AssetManager)

    def initializePygame(self):
        pygame.init()

        DISPLAY_WIDTH: int = 800
        DISPLAY_HEIGHT: int = 600

        self.EngineContext.RenderContext.Display = pygame.display.set_mode(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )

    def initialisation(self):
        self.initializePygame()
        self.initializeAssets()
        self.initializeScenes()

    def initializeEngine(self):
        game = Game.Game(
            self.EngineContext,
            self.SceneManager,
            self.Scheduler,
        )

        self.initialisation()

        return game