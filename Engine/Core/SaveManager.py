import json

import Math.Math
from ECS.Component import Speed


class SaveManager:
    def __init__(self):
        self.savePath = r"C:\Users\luisk\User provided code\Python Projects\Take and Shape\Engine\SaveFile\Savefile.json"
        self.logFilePath = r"C:\Users\luisk\User provided code\Python Projects\Take and Shape\Engine\SaveFile\Logfile.txt"

        self.classes = {}

    def save(self, data, saveType: str = "save"):
        if saveType == "save":
            with open(self.savePath, 'w') as file:
                json.dump(data, file, indent=4)
        elif saveType == "log":
            with open(self.logFilePath, 'w') as file:
                json.dump(data, file, indent=4)

    def load(self, saveType: str = "save"):
        if saveType == "save":
            try:
                with open(self.savePath, 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                return None
        elif saveType == "log":
            try:
                with open(self.logFilePath, 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                return None
        return None

    def serialize(self, obj):
        if isinstance(obj, Math.Math.Vector2):
            return {"type": "Vector2", "x": obj.x, "y": obj.y}
        if isinstance(obj, Math.Math.Degrees):
            return {"type": "Degrees", "degree": obj.degree}

        if isinstance(obj, (int, float, str, bool)):
            return obj
        if isinstance(obj, list):
            return [self.serialize(x) for x in obj]
        if isinstance(obj, dict):
            return {
                key: self.serialize(value)
                for key, value in obj.items()
            }

        return {
            "name": obj.__class__.__name__,
            "data": {key: self.serialize(value) for key, value in obj.__dict__.items()}
        }

    def deserialize(self, saveEntry):
        if "type" in saveEntry:
            if saveEntry["type"] == "Vector2":
                return Math.Math.Vector2(
                    saveEntry["x"],
                    saveEntry["y"]
                )

            if saveEntry["type"] == "Degrees":
                return Math.Math.Degrees(
                    saveEntry["degree"]
                )
        className = saveEntry["name"]
        if className not in self.classes:
            raise Exception("Unknown Class")
        cls = self.classes[className]
        data = {
            key: self.deserialize(value)
            for key, value in saveEntry["data"].items()
        }
        return cls(**data)

    def register(self, cls):
        if cls.__name__ in self.classes:
            raise Exception("Class already registered")

        self.classes[cls.__name__] = cls


