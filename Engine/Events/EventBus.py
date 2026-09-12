
class EventBus:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)

    def remove(self, event):
        if event in self.events:
            self.events.remove(event)
        else:
            raise Exception("Event not in Events")

    def clear(self):
        self.events = []

    def __str__(self):
        return str(self.events)