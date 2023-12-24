
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
from noise import noise
import random
import time
import colours

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
GREY = display.create_pen(33, 32, 32)
MAGENTA = display.create_pen(255, 33, 140)
CYAN = display.create_pen(33, 177, 255)

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]
ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# generate a list of pens with varying brightness values
magenta = colours.Colour(255, 33, 140)
PENS = magenta.create_fade(display, 8)

def get_char_at_index(string, float_index):
    index = int((len(string)-1) * float_index)
    if index < 0:
        index = 0
    if index >= len(string):
        index = len(string) - 1
    return string[index]

# fill the screen with ascii characters
def ascii_noise(scale=1):
    x = 0
    y = 0
    columns = (WIDTH // (9 * scale)) + 1
    rows = HEIGHT // (9 * scale)
    for i in range(columns * rows):
        # ic = random.randint(0, 128) / 127.0
        ic = (noise(x/1.0, y/1.0) + 1.0) / 2.0
        char = get_char_at_index(ascii_chars, ic)
        # display.set_pen(VIOLET)
        # display.rectangle(x, y, 8*scale, 8*scale)
        # display.set_pen(MAGENTA)
        display.text(char, x, y, scale=scale)
        x += 9 * scale
        if x > WIDTH:
            x = 0
            y += 9 * scale

# fill the screen with pixels
def pixel_noise(scale=1):
    x = 0
    y = 0
    columns = (WIDTH // (8 * scale)) #+ 1
    rows = HEIGHT // (8 * scale) + 1
    for i in range(columns * rows):
        ic = (noise(x/10.0, y/10.0) + 1.0) / 2.0
        ix = int(ic * len(PENS))
        display.set_pen(PENS[ix])
        display.rectangle(x, y, 8*scale, 8*scale)
        x += 8 * scale
        if x > WIDTH:
            x = 0
            y += 8 * scale

# Change details here! Works best with a short, one word name
TEXT = "37c3"

display.set_font(FONTS[1])

# draw background
display.set_pen(MAGENTA)
# display.text(TEXT, 0, 0, scale=1, fixed_width=True)

# ascii_noise(2)
pixel_noise(1)

# Once all the adjusting and drawing is done, update the display.
display.update()

