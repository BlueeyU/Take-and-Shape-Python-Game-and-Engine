from Core.EngineContext import EngineContext
from Core.Scenes import SceneManager
from FactoryGame.GameScenes.Scenes import MainMenuScene

class AssetRegistry:
    @staticmethod
    def register(AssetManager): ...

class SceneRegistry:
    @staticmethod
    def register(scenemanager: SceneManager, enginecontext: EngineContext):
        Main_Menu_Scene = MainMenuScene()
        Main_Menu_Scene._defineAttributes(enginecontext)

        scenemanager.addScene(
            Main_Menu_Scene
        )

        scenemanager.loadScene(
            Main_Menu_Scene
        )

        scenemanager.setActiveScene(
            Main_Menu_Scene
        )


