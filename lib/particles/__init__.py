import random

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, scalar: float):
        return Vector(self.x * scalar, self.y * scalar)

    def __add__(self, other):
        return self.add(other)


class Particle:
    def __init__(self, display, position: Vector, velocity: Vector = Vector(0, 0), acceleration: Vector = Vector(0, 0), 
                 size = 1.0, lifetime = 1000.0):
        self.display = display
        (self.width, self.height) = display.get_bounds()
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.size = size
        self.age = 0
        self.lifetime = lifetime

    def update(self, dt: float = 1.0):
        # Update velocity
        self.velocity += self.acceleration * dt
        # Update position
        self.position += self.velocity * dt
        # Update lifetime
        self.age += dt

    def is_alive(self) -> bool:
        return self.age < self.lifetime

    def is_offscreen(self) -> bool:
        return self.position.x - self.size < 0 or self.position.x + self.size > self.width or self.position.y + self.size < 0 or self.position.y + self.size > self.height

    def random_char(self):
        return random.randint(33, 127)