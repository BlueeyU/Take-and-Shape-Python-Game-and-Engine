
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ECS.Component import Sprite

if TYPE_CHECKING:
    from Engine.Core.Scenes import Scene
    from Engine.Core.EngineContext import EngineContext

from Engine.Math import Math as math
from Engine.ECS import Component
import math as mathf

vec2 = math.Vector2

import pygame

@dataclass
class System:
    EngineContext: EngineContext
    Scene: Scene

class MovementSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        display = self.EngineContext.RenderContext.Display
        camera = self.Scene.Camera

        nearestEntities = self.Scene.SpatialGrid.nearestEntities(
            camera.position - vec2(display.width / 2, display.height / 2),
            camera.position + vec2(display.width * 1.5, display.height * 1.5)
        )

        entities = self.Scene.ComponentManager.queryNearestEntities(
            nearestEntities,
            Component.Transform, Component.Velocity
        )

        for entity in entities:
            transform, velocity = self.Scene.ComponentManager.getComponent(
                entity,
                Component.Transform, Component.Velocity
            )

            transform.position += velocity.velocity * self.EngineContext.Time.deltaTime

class AccelerationSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        display = self.EngineContext.RenderContext.Display
        camera = self.Scene.Camera

        nearestEntities = self.Scene.SpatialGrid.nearestEntities(
            camera.position - vec2(display.width / 2, display.height / 2),
            camera.position + vec2(display.width * 1.5, display.height * 1.5)
        )

        entities = self.Scene.ComponentManager.queryNearestEntities(
            nearestEntities,
            Component.Velocity, Component.Acceleration
        )

        for entity in entities:
            velocity, acceleration = self.Scene.ComponentManager.getComponent(
                entity,
                Component.Velocity, Component.Acceleration
            )

            velocity.velocity += acceleration.acceleration * self.EngineContext.Time.deltaTime

class CharacterMovementSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass

class CollisionSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass

class RenderingSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        display = self.EngineContext.RenderContext.Display
        camera = self.Scene.Camera
        assets = self.EngineContext.AssetManager.Access
        loader = self.EngineContext.AssetManager.Loader

        nearestEntities = self.Scene.SpatialGrid.nearestEntities(
            camera.position - vec2(display.width / 2, display.height / 2),
            camera.position + vec2(display.width * 1.5, display.height * 1.5)
        )

        entities = list(
            self.Scene.ComponentManager.queryNearestEntities(
                nearestEntities,
                Component.Transform, Component.Sprite
            )
        )

        batch = []

        for entity in entities:
            transform, sprite = self.Scene.ComponentManager.getComponent(
                entity,
                Component.Transform, Component.Sprite
            )

            position = transform.position
            rotation = transform.rotation.degree
            scale = transform.scale

            plaintexture = assets.getTexture(sprite.textureName)

            texture = pygame.transform.rotate(plaintexture, rotation)
            texture = pygame.transform.smoothscale(
                texture,
                (
                    int(texture.width * scale),
                    int(texture.height * scale)
                )
            )

            batch.append(
                (texture,
                (
                position.x - camera.position.x,
                position.y - camera.position.y
                )
                )
            )

        display.blits(batch)

class CameraSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass

class AnimationSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass

class LifetimeSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass

class DamageSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass

class ScriptSystem(System):
    def __init__(self, enginecontext: EngineContext, scene: Scene):
        super().__init__(enginecontext, scene)

    def update(self):
        pass