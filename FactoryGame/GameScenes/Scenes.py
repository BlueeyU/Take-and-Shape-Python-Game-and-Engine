from Core.EngineContext import EngineContext
from Engine.Core.Scenes import Scene

from Engine.ECS.System import MovementSystem, RenderingSystem
from Engine.ECS.SystemManager import SystemType

#==================================================#

from Engine.ECS import Component
from Engine.Math import Math

TransformComponent = Component.Transform
ColliderComponent = Component.Collider
SpriteComponent = Component.Sprite
VelocityComponent = Component.Velocity
AccelerationComponent = Component.Acceleration

Vec2 = Math.Vector2
Degree = Math.Degrees

#==================================================#

class MainMenuScene(Scene):
    def _defineAttributes(self, enginecontext: EngineContext):
        self.EngineContext = enginecontext

    def _onStart(self):
        assets = self.EngineContext.AssetManager.Registry
        loader = self.EngineContext.AssetManager.Loader
        playersprite = assets.registerTexture("playersprite", "engineer_1.png")
        loader.loadTexture(playersprite)

        print("MainMenuScene Started")

        self.SystemManager.addSystem(
            MovementSystem(self.EngineContext, self),
            SystemType.PHYSICS
        )

        self.SystemManager.addSystem(
            RenderingSystem(self.EngineContext, self),
            SystemType.RENDERING
        )

        self.addEntityToQueue(TransformComponent(Vec2(0, 0), Degree(0), scale=1),
                              ColliderComponent(100, 100),
                              SpriteComponent(playersprite)
                              )

        player = self.EntityManager.createEntity()
        self.ComponentManager.addComponents(player, TransformComponent(Vec2(0, 0), Degree(0), scale=1),
                              ColliderComponent(100, 100),
                              SpriteComponent(playersprite)
                              )

    def _onStop(self):
        print("MainMenuScene Ended")
