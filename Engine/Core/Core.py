
class Core:
    def __init__(self, EntityManager, ComponentManager, SystemManager, EventBus, InputManager, TimeManager, Time, AssetManager, Logger, SaveManager, Camera, SpatialGrid, display, game, alpha):
        self.EntityManager = EntityManager
        self.ComponentManager = ComponentManager
        self.SystemManager = SystemManager
        self.EventBus = EventBus
        self.InputManager = InputManager
        self.TimeManager = TimeManager
        self.Time = Time
        self.AssetManager = AssetManager
        self.Logger = Logger
        self.SaveManager = SaveManager
        self.Camera = Camera
        self.SpatialGrid = SpatialGrid

        self.display = display
        self.game = game
        self.alpha = alpha