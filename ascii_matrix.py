# A name badge with customisable flag background.
import tuftyboard
import random
import time
import colours
from matrix import Matrix
from pimoroni import Button

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
AUTO_BRIGHTNESS = True

WIDTH, HEIGHT = display.get_bounds()

# List of available pen colours, add more if necessary
BACKGROUND = display.create_pen(0x28, 0x2a, 0x36)
FOREGROUND = display.create_pen(0xf8, 0xf8, 0xf2)
CYAN = display.create_pen(0x8b, 0xe9, 0xfd)
GREEN = display.create_pen(0x50, 0xfa, 0x7b)
ORANGE = display.create_pen(0xff, 0xb8, 0x6c)
PINK = display.create_pen(0xff, 0x79, 0xc6)
PURPLE = display.create_pen(0xbd, 0x93, 0xf9)
RED = display.create_pen(0xff, 0x55, 0x55)
YELLOW = display.create_pen(0xf1, 0xfa, 0x8c)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
MAGENTA = display.create_pen(255, 33, 140)
BLUE = display.create_pen(116, 215, 238)
VIOLET = display.create_pen(115, 41, 130)
INDIGO = display.create_pen(36, 64, 142)

# generate a list of pens with varying brightness values
magenta = colours.Colour(0xff, 0x79, 0xc6).set_saturation(1.0)
PENS = magenta.create_fade(display, 8)

FONTS = ["bitmap6", "bitmap8"]
CHARACTER_HEIGHTS = [6, 8, 14, 8, 8, 8, 8, 8]

# How fast the rain should fall. In config, we change it according to screen.
FALLING_SPEED = 20

# The max number of falling rains. In config, we change it according to screen.
MAX_RAIN_COUNT = 15

display.set_font(FONTS[1])
matrix = Matrix(display, MAX_RAIN_COUNT, WHITE, PENS, FALLING_SPEED)

while True:
    if button_up.is_pressed:
        AUTO_BRIGHTNESS = False
        display.set_backlight(1.0)
    if button_down.is_pressed:
        AUTO_BRIGHTNESS = True

    if AUTO_BRIGHTNESS:
        tufty.tick()
    # draw background
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(GREEN)
    tufty.draw_fps()

    matrix.draw()

    display.update()