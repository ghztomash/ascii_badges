import random

def random_char():
    return random.randint(33, 127)

def random_rain_length():
    return random.randint(5, 30)

def random_rain_x():
    return random.randint(0, WIDTH)

def random_rain_speed():
    return random.randint(5, FALLING_SPEED)

class RainDrop:
    def __init__(self, display, colour):
        self.reset()
        self.display = display
        self.colour = colour

    def reset(self):
        self.x = random_rain_x()
        self.y = 0
        self.length = random_rain_length()
        self.speed = random_rain_speed()
        self.chars = [random_char()]
        self.scale = random.randint(1, 2)
        self.char_height = self.scale * 8

    def move(self):
        self.y += self.speed

    def draw(self):
        # draw head
        self.display.set_pen(WHITE)
        self.chars.insert(0, random_char())
        if len(self.chars) > self.length:
            self.chars.pop()
        self.display.character(self.chars[0], self.x, self.y, scale=self.scale)
        # draw tail
        length = len(self.chars)
        for i in range(1, length):
            ci = int(i / length * (len(self.colour) - 1)) 
            self.display.set_pen(self.colour[ci])
            self.display.character(self.chars[i], self.x, self.y - (i * self.char_height), scale=self.scale)

    def is_offscreen(self):
        return self.y > HEIGHT + self.length * self.char_height
    
    def tick(self):
        self.move()
        self.draw()
        if self.is_offscreen():
            self.reset()

class Matrix:
    def __init__(self, display, max, pens):# array of rain drops
        self.drops = []
        for _ in range(max):
            self.drops.append(RainDrop(display, pens))

    def draw(self):
        for drop in self.drops:
            drop.tick()