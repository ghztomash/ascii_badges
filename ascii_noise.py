
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
from noise import noise
import random
import time
import colours
import resize
from math import sin, cos, pi

WIDTH, HEIGHT = display.get_bounds()
SCALE = 3

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
# ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
ascii_chars = "$@B%8&MW#*haokbdpqwmZO0QLJCJYXzcvunxrjft/\\|)(1}{][?-_+~i!lI;:,\"^`"

# generate a list of pens with varying brightness values
magenta = colours.Colour(255, 33, 140)
PENS = magenta.create_fade(display, 8)

noise_size = (14, 10)
noise_cache = []

#initialize noise_cache
for x in range(noise_size[0]):
    noise_cache.append([])
    for y in range(noise_size[1]):
        noise_cache[x].append(0)

# cache noise map at a given scale and point
def cache_noise(scale, x, y):
    global noise_cache
    for x in range(len(noise_cache)):
        for y in range(len(noise_cache[x])):
            noise_cache[x][y] = (noise(x/(1.0 * scale), y/(1.0 * scale)) + 1.0) / 2.0

# get noise value at a given point from the cache
def get_cached_noise(x, y):
    x = int(x/WIDTH * (noise_size[0]-1))
    y = int(y/HEIGHT * (noise_size[1]-1))
    # print(f"x: {x}, y: {y}")
    # print(f"len: {len(interpolated_noise)}")
    val = noise_cache[x][y]
    return val

def get_pen_at_index(float_index):
    size = len(PENS)
    index = int((size-1) * float_index)
    if index < 0:
        index = 0
    # dont want the last pen
    if index >= size - 1:
        index = size - 2
    return PENS[index]

def get_char_at_index(string, float_index):
    size = len(string)
    index = int((size-1) * float_index)
    if index < 0:
        index = 0
    if index >= size:
        index = size - 1
    return string[index]

# fill the screen with pixels
def pixel_noise(scale=1, ascii=True, pixels=False):
    x = 0
    y = 0
    columns = (WIDTH // (8 * scale)) #+ 1
    rows = HEIGHT // (8 * scale) + 1
    for i in range(columns * rows):
        ic = get_cached_noise(x, y)
        # ic = random.randint(0, 127) / 127.0
        # print(ix)
        display.set_pen(get_pen_at_index(ic))
        if pixels:
            display.rectangle(x, y, 8*scale, 8*scale)
        if ascii:
            char = get_char_at_index(ascii_chars, ic)
            display.set_pen(get_pen_at_index(0))
            display.text(char, x, y, scale=scale)
        x += 8 * scale
        if x > WIDTH:
            x = 0
            y += 8 * scale

display.set_font(FONTS[1])

r = 1
theta = 0
theta_inc = 0.025

while True:
    # draw background
    display.set_pen(BLACK)
    display.clear()

    x = r * sin(theta)
    y = r * cos(theta)
    theta = (theta + theta_inc) % (pi * 2)

    cache_noise(10, x, y)
    pixel_noise(SCALE, True, True)

    display.update()
    time.sleep(0.025)  # this number is how frequently Tufty checks for button presses
    break