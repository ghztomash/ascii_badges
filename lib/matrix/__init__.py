import random
from picographics import PicoGraphics, DISPLAY_TUFTY_2040

class RainDrop:
    def __init__(self, display, colour_head, colour_tail, speed):
        self.display = display
        WIDTH, HEIGHT = display.get_bounds()
        self.width = WIDTH
        self.height = HEIGHT
        self.speed = speed
        self.colour_head = colour_head
        self.colour_tail = colour_tail
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
        self.display.set_pen(self.colour_head)
        self.display.character(self.chars[0], self.x, self.y, scale=self.scale)
        # draw tail
        length = len(self.chars)
        for i in range(1, length):
            ci = int(i / length * (len(self.colour_tail) - 1)) 
            self.display.set_pen(self.colour_tail[ci])
            self.display.character(self.chars[i], self.x, self.y - (i * self.char_height), scale=self.scale)

    def is_offscreen(self):
        return self.y > self.height + self.length * self.char_height

    def random_char(self):
        return random.randint(33, 127)

class Matrix:
    def __init__(self, display, max_size, head_pen, pens, max_speed):# array of rain drops
        self.drops = []
        self.size = max_size
        self.display = display
        self.head_pen = head_pen
        self.pens = pens
        self.max_speed = max_speed
        for _ in range(max_size):
            self.drops.append(RainDrop(display, head_pen, pens, max_speed))

    def draw(self):
        for index, drop in enumerate(self.drops):
            drop.move()
            drop.draw()
            # reset if offscreen or remove at end of array
            if drop.is_offscreen():
                if index > self.size:
                    self.drops.pop(index)
                else:
                    drop.reset()

    def set_size(self, size):
        if size > len(self.drops):
            for _ in range(size - len(self.drops)):
                self.drops.append(RainDrop(self.display, self.head_pen, self.pens, self.max_speed))
        self.size = size