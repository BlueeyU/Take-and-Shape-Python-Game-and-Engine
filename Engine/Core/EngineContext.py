from dataclasses import dataclass
import pygame

from Events.CommandBus import CommandBus
from Events.EventBus import EventBus
from Debug.Logger import Logger
from Debug.DebugManager import DebugManager
from Engine.Core.SaveManager import SaveManager
from Assets.AssetManager import AssetManager
from Inputs.InputManager import InputManager
from Engine.Core.Time import Time

@dataclass
class RenderContext:
    Display: pygame.Surface = None
    Alpha: float = 0.0

@dataclass
class EngineContext:
    EventBus: EventBus
    CommandBus: CommandBus

    Logger: Logger
    DebugManager: DebugManager

    Time: Time

    SaveManager: SaveManager

    InputManager: InputManager

    AssetManager: AssetManager

    RenderContext: RenderContext
