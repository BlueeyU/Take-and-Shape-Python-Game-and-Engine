
from Engine.ECS import Component
from Math import Math as math
from itertools import product

class SpatialGrid:
    def __init__(self):
        self.grid = {}
        self.entityCells = {}
        self.gridsize = 100

    def build(self, componentManager, assetManager = None):
        entities = list(componentManager.query(Component.Transform))
        colliderEntities = list(componentManager.query(Component.Collider))
        if not assetManager is None:
            spriteEntities = list(componentManager.query(Component.Sprite))
        else:
            spriteEntities = []

        entityListLength = len(entities)

        print(f"Starting SpatialGrid build ... | Entity amount: {entityListLength}")

        count = 0

        for entity in entities:
            count += 1

            if entityListLength * 0.1 + 1 > count >= entityListLength * 0.1:
                print("SpatialGrid build Status: 10% done")
            if entityListLength * 0.25 + 1 > count >= entityListLength  * 0.25:
                print("SpatialGrid build Status: 25% done")
            if entityListLength * 0.5 + 1 > count >= entityListLength * 0.5:
                print("SpatialGrid build Status: 50% done")
            if entityListLength * 0.75 + 1 > count >= entityListLength * 0.75:
                print("SpatialGrid build Status: 75% done")

            pos = componentManager.getComponent(entity, Component.Transform).position

            if entity not in colliderEntities and entity not in spriteEntities:
                self.insertEntity(entity, pos)

            if entity in colliderEntities and entity in spriteEntities:
                spriteTexture = componentManager.getComponent(entity, Component.Sprite).textureName
                sprite = assetManager.getAsset(spriteTexture)

                col = componentManager.getComponent(entity, Component.Collider)

                self.insertEntity(entity, math.Vector2(pos.x, pos.y), math.Vector2(max(col.width, sprite.width), max(col.height, sprite.height)))
                continue

            if entity in colliderEntities:
                col = componentManager.getComponent(entity, Component.Collider)

                self.insertEntity(entity, math.Vector2(pos.x, pos.y), math.Vector2(col.width, col.height))
                continue

            if entity in spriteEntities:
                spriteTexture = componentManager.getComponent(entity, Component.Sprite).textureName
                sprite = assetManager.getAsset(spriteTexture)

                self.insertEntity(entity, math.Vector2(pos.x, pos.y), math.Vector2(sprite.width, sprite.height))
                continue

    def update(self, entityID: int, position: math.Vector2, size: math.Vector2 = math.Vector2(0, 0)):
        newCells = self.get(position, size)
        if entityID not in self.entityCells:
            self.directlyInsert(entityID, newCells)
            return
        oldCells = self.entityCells[entityID]
        if oldCells == newCells:
            return
        self.remove(entityID)
        self.directlyInsert(entityID, newCells)

    def remove(self, entityID: int):
        for cell in self.entityCells[entityID]:
            self.grid[cell].remove(entityID)

            if not self.grid[cell]:
                del self.grid[cell]

        del self.entityCells[entityID]

    def directlyInsert(self, entityID: int, cells):
        for cell in cells:
            self.grid.setdefault(cell, []).append(entityID)
        self.entityCells[entityID] = cells

    def insertEntity(self, entityID: int, position: math.Vector2, size: math.Vector2 = math.Vector2(0, 0)):
        cells = list(self.get(position, size))
        for cell in cells:
            try:
                self.grid[cell].append(entityID)
            except KeyError:
                self.grid[cell] = [entityID]
        self.entityCells[entityID] = cells

    def get(self, position: math.Vector2, size: math.Vector2 = math.Vector2(0, 0)):
        startX = int(position.x // self.gridsize)
        startY = int(position.y // self.gridsize)

        endX = int((position.x + size.x) // self.gridsize)
        endY = int((position.y + size.y) // self.gridsize)

        return list(product(range(startX, endX + 1), range(startY, endY + 1)))

    def nearestEntities(self, position: math.Vector2, size: math.Vector2 = math.Vector2(0, 0)):
        entities = set()
        for cell in self.get(position, size):
            entities.update(self.grid.get(cell, []))
        return entities
