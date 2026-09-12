from dataclasses import dataclass

from Engine.Game.Game import Game
from Engine.Inputs.InputManager import Key, MouseButton, InputAction


@dataclass
class GameSetup:
    Game: Game

    def setup(self):
        InputManager = self.Game.EngineContext.InputManager

        InputManager.ActionBind(InputAction.Escape, Key.ESCAPE)