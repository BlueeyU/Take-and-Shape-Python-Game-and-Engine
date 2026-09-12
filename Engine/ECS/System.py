
from ECS import Component as cmp
from Math import Math as math
import pygame



class System:
    def __init__(self, core):
        self.core = core

class MovementSystem(System):
    def __init__(self, core):
        super().__init__(core)

    def update(self):
        accelerationEntities = self.core.ComponentManager.query(cmp.Acceleration)
        colliderEntities = self.core.ComponentManager.query(cmp.Collider)
        interpolatedEntities = self.core.ComponentManager.query(cmp.Interpolated, cmp.PreviousTransform)

        for entity in self.core.ComponentManager.query(cmp.Velocity):
            pos = self.core.ComponentManager.getComponent(entity, cmp.Transform).position
            vel = self.core.ComponentManager.getComponent(entity, cmp.Velocity).velocity

            if entity in accelerationEntities:
                acc = self.core.ComponentManager.getComponent(entity, cmp.Acceleration).acceleration
                vel.x += acc.x * self.core.Time.physicsDeltaTime
                vel.y += acc.y * self.core.Time.physicsDeltaTime

            if entity in interpolatedEntities:
                position = self.core.ComponentManager.getComponent(entity, cmp.PreviousTransform).position
                position.x = pos.x
                position.y = pos.y

            pos.x += vel.x * self.core.Time.physicsDeltaTime
            pos.y += vel.y * self.core.Time.physicsDeltaTime

            if entity in colliderEntities:
                col = self.core.ComponentManager.getComponent(entity, cmp.Collider)
                self.core.SpatialGrid.update(entity, math.Vector2(pos.x + col.offsetX, pos.y + col.offsetY), math.Vector2(col.width, col.height))
                continue

            self.core.SpatialGrid.update(entity, pos)

class DebugSystem(System):
    def __init__(self, core):
        super().__init__(core)

    def update(self):
        pass

class CameraSystem(System):
    def __init__(self, core):
        super().__init__(core)

    def update(self):
        startPosition = math.Vector2(self.core.Camera.position.x - self.core.display.width * 2, self.core.Camera.position.y - self.core.display.height * 2)
        endPosition = math.Vector2(self.core.display.width * 4, self.core.display.height * 4)

        designatedCameraPosition = (self.core.Camera.position.x, self.core.Camera.position.y)

        rawEntities = self.core.SpatialGrid.nearestEntities(startPosition, endPosition)
        interpolatedEntities = list(self.core.ComponentManager.queryNearestEntities(rawEntities, cmp.Interpolated, cmp.PreviousTransform))

        for entity in self.core.ComponentManager.query(cmp.PlayerCharacter, cmp.Transform, cmp.Collider):
            pos = self.core.ComponentManager.getComponent(entity, cmp.Transform).position
            col = self.core.ComponentManager.getComponent(entity, cmp.Collider)

            if entity in interpolatedEntities:
                position = self.core.ComponentManager.getComponent(entity, cmp.PreviousTransform).position
                newPos = (math.Util.lerp(position.x, pos.x, self.core.alpha), math.Util.lerp(position.y, pos.y, self.core.alpha))
            else:
                newPos = (pos.x, pos.y)

            designatedCameraPosition = (newPos[0] - self.core.display.width / 2 + col.width / 2 + col.offsetX, newPos[1] - self.core.display.height / 2 + col.height / 2 + col.offsetY)

        self.core.Camera.position.x = designatedCameraPosition[0]
        self.core.Camera.position.y = designatedCameraPosition[1]

