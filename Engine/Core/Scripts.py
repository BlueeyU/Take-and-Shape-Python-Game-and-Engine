from Core.Time import Time
from ECS import Component as cmp
from ECS.ComponentManager import ComponentManager
from Math import Math as math
from Events import Events as evn
import math as mathf
import pygame

from Physics.SpatialGrid import SpatialGrid


class Script:
    def __init__(self, entityID):
        self.entityID: int = entityID
        pass

    def _onStart(self, core):
        pass

    def _onEnd(self, core):
        pass

    def _tick(self, core): # Ticks at the current Framerate, can use Transform, Velocity, Acceleration, Collider and Sprite
        pass

    def _physicsTick(self, core): # Ticks at the physics Tickrate, can use Transform, Velocity, Acceleration, Collider and Sprite
        pass

    def _specialTick(self, core): # Ticks at a custom Tickrate, can use every Component but is lesser performing
        pass

    def _onEvent(self, core):
        pass

    def _trigger(self, core):
        pass

    def _onDestroy(self, core):
        pass


class PlayerScript(Script):
    def __init__(self, entityID):
        super().__init__(entityID)

    def _physicsTick(self, core):
        rot = core.ComponentManager.getComponent(self.entityID, cmp.Transform).rotation
        vel = core.ComponentManager.getComponent(self.entityID, cmp.Velocity).velocity
        speed = core.ComponentManager.getComponent(self.entityID, cmp.Speed).speed
        sprite = core.ComponentManager.getComponent(self.entityID, cmp.Sprite)

        movement = False

        moveDirection = math.Vector2(0, 0)
        for event in core.EventBus.events:
            if type(event) == evn.KeyPressedEvent:
                if event.key == "W":
                    moveDirection.y -= 1
                if event.key == "S":
                    moveDirection.y += 1
                if event.key == "A":
                    moveDirection.x -= 1
                    movement = True
                if event.key == "D":
                    moveDirection.x += 1
                    movement = True
                if event.key == "LSHIFT":
                    speed *= 2
                if event.key == "LCTRL":
                    speed *= 5

        moveDirection.x, moveDirection.y = math.Util.normalize(moveDirection.x, moveDirection.y)

        heightTurn = 10 if (moveDirection.y < 0 and moveDirection.x != 0) else -10 if (moveDirection.y > 0 and moveDirection.x != 0) else 0
        rot.degree = heightTurn

        if movement:
            sprite.flipX = True if moveDirection.x < 0 else False

        vel.x = moveDirection.x * speed
        vel.y = moveDirection.y * speed

class EnemyAI(Script):
    def _physicsTick(self, core):
        pos = core.ComponentManager.getComponent(self.entityID, cmp.Transform).position
        col = core.ComponentManager.getComponent(self.entityID, cmp.Collider)
        vel = core.ComponentManager.getComponent(self.entityID, cmp.Velocity).velocity
        speed = core.ComponentManager.getComponent(self.entityID, cmp.Speed).speed

        player = list(core.ComponentManager.query(cmp.PlayerCharacter))

        playerPosition = core.ComponentManager.getComponent(player[0], cmp.Transform).position

        distanceCoordinates = math.Vector2((playerPosition.x + col.width/2 - pos.x), (playerPosition.y - col.height/2 - pos.y))

        distance = mathf.hypot(distanceCoordinates.x, distanceCoordinates.y)

        if distance > 200:
            movementVector = math.Vector2(0, 0)
            movementVector.x, movementVector.y = math.Util.normalize(distanceCoordinates.x / distance, distanceCoordinates.y / distance)

            vel.x = movementVector.x * speed
            vel.y = movementVector.y * speed

        else:
            vel.x = 0
            vel.y = 0




