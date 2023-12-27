import random
import time
from particles.particle import Particle, Vector, random_vector
from particles.joints import RigidChain


class AsciiChain:
    def __init__(
        self,
        display,
        source: Vector,
        velocity: Vector = Vector(0, 0),
        acceleration: Vector = Vector(0, 0),
        scale=1.0,
        size=10,
        lifetime=1000.0,
        length=1,
        char_rate=250,
    ):
        self.display = display
        self.particles = [
            Particle(display, source, velocity, acceleration, scale, False, lifetime)
        ]
        self.source = source
        self.size = size * scale
        self.scale = scale
        self.chain = RigidChain(self.particles, distance = self.size)
        self.chars: [int] = [random_char() for _ in range(length)]
        self.char_rate = char_rate
        self.length = length
        self.last_char_ms = ticks_ms()

    def update(self, dt: float = 1.0):
        if len(self.particles) > 0:
            last_position = self.particles[-1].position
        else:
            last_position = self.source

        self.chain.update(dt)

        if len(self.particles) < len(self.chars):
            self.particles.append(Particle(self.display, last_position))
            self.chain = RigidChain(self.particles, distance = self.size)

        # set a new head character if enough time has passed
        if ticks_ms() - self.last_char_ms > self.char_rate:
            self.chars.insert(0, random_char())
            while len(self.chars) > self.length:
                self.chars.pop()
            self.last_char_ms = ticks_ms()

    def reset(self):
        # self.length = random.randint(3, 10)
        self.length = 10
        head = self.particles[0]
        head.velocity = random_vector(5.0)
        self.particles = [head]
        # self.acceleration = Vector(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
        # self.scale = random.uniform(1, 5)
        self.chars = [random_char() for i in range(self.length)]
        # self.char_rate = random.uniform(250, 500) * (1.0 / self.velocity.dot(self.velocity)) + 50
        self.char_rate = 250
        # print(f"char_rate: {self.char_rate}")
        self.last_char_ms = ticks_ms()
        self.age = 0

    def is_offscreen(self) -> bool:
        # loop through all particles and return true if all are offscreen
        off_screen = True
        for particle in self.particles:
            if not particle.is_offscreen():
                off_screen = False 
        return off_screen

    def draw(self):
        i = 0
        display = self.display
        for particle in self.particles:
            display.character(
                self.chars[i], int(particle.position.x), int(particle.position.y), scale=int(self.scale)
            )
            i+=1
        # self.display.text(''.join([chr(c) for c in self.chars]), int(self.position.x), int(self.position.y), scale = self.size)


def random_char():
    return random.randint(33, 126)

# MicroPython compatibility
def ticks_ms():
    # return time.ticks_ms()
    return int(time.time() * 1000)
