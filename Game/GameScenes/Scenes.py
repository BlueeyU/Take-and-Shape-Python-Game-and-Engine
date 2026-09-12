from Core.EngineContext import EngineContext
from Engine.Core.Scenes import Scene

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
        self.EngineContext.AssetManager.loadSprite("playersprite", "engineer_1.png", (128, 128))
        playersprite = self.EngineContext.AssetManager.getAsset("playersprite")

        self.addEntityToQueue(TransformComponent(Vec2(0, 0), Degree(0), scale = 1),
                                       ColliderComponent(100, 100),
                                       SpriteComponent(playersprite)
                                       )