class RenderingSystem(System):
    def __init__(self, core):
        super().__init__(core)

    def update(self):
        startPosition = math.Vector2(self.core.Camera.position.x, self.core.Camera.position.y)
        endPosition = math.Vector2(self.core.display.width, self.core.display.height)

        rawEntities = self.core.SpatialGrid.nearestEntities(startPosition, endPosition)
        entities = list(self.core.ComponentManager.queryNearestEntities(rawEntities, cmp.Sprite))
        entities.sort(key=lambda e: (self.core.ComponentManager.getComponent(e, cmp.Sprite).layer, self.core.ComponentManager.getComponent(e, cmp.Transform).position.y))

        interpolatedEntities = set(self.core.ComponentManager.queryNearestEntities(rawEntities, cmp.PreviousTransform))

        spriteList = []

        for entity in entities:
            transform = self.core.ComponentManager.getComponent(entity, cmp.Transform)
            pos = transform.position
            rot = transform.rotation.degree
            scale = transform.scale
            sprite = self.core.ComponentManager.getComponent(entity, cmp.Sprite)
            oldSprite = self.core.AssetManager.getAsset(sprite.textureName)

            flipX = sprite.flipX
            flipY = sprite.flipY

            newSprite = pygame.transform.scale(oldSprite, (oldSprite.width * scale, oldSprite.height * scale))

            if flipX:
                newSprite = pygame.transform.flip(newSprite, True, False)
            if flipY:
                newSprite = pygame.transform.flip(newSprite, False, True)

            if rot < 180:
                if not flipX:
                    newSprite = pygame.transform.rotate(newSprite, rot)
                else:
                    newSprite = pygame.transform.rotate(newSprite, -rot)
            else:
                if not flipX:
                    newSprite = pygame.transform.rotate(newSprite, rot - 180)
                else:
                    newSprite = pygame.transform.rotate(newSprite, -rot - 180)

            spriteOffsetX = newSprite.width / 2
            spriteOffsetY = newSprite.height / 2

            if entity in interpolatedEntities:
                position = self.core.ComponentManager.getComponent(entity, cmp.PreviousTransform).position
                drawingPosition = ((math.Util.lerp(position.x - spriteOffsetX, pos.x - spriteOffsetX, self.core.alpha) - self.core.Camera.position.x),
                                   (math.Util.lerp(position.y - spriteOffsetY, pos.y - spriteOffsetY, self.core.alpha) - self.core.Camera.position.y))
            else:
                drawingPosition = (pos.x - self.core.Camera.position.x - spriteOffsetX, pos.y - self.core.Camera.position.y - spriteOffsetY)

            spriteList.append((newSprite, drawingPosition))

        self.core.display.blits(spriteList)

class SpatialGridSystem(System):
    def __init__(self, core):
        System.__init__(self, core)

    def update(self):
        startPosition = math.Vector2(self.core.Camera.position.x - self.core.display.width * 2, self.core.Camera.position.y - self.core.display.height * 2)
        endPosition = math.Vector2(self.core.display.width * 4, self.core.display.height * 4)

        rawEntities = self.core.SpatialGrid.nearestEntities(startPosition, endPosition)
        entities = self.core.ComponentManager.queryNearestEntities(rawEntities, cmp.Transform)
        colliderEntities = self.core.ComponentManager.query(cmp.Collider)

        for entity in entities:
            pos = self.core.ComponentManager.getComponent(entity, cmp.Transform).position

            if entity in colliderEntities:
                col = self.core.ComponentManager.getComponent(entity, cmp.Collider)
                self.core.SpatialGrid.update(entity, math.Vector2(pos.x + col.offsetX, pos.y + col.offsetY), math.Vector2(col.width, col.height))
                continue

            self.core.SpatialGrid.update(entity, pos)

