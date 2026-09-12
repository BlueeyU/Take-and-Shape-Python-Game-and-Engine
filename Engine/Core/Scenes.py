from dataclasses import dataclass, field

import Math.Math as math
from ECS.EntityManager import EntityManager
from ECS.ComponentManager import ComponentManager
from ECS.SystemManager import SystemManager
from Engine.Core.Camera import Camera
from Physics.SpatialGrid import SpatialGrid

@dataclass
class Scene:
    EntityManager: EntityManager = field(default_factory = EntityManager)
    ComponentManager: ComponentManager = field(default_factory = ComponentManager)
    SpatialGrid: SpatialGrid = field(default_factory = SpatialGrid)
    SystemManager: SystemManager = field(default_factory = SystemManager)

    Camera: Camera = field(default_factory = lambda:
        Camera(
            math.Vector2(0, 0),
            math.Degrees(0),
            zoom = 1
        )
    )

    entityQueue: list = field(default_factory=list)

    loaded: bool = False

    def _defineAttributes(self, *args):
        pass

    def _onStart(self):
        pass

    def _onStop(self):
        pass

    def construct(self):
        if not self.entityQueue:
            return

        for components in self.entityQueue:
            entity = self.EntityManager.createEntity()
            self.ComponentManager.addComponents(entity, *components)

        self.entityQueue.clear()

    def addEntityAtRuntime(self, *components):
        entity = self.EntityManager.createEntity()
        self.ComponentManager.addComponents(entity, *components)

    def addEntityToQueue(self, *components):
        self.entityQueue.append(components)

@dataclass
class SceneManager:
    ActiveScene: Scene | None = None
    LoadedScenes: list[Scene] = field(default_factory=list)
    UnloadedScenes: list[Scene] = field(default_factory=list)

    def setActiveScene(self, scene: Scene):
        if scene not in self.LoadedScenes:
            if scene in self.UnloadedScenes:
                self.loadScene(scene)
            return

        self.ActiveScene = scene

    def addScene(self, scene: Scene):
        if scene not in self.LoadedScenes and scene not in self.UnloadedScenes:
            self.UnloadedScenes.append(scene)

    def removeScene(self, scene: Scene):
        if scene == self.ActiveScene:
            self.ActiveScene = None

        if scene in self.LoadedScenes:
            self.LoadedScenes.remove(scene)

        if scene in self.UnloadedScenes:
            self.UnloadedScenes.remove(scene)

    def loadScene(self, scene: Scene):
        if scene not in self.UnloadedScenes or scene in self.LoadedScenes:
            return

        scene.construct()
        scene._onStart()

        self.LoadedScenes.append(scene)
        self.UnloadedScenes.remove(scene)

    def unloadScene(self, scene: Scene):
        if scene == self.ActiveScene:
            self.ActiveScene = None

        if scene in self.UnloadedScenes or scene not in self.LoadedScenes:
            return

        scene._onStop()

        self.UnloadedScenes.append(scene)
        self.LoadedScenes.remove(scene)

