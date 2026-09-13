from dataclasses import dataclass, field

import pygame
from enum import Enum, auto
from Engine.Math import Math as math

class InputAction(Enum):
    MoveForward = auto()
    MoveBackward = auto()
    MoveLeft = auto()
    MoveRight = auto()
    Sneak = auto()
    Sprint = auto()

    OpenInventory = auto()
    BuildMode = auto()

    Escape = auto()
    Continue = auto()
    Interact = auto()
    Enter = auto()
    LeaveWindow = auto()

    OpenMap = auto()

class Key(Enum):
    E = pygame.K_e
    B = pygame.K_b
    R = pygame.K_r
    F = pygame.K_f
    Q = pygame.K_q
    TAB = pygame.K_TAB
    X = pygame.K_x
    C = pygame.K_c
    M = pygame.K_m
    Y = pygame.K_y

    PLUS = pygame.K_PLUS
    MINUS = pygame.K_MINUS

    W = pygame.K_w
    A = pygame.K_a
    S = pygame.K_s
    D = pygame.K_d

    SPACE = pygame.K_SPACE
    SHIFT = pygame.K_LSHIFT
    CTRL = pygame.K_LCTRL

    ESCAPE = pygame.K_ESCAPE
    ENTER = pygame.K_RETURN

    ZERO = pygame.K_0
    ONE = pygame.K_1
    TWO = pygame.K_2
    THREE = pygame.K_3
    FOUR = pygame.K_4
    FIVE = pygame.K_5
    SIX = pygame.K_6
    SEVEN = pygame.K_7
    EIGHT = pygame.K_8
    NINE = pygame.K_9

    F_ONE = pygame.K_F1
    F_TWO = pygame.K_F2
    F_THREE = pygame.K_F3
    F_FOUR = pygame.K_F4
    F_FIVE = pygame.K_F5
    F_SIX = pygame.K_F6
    F_SEVEN = pygame.K_F7
    F_EIGHT = pygame.K_F8
    F_NINE = pygame.K_F9
    F_TEN = pygame.K_F10
    F_ELEVEN = pygame.K_F11
    F_TWELVE = pygame.K_F12

class MouseButton(Enum):
    LEFT_CLICK = pygame.BUTTON_LEFT
    RIGHT_CLICK = pygame.BUTTON_RIGHT
    MIDDLE_CLICK = pygame.BUTTON_MIDDLE
    WHEEL_UP = pygame.BUTTON_WHEELUP
    WHEEL_DOWN = pygame.BUTTON_WHEELDOWN

@dataclass
class InputManager:
    Keys: set = field(default_factory=set)
    PreviousKeys: set = field(default_factory=set)

    MouseKeys: set = field(default_factory=set)
    MousePreviousKeys: set = field(default_factory=set)

    MousePosition: tuple = field(default_factory=tuple)

    KeyBindings: dict = field(default_factory=dict)

    def ActionBind(self, bind: InputAction, key: Key | MouseButton):
        if bind not in self.KeyBindings.keys():
            self.KeyBindings[bind] = key
        else:
            raise Exception(f"Key {bind} already bound to a different Key!")

    def IsActionPressed(self, bind: InputAction):
        key = self.KeyBindings.get(bind)

        if isinstance(key, Key):
            key = key.value
            return key in self.Keys and key not in self.PreviousKeys

        if isinstance(key, MouseButton):
            key = key.value
            return key in self.MouseKeys and key not in self.MousePreviousKeys

        return False

    def IsActionReleased(self, bind: InputAction):
        key = self.KeyBindings.get(bind)

        if isinstance(key, Key):
            key = key.value
            return key not in self.Keys and key in self.PreviousKeys

        if isinstance(key, MouseButton):
            key = key.value
            return key not in self.MouseKeys and key in self.MousePreviousKeys

        return False

    def IsActionDown(self, bind: InputAction):
        key = self.KeyBindings.get(bind)

        if isinstance(key, Key):
            key = key.value
            return key in self.Keys

        if isinstance(key, MouseButton):
            key = key.value
            return key in self.MouseKeys

        return False

    def Axis(self, bindX: InputAction, bindY: InputAction):
        return math.Util.normalize(
            1 if self.IsActionPressed(bindX) else 0,
            1 if self.IsActionPressed(bindY) else 0
        )

    def update(self):
        self.PreviousKeys = self.Keys.copy()
        self.MousePreviousKeys = self.MouseKeys.copy()

        self.processEvents()

    def processEvents(self):
        self.Keys = {
            key for key, pressed
            in enumerate(pygame.key.get_pressed())
            if pressed
        }

        self.MouseKeys = {
            key for key, pressed
            in enumerate(pygame.mouse.get_pressed())
            if pressed
        }

        self.MousePosition = pygame.mouse.get_pos()


