
class CommandBus:
    def __init__(self):
        self.commands = []

    def post(self, command):
        self.commands.append(command)

    def remove(self, command):
        if command in self.commands:
            self.commands.remove(command)
        else:
            raise Exception("Command not in Cmmands")

    def clear(self):
        self.commands = []

    def __str__(self):
        return str(self.commands)