class CollisionSystem(System):
    def __init__(self, core):
        super().__init__(core)

    def update(self):
        entities = self.core.ComponentManager.query(cmp.Collider)
        movingEntities = set(self.core.ComponentManager.query(cmp.Velocity))
        scriptEntities = set(self.core.ComponentManager.query(cmp.Script))

        for e in entities:
            pos = self.core.ComponentManager.getComponent(e, cmp.Transform).position
            col = self.core.ComponentManager.getComponent(e, cmp.Collider)
            closestEntities = self.core.SpatialGrid.nearestEntities(pos, math.Vector2(col.width, col.height))
            entities = self.core.ComponentManager.queryNearestEntities(closestEntities, cmp.Transform, cmp.Collider)
            for o in entities:
                if e == o:
                    continue

                if not e in movingEntities and not o in movingEntities:
                    continue

                posE, posO = self.core.ComponentManager.getComponent(e, cmp.Transform).position, self.core.ComponentManager.getComponent(o, cmp.Transform).position
                colE, colO = self.core.ComponentManager.getComponent(e, cmp.Collider), self.core.ComponentManager.getComponent(o, cmp.Collider)
                newPosE = math.Vector2(posE.x + colE.offsetX, posE.y + colE.offsetY)
                newPosO = math.Vector2(posO.x + colO.offsetX, posO.y + colO.offsetY)
                if self.collisionTrigger(math.Rectangle(newPosE.x, newPosE.x + colE.width, newPosE.y, newPosE.y + colE.height),
                                         math.Rectangle(newPosO.x, newPosO.x + colO.width, newPosO.y, newPosO.y + colO.height)):
                    if e in scriptEntities:
                        scripts = self.core.ComponentManager.getComponent(e, cmp.Script).script
                        for script in scripts:
                            script._trigger(self.core)
                    if o in scriptEntities:
                        scripts = self.core.ComponentManager.getComponent(o, cmp.Script).script
                        for script in scripts:
                            script._trigger(self.core)

                    if e in movingEntities and o in movingEntities:
                        self.resolveDynamicCollision(e, o)
                    elif e in movingEntities and not o in movingEntities:
                        self.resolveStaticCollision(e, o)
                    elif o in movingEntities and not e in movingEntities:
                        self.resolveStaticCollision(o, e)

    @staticmethod
    def collisionTrigger(obj, other):
        if obj.bottom > other.top and obj.top < other.bottom and obj.right > other.left and obj.left < other.right:
            return True
        return False

    def resolveDynamicCollision(self, e, o):
        posE, posO = self.core.ComponentManager.getComponent(e, cmp.Transform).position, self.core.ComponentManager.getComponent(o, cmp.Transform).position
        colE, colO = self.core.ComponentManager.getComponent(e, cmp.Collider), self.core.ComponentManager.getComponent(o, cmp.Collider)
        velE, velO = self.core.ComponentManager.getComponent(e, cmp.Velocity).velocity, self.core.ComponentManager.getComponent(o, cmp.Velocity).velocity

        newPosE = math.Vector2(posE.x + colE.offsetX, posE.y + colE.offsetY)
        newPosO = math.Vector2(posO.x + colO.offsetX, posO.y + colO.offsetY)

        colliderCoefficentO = math.Vector2(colE.width / colO.width, colE.height / colO.height)
        colliderCoefficentE = math.Vector2(colO.width / colE.width, colO.height / colE.height)

        overlapX = min(newPosE.x + colE.width, newPosO.x + colO.width) - max(newPosE.x, newPosO.x)
        overlapY = min(newPosE.y + colE.height, newPosO.y + colO.height) - max(newPosE.y, newPosO.y)

        if overlapX < overlapY:
            if posE.x < posO.x:
                posE.x -= overlapX / 2
                posO.x += overlapX / 2
            else:
                posE.x += overlapX / 2
                posO.x -= overlapX / 2
        else:
            if posE.y < posO.y:
                posE.y -= overlapY / 2
                posO.y += overlapY / 2
            else:
                posE.y += overlapY / 2
                posO.y -= overlapY / 2
        velE.x, velO.x = velO.x * colliderCoefficentE.x * 0.95 / 4, velE.x * colliderCoefficentO.x * 0.95 / 4
        velE.y, velO.y = velO.y * colliderCoefficentE.y * 0.95 / 4, velE.y * colliderCoefficentO.y * 0.95 / 4

    def resolveStaticCollision(self, e, o):
        posE, posO = self.core.ComponentManager.getComponent(e, cmp.Transform).position, self.core.ComponentManager.getComponent(o, cmp.Transform).position
        colE, colO = self.core.ComponentManager.getComponent(e, cmp.Collider), self.core.ComponentManager.getComponent(o, cmp.Collider)
        vel = self.core.ComponentManager.getComponent(e, cmp.Velocity).velocity

        newPosE = math.Vector2(posE.x + colE.offsetX, posE.y + colE.offsetY)
        newPosO = math.Vector2(posO.x + colO.offsetX, posO.y + colO.offsetY)

        overlapX = min(newPosE.x + colE.width, newPosO.x + colO.width) - max(newPosE.x, newPosO.x)
        overlapY = min(newPosE.y + colE.height, newPosO.y + colO.height) - max(newPosE.y, newPosO.y)
        if overlapX < overlapY:
            if posE.x < posO.x:
                posE.x -= overlapX
            else:
                posE.x += overlapX
        else:
            if posE.y < posO.y:
                posE.y -= overlapY
            else:
                posE.y += overlapY
        vel.x *= -0.5
        vel.y *= -0.5

class ScriptingSystem(System):
    def __init__(self, core):
        super().__init__(core)

    def update(self):
        colliderEntities = self.core.ComponentManager.query(cmp.Collider)
        for entity in self.core.ComponentManager.query(cmp.Script):
            pos = self.core.ComponentManager.getComponent(entity, cmp.Transform).position
            scripts = self.core.ComponentManager.getComponent(entity, cmp.Script).script
            for script in scripts:
                script._tick(self.core)

                if self.core.Time.physicsTick >= 0:
                    script._physicsTick(self.core)

                if self.core.Time.specialTick >= 0:
                    script._specialTick(self.core)

            if entity in colliderEntities:
                col = self.core.ComponentManager.getComponent(entity, cmp.Collider)
                self.core.SpatialGrid.update(entity, math.Vector2(pos.x + col.offsetX, pos.y + col.offsetY), math.Vector2(col.width, col.height))
                continue

            self.core.SpatialGrid.update(entity, pos)
