from dataclasses import dataclass
import math as maths

class Util:
    @staticmethod
    def normalize(a: float, b: float):
        length: float = maths.hypot(a, b)
        if length == 0:
            return 0.0, 0.0
        a /= length
        b /= length
        return a, b

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def clamp(value: float, minValue: float, maxValue: float):
        return max(minValue, min(value, maxValue))

    @staticmethod
    def smoothstep(t: float):
        return t * t * (3.0 - 2.0 * t)

@dataclass
class Vector2:
    x: float
    y: float

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Vector2(self.x / other.x, self.y / other.y)

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Rectangle:
    left: float
    right: float
    top: float
    bottom: float

class Degrees:
    def __init__(self, degree: float):
        self.degree = degree % 360

    def __add__(self, other):
        return Degrees(self.degree + other.degree)

    def __sub__(self, other):
        return Degrees(self.degree - other.degree)

    def __mul__(self, other):
        return Degrees(self.degree * other.degree)

    def __truediv__(self, other):
        return Degrees(self.degree / other.degree)

    def __repr__(self):
        return f'{self.degree}'

    def _to_radians(self):
        import math
        return math.radians(self.degree)

    @staticmethod
    def _from_radians(degree):
        import math
        return Degrees(math.degrees(degree))