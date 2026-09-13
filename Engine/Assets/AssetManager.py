from dataclasses import dataclass, field
import pygame
import os

@dataclass
class Registry:
    TextureRegistry: dict
    SoundRegistry: dict

    TEXTURE_DIRECTORY: str
    SOUND_DIRECTORY: str

    def registerTexture(self, texture: str, path: str):
        if texture in self.TextureRegistry:
            raise Exception(f"Texture: {texture} already registered")

        self.TextureRegistry[texture] = os.path.join(
            self.TEXTURE_DIRECTORY,
            path
        )

        return texture

    def registerSound(self, sound: str, path: str):
        if sound in self.SoundRegistry:
            raise Exception(f"Sound: {sound} already registered")

        self.SoundRegistry[sound] = os.path.join(
            self.SOUND_DIRECTORY,
            path
        )

        return sound

@dataclass
class Loader:
    Textures: dict
    Sounds: dict

    TextureRegistry: dict
    SoundRegistry: dict

    def loadTexture(self, texture: str):
        if texture in self.Textures:
            raise Exception(f"Texture: {texture} already loaded")

        if texture not in self.TextureRegistry:
            raise Exception(f"Texture: {texture} not registered")

        self.Textures[texture] = (
            pygame.image.load(
                self.TextureRegistry[texture]
            ).convert_alpha()
        )

    def loadSound(self, sound: str):
        if sound in self.Sounds:
            raise Exception(f"Sound: {sound} already loaded")

        if sound not in self.SoundRegistry:
            raise Exception(f"Sound: {sound} not registered")

        self.Sounds[sound] = (
            pygame.mixer.Sound(
                self.SoundRegistry[sound]
            )
        )

    def unloadTexture(self, texture: str):
        if texture not in self.Textures:
            return

        del self.Textures[texture]

    def unloadSound(self, sound: str):
        if sound not in self.Sounds:
            return

        del self.Sounds[sound]

@dataclass
class Access:
    Textures: dict
    Sounds: dict

    def getTexture(self, texture: str):
        if texture not in self.Textures:
            raise Exception(f"Texture: {texture} not loaded")

        return self.Textures[texture]

    def getSound(self, sound: str):
        if sound not in self.Sounds:
            raise Exception(f"Sound: {sound} not loaded")

        return self.Sounds[sound]

@dataclass
class AssetManager:
    Textures: dict = field(default_factory=dict)
    Sounds: dict = field(default_factory=dict)

    TextureRegistry: dict = field(default_factory=dict)
    SoundRegistry: dict = field(default_factory=dict)

    BASE_DIRECTORY: str = r"C:\Users\luisk\User provided code\Python Projects\Take and Shape\Engine\Assets\Asset"
    TEXTURE_DIRECTORY: str = os.path.join(
        BASE_DIRECTORY, "SpriteAssets"
    )
    SOUND_DIRECTORY: str = os.path.join(
        BASE_DIRECTORY, "SoundAssets"
    )

    Registry: Registry = field(init=False)
    Loader: Loader = field(init=False)
    Access: Access = field(init=False)

    def __post_init__(self):
        self.Registry = Registry(
            self.TextureRegistry,
            self.SoundRegistry,
            self.TEXTURE_DIRECTORY,
            self.SOUND_DIRECTORY
        )

        self.Loader = Loader(
            self.Textures,
            self.Sounds,
            self.TextureRegistry,
            self.SoundRegistry
        )

        self.Access = Access(
            self.Textures,
            self.Sounds
        )
