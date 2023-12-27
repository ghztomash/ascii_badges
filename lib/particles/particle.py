import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def multiply(self, scalar: float):
        return Vector(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def angle(self):
        return math.atan2(self.y, self.x)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector(self.x / length, self.y / length)
        return Vector(0, 0)

    def __mul__(self, scalar: float):
        return self.multiply(scalar)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


class Particle:
    def __init__(
        self,
        display,
        position: Vector,
        velocity: Vector = Vector(0, 0),
        acceleration: Vector = Vector(0, 0),
        scale=1.0,
        is_anchor: bool = False,
        lifetime=100.0,
    ):
        self.display = display
        (self.width, self.height) = display.get_bounds()
        self.position = position
        self.is_anchor = is_anchor
        self.velocity = velocity
        self.acceleration = acceleration
        self.scale = scale
        self.age = 0
        self.lifetime = lifetime
        self.last_angle = velocity.angle()
        self.last_distance = velocity.length()

    def update(self, dt: float = 1.0):
        if self.is_anchor:
            return
        # Update velocity
        self.velocity += self.acceleration * dt
        # Update position
        self.position += self.velocity * dt
        # Update lifetime
        self.age += dt
        # last position angle
        self.last_angle = self.velocity.angle()
        # distance from last position
        self.last_distance = self.velocity.dot(self.velocity)

    def is_alive(self) -> bool:
        return self.age < self.lifetime

    def is_offscreen(self) -> bool:
        return (
            self.position.x - self.scale < 0
            or self.position.x + self.scale > self.width
            or self.position.y + self.scale < 0
            or self.position.y + self.scale > self.height
        )

    def apply_force(self, force: Vector):
        self.acceleration += force


# Calculate position of a point at a given angle and distance from a center point
def point_at_angle(center: Vector, angle: float, distance: float) -> Vector:
    return Vector(
        center.x + distance * math.cos(angle), center.y + distance * math.sin(angle)
    )


def random_vector(scale=10.0):
    return Vector(random.uniform(-scale, scale), random.uniform(-scale, scale))

