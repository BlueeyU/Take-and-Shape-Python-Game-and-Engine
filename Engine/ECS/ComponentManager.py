
class ComponentManager:
    def __init__(self):
        self.components = {}

    def clear(self):
        self.components = {}

    def addComponents(self, entityID, *components):
        for component in components:
            componentType = type(component)
            if componentType not in self.components:
                self.components[componentType] = {}
            self.components[componentType][entityID] = component

    def removeComponent(self, entityID, component):
        if component in self.components:
            if entityID in self.components[component]:
                del self.components[component][entityID]
            else:
                raise Exception("EntityID not in Components")
        else:
            raise Exception("Component not in Components")

    def hasComponent(self, entityID, component):
        if component in self.components:
            return entityID in self.components[component]
        return False

    def getComponent(self, entityID, component):
        if component not in self.components:
            raise Exception("Component not in Components")
        if entityID not in self.components[component]:
            raise Exception("EntityID not in Components")
        return self.components[component][entityID]

    def removeAll(self, entityID):
        for componentType in self.components:
            if entityID in self.components[componentType]:
                del self.components[componentType][entityID]

    def query(self, *components):
        if not components:
            return

        componentSets = [self.components.get(component, {}) for component in components]

        componentSets.sort(key=len)

        entityIDs = set(componentSets[0].keys())

        for componentSet in componentSets[1:]:
            entityIDs &= componentSet.keys()

        for entityID in entityIDs:
            yield entityID

    def queryNearestEntities(self, entities, *components):
        if not components:
            return

        componentSets = [self.components.get(component, {}) for component in components]

        entityIDs = set(entities)

        for componentSet in componentSets:
            entityIDs.intersection_update(componentSet.keys())

        for entityID in entityIDs:
            yield entityID
