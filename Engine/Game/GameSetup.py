from dataclasses import dataclass, field

from Engine.Core.EngineContext import EngineContext, RenderContext
from Engine.Core.Scenes import SceneManager
from Engine.Core.Scheduler import Scheduler
from Engine.Game.Game import Game

from Events.CommandBus import CommandBus
from Events.EventBus import EventBus
from Debug.Logger import Logger
from Debug.DebugManager import DebugManager
from Engine.Core.SaveManager import SaveManager
from Assets.AssetManager import AssetManager
from Inputs.InputManager import InputManager
from Engine.Core.Time import Time
from Game.GameRegistration import AssetRegistry, SceneRegistry

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
        SceneManager()
    )

    Scheduler: Scheduler = field(default_factory =
        Scheduler()
    )

    def createScenes(self):
        SceneRegistry.register(self.SceneManager)

    def initializeAssets(self):
        AssetRegistry.register(self.EngineContext.AssetManager)

    def initializeEngine(self):
        game = Game(
            self.EngineContext,
            self.SceneManager,
            self.Scheduler,
        )

        self.createScenes()
        self.initializeAssets()

        return game