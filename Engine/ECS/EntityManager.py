
class EntityManager:
    def __init__(self):
        self.nextIds = 0
        self.freeIds = []

        self.activeEntities = set()
        self.freeingQueue = set()
        self.destroyQueue = set()

    def clear(self):
        self.nextIds = 0
        self.freeIds = []

        self.activeEntities = set()
        self.freeingQueue = set()
        self.destroyQueue = set()

    def createEntity(self):
        if self.freeIds:
            entityID = self.freeIds.pop(0)
        else:
            entityID = self.nextIds
            self.nextIds += 1
        self.activeEntities.add(entityID)
        return entityID

    def destroyEntity(self, entityId):
        self.destroyQueue.add(entityId)
        self.freeingQueue.add(entityId)

    def entityRecycling(self):
        self.freeIds.extend(self.freeingQueue)
        self.freeingQueue.clear()