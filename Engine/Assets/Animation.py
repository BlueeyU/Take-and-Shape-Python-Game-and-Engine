
class Animation:
    def __init__(self, fps, loop):
        self.frames = []
        self.index = 0 % fps
        self.time = 0
        self.fps = fps
        self.loop = loop

    def update(self, deltaTime):
        self.time += deltaTime
        if self.time >= 1 / self.fps:
            self.index += 1
            if self.loop:
                self.time = 0