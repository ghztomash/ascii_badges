import random
import time
import math
from particles.particle import Particle, Vector, random_vector, point_at_angle
from particles.joints import RigidChain


class AsciiChain:
    def __init__(
        self,
        display,
        head_colour,
        tail_colours,
        source: Vector,
        velocity: Vector = Vector(0, 0),
        acceleration: Vector = Vector(0, 0),
        scale=1.0,
        char_height=8,
        length=1,
        char_rate=250,
    ):
        self.display = display
        self.particles = [
            Particle(display, source, velocity, acceleration, scale)
        ]
        self.source = source
        self.char_height = char_height
        self.size = char_height * scale
        self.scale = scale
        self.chain = RigidChain(self.particles, distance = self.size)
        self.chars: [int] = [random_char() for _ in range(length)]
        self.char_rate = char_rate
        self.length = length
        self.head_colour = head_colour
        self.tail_colours = tail_colours
        self.last_char_ms = ticks_ms()

    def update(self, dt: float = 1.0):
        if len(self.particles) < len(self.chars):
            if len(self.particles) > 0:
                last_position = self.particles[-1].position
            else:
                last_position = self.source

            # add a new particle if the last one is far enough away
            distance_from_source = last_position.subtract(self.source).length()
            if distance_from_source > self.size:
                self.particles.append(Particle(self.display, self.source))
                self.chain = RigidChain(self.particles, distance = self.size)

        self.chain.update(dt)

        # set a new head character if enough time has passed
        if ticks_ms() - self.last_char_ms > self.char_rate:
            self.chars.insert(0, random_char())
            while len(self.chars) > self.length:
                self.chars.pop()
            self.last_char_ms = ticks_ms()

    def reset(self):
        self.length = random.randint(5, 10)
        head = self.particles[0]
        head.position = self.source
        head.velocity = random_vector(10.0)
        head.acceleration = random_vector(0.5)
        self.particles = [head]
        self.scale = random.uniform(1, 3)
        self.size = self.scale * self.char_height
        self.chars = [random_char() for i in range(self.length)]
        self.char_rate = random.uniform(50, 250) * (1.0 / head.velocity.length()) + 50
        # self.char_rate = 150
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
        length = len(self.particles)
        colours_length = len(self.tail_colours)
        for particle in self.particles:
            if i == 0:
                display.set_pen(self.head_colour)
            else:
                ci = int(i / length * colours_length - 1)
                display.set_pen(self.tail_colours[ci])

            display.character(
                self.chars[i], int(particle.position.x), int(particle.position.y), scale=int(self.scale)
            )
            i+=1
        # self.display.text(''.join([chr(c) for c in self.chars]), int(self.position.x), int(self.position.y), scale = self.size)


def random_char():
    return random.randint(33, 126)

# MicroPython compatibility
def ticks_ms():
    return time.ticks_ms()
    # return int(time.time() * 1000)
