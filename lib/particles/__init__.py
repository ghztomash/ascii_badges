import random
import time

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

class AsciiParticle(Particle):
    def __init__(self, display, position: Vector, velocity: Vector = Vector(0, 0), acceleration: Vector = Vector(0, 0), 
                 size = 1.0, lifetime = 1000.0, length = 1, char_rate = 250):
        super().__init__(display, position, velocity, acceleration, size, lifetime)
        self.chars = [random_char()]
        self.char_rate = char_rate
        self.length = length
        self.last_char_ms = time.ticks_ms()
    
    def update(self, dt: float = 1.0):
        super().update(dt)
        if time.ticks_ms() - self.last_char_ms > self.char_rate:
            self.chars.insert(0, random_char())
            if len(self.chars) > self.length:
                self.chars.pop()
            self.last_char_ms = time.ticks_ms()
    
    def reset(self):
        self.velocity = Vector(random.uniform(-5, 5), random.uniform(-5, 5))
        self.acceleration = Vector(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
        self.size = random.uniform(1, 5)
        self.chars = [random_char()]
        self.char_rate = random.uniform(100, 500)
        self.length = random.randint(3, 10)
        self.last_char_ms = time.ticks_ms()
        self.age = 0

    def draw(self):
        self.display.text(''.join([chr(c) for c in self.chars]), int(self.position.x), int(self.position.y), scale = self.size)

def random_char():
    return random.randint(33, 126)