import random
from picographics import PicoGraphics, DISPLAY_TUFTY_2040

class RainDrop:
    def __init__(self, display, colour, speed):
        self.display = display
        WIDTH, HEIGHT = display.get_bounds()
        self.width = WIDTH
        self.height = HEIGHT
        self.speed = speed
        self.colour = colour
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.width)
        self.y = 0
        self.length = random.randint(5, 30)
        self.speed = random.randint(5, self.speed)
        self.chars = [self.random_char()]
        self.scale = random.randint(1, 3)
        self.char_height = self.scale * 8

    def move(self):
        self.y += self.speed

    def draw(self):
        self.chars.insert(0, self.random_char())
        if len(self.chars) > self.length:
            self.chars.pop()
        # draw head
        self.display.set_pen(self.colour[0])
        self.display.character(self.chars[0], self.x, self.y, scale=self.scale)
        # draw tail
        length = len(self.chars)
        for i in range(1, length):
            ci = int(i / length * (len(self.colour) - 1)) 
            self.display.set_pen(self.colour[ci])
            self.display.character(self.chars[i], self.x, self.y - (i * self.char_height), scale=self.scale)

    def is_offscreen(self):
        return self.y > self.height + self.length * self.char_height

    def tick(self):
        self.move()
        self.draw()
        if self.is_offscreen():
            self.reset()

    def random_char(self):
        return random.randint(33, 127)

class Matrix:
    def __init__(self, display, max_size, pens, max_speed):# array of rain drops
        self.drops = []
        for _ in range(max_size):
            self.drops.append(RainDrop(display, pens, max_speed))

    def draw(self):
        for drop in self.drops:
            drop.tick()