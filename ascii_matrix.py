# A name badge with customisable flag background.
import random
import time
import colours

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

WIDTH, HEIGHT = display.get_bounds()

# List of available pen colours, add more if necessary
RED = display.create_pen(209, 34, 41)
ORANGE = display.create_pen(246, 138, 30)
YELLOW = display.create_pen(255, 216, 0)
GREEN = display.create_pen(0, 121, 64)
INDIGO = display.create_pen(36, 64, 142)
VIOLET = display.create_pen(115, 41, 130)
WHITE = display.create_pen(255, 255, 255)
PINK = display.create_pen(255, 175, 200)
BLUE = display.create_pen(116, 215, 238)
BROWN = display.create_pen(97, 57, 21)
BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(32, 32, 32)
MAGENTA = display.create_pen(255, 33, 140)
CYAN = display.create_pen(33, 177, 255)

# generate a list of pens with varying brightness values
magenta = colours.Colour(255, 33, 140)
PENS = magenta.create_fade(display, 8)

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]
CHARACTER_HEIGHTS = [6, 8, 14, 8, 8, 8, 8, 8]

# How fast the rain should fall. In config, we change it according to screen.
FALLING_SPEED = 20

# The max number of falling rains. In config, we change it according to screen.
MAX_RAIN_COUNT = 15

def get_chars():
    l = [i for i in range(33, 127)]
    # half-width katakana. See https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
    # l.extend([chr(i) for i in range(0xFF66, 0xFF9D)])
    return l

CODE_CHARS = get_chars()

def random_char():
    return random.choice(CODE_CHARS)

def random_rain_length():
    return random.randint(5, 30)

def random_rain_x():
    return random.randint(0, WIDTH)

def random_rain_speed():
    return random.randint(5, FALLING_SPEED)

class rain_drop:
    def __init__(self, colour):
        self.reset()
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
        display.set_pen(WHITE)
        self.chars.insert(0, random_char())
        if len(self.chars) > self.length:
            self.chars.pop()
        display.character(self.chars[0], self.x, self.y, scale=self.scale)
        # draw tail
        length = len(self.chars)
        for i in range(1, length):
            ci = int(i / length * (len(self.colour) - 1)) 
            display.set_pen(self.colour[ci])
            display.character(self.chars[i], self.x, self.y - (i * self.char_height), scale=self.scale)

    def is_offscreen(self):
        return self.y > HEIGHT + self.length * self.char_height
    
    def tick(self):
        self.move()
        self.draw()
        if self.is_offscreen():
            self.reset()

class Matrix:
    def __init__(self, max, pens):# array of rain drops
        self.drops = []
        for _ in range(max):
            self.drops.append(rain_drop(pens))

    def draw(self):
        for drop in self.drops:
            drop.tick()

display.set_font(FONTS[1])
matrix = Matrix(MAX_RAIN_COUNT, PENS)

while True:
# draw background
  display.set_pen(BLACK)
  display.clear()

  matrix.draw()

  display.update()
  time.sleep(0.025)  # this number is how frequently Tufty checks for button presses

# draw_ascii(0, 0, scale=2, fixed_width=True)