# A name badge with customisable flag background.
import random
import time
import colours
from matrix import Matrix
from pimoroni import Button
import tuftyboard

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332, PEN_RGB565
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB565)

tufty = tuftyboard.TuftyBoard(display)
tufty.tick()
# board control

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
AUTO_BRIGHTNESS = True

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
magenta = colours.Colour(255, 33, 140).set_saturation(1.0)
PENS = magenta.create_fade(display, 8)

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]
CHARACTER_HEIGHTS = [6, 8, 14, 8, 8, 8, 8, 8]

# How fast the rain should fall. In config, we change it according to screen.
FALLING_SPEED = 20

# The max number of falling rains. In config, we change it according to screen.
MAX_RAIN_COUNT = 15


display.set_font(FONTS[1])
matrix = Matrix(display, MAX_RAIN_COUNT, MAGENTA, PENS, FALLING_SPEED)

# Change details here! Works best with a short, one word name
NAME = "37c3"
PRONOUNS = "UNLOCKED"

# Change the colour of the text (swapping these works better on a light background)
TEXT_COLOUR = WHITE
DROP_SHADOW_COLOUR = BLACK
# Set a starting scale for text size.
# This is intentionally bigger than will fit on the screen, we'll shrink it to fit.
name_size = 20
pronouns_size = 20

def resize_text():
    global name_size, name_length
    global pronouns_size, pronouns_length
    name_size = 20
    pronouns_size = 20
    # These loops adjust the scale of the text until it fits on the screen
    while True:
        name_length = display.measure_text(NAME, name_size)
        if name_length >= WIDTH - 20:
            name_size -= 1
        else:
            break

    while True:
        pronouns_length = display.measure_text(PRONOUNS, pronouns_size)
        if pronouns_length >= WIDTH - 60:
            pronouns_size -= 1
        else:
            break

resize_text()

while True:
    if button_a.is_pressed:
        NAME = ""
        PRONOUNS = ""
        resize_text()
    if button_b.is_pressed:
        NAME = "37c3"
        PRONOUNS = "UNLOCKED"
        resize_text()
    if button_c.is_pressed:
        NAME = " "
        PRONOUNS = "@TOMASH.GHZ"
        resize_text()
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
    display.set_pen(MAGENTA)
    tufty.draw_fps()
    matrix.draw()

    DROP_SHADOW_OFFSET = 5
    display.set_pen(DROP_SHADOW_COLOUR)
    display.text(NAME, int((WIDTH - name_length) / 2 + 10) - DROP_SHADOW_OFFSET, 10 + DROP_SHADOW_OFFSET, WIDTH, name_size)

    # draw name and stop looping
    display.set_pen(TEXT_COLOUR)
    display.text(NAME, int((WIDTH - name_length) / 2 + 10), 10, WIDTH, name_size)

    display.set_pen(TEXT_COLOUR)
    display.text(PRONOUNS, int((WIDTH - pronouns_length) / 2), 175, WIDTH, pronouns_size)

    display.update()
#   time.sleep(0.025)  # this number is how frequently Tufty checks for button presses

# draw_ascii(0, 0, scale=2, fixed_width=True)