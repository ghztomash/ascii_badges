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
    def __init__(self, display, position: Vector, velocity: Vector, acceleration: Vector):
        self.display = display
        (self.width, self.height) = display.get_bounds()
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.lifetime = 1

    def update(self, dt: float = 1.0):
        # Update velocity
        self.velocity += self.acceleration * dt
        # Update position
        self.position += self.velocity * dt
        # Update lifetime
        self.lifetime += dt

    def is_alive(self) -> bool:
        return self.lifetime > 0

    def is_offscreen(self) -> bool:
        return self.position.x < 0 or self.position.x > self.width or self.position.y < 0 or self.position.y > self.height

    def random_char(self):
        return random.randint(33, 127)