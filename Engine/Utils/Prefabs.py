from ECS import Component as component
from Math import Math as math
import pygame
import random

class Prefab:
    def __init__(self, core):
        self.core = core

    def Rigidbody(self, name: str, sprite):
        rigidbody = self.core.EntityManager.createEntity()
        self.core.ComponentManager.addComponents(rigidbody, component.Transform(math.Vector2(0, 0), math.Degrees(0), 1),
                                                            component.Velocity(math.Vector2(0, 0)),
                                                            component.Acceleration(math.Vector2(0, 0)),
                                                            component.Sprite(sprite),
                                                            component.Name(name))

    def Tile(self, name: str, sprite, cell: math.Vector2 = math.Vector2(0, 0), tilesize: int = 100):
        tile = self.core.EntityManager.createEntity()
        self.core.ComponentManager.addComponents(tile, component.Transform(math.Vector2(cell.x * tilesize, cell.y * tilesize), math.Degrees(0), 1),
                                                       component.Sprite(sprite),
                                                       component.Tile(tilesize, tilesize),
                                                       component.Name(name))
        self.core.SpatialGrid.insertEntity(tile, math.Vector2(cell.x * tilesize, cell.y * tilesize), math.Vector2(tilesize, tilesize))