import pygame

class AssetManager:
    def __init__(self):
        self.activeAssets = {}

        self.mainAssetsSource = r"C:\Users\luisk\User provided code\Python Projects\Factory Engine\Engine\Assets\Asset"

    def loadSprite(self, name, asset, scale = (100, 100), sourceType = r"\SpriteAssets"):
        if name not in self.activeAssets:
            self.activeAssets[name] = (pygame.image.load(str(self.mainAssetsSource + sourceType + r"\\" + asset)).convert_alpha())
            self.activeAssets[name] = (pygame.transform.scale(self.activeAssets[name], scale))
            return name
        else:
            raise Exception("Name already in Assets")

    def loadFont(self, name, text, size = 10):
        if name not in self.activeAssets:
            self.activeAssets[name] = (pygame.font.Font(text, size))
            return name
        else:
            raise Exception("Name already in Assets")

    def loadSound(self, name, asset, sourceType = r"\SoundAssets"):
        if name not in self.activeAssets:
            self.activeAssets[name] = (pygame.mixer.Sound(str(self.mainAssetsSource + sourceType + asset)))
            return name
        else:
            raise Exception("Name already in Assets")

    def getAsset(self, asset):
        if asset in self.activeAssets:
            return self.activeAssets[asset]
        else:
            raise Exception("Asset not in Assets")

    def unload(self, asset):
        if asset in self.activeAssets:
            del self.activeAssets[asset]
        else:
            raise Exception("Asset not in Assets")

    def clear(self):
        self.activeAssets = {}

