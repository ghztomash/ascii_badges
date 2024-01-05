# A name badge with customisable flag background.
import tuftyboard
import random
import time
import colours
from matrix import Matrix

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332, PEN_RGB565
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB565)

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

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
matrix = Matrix(display, MAX_RAIN_COUNT, WHITE, PENS, FALLING_SPEED)

while True:
  # draw background
  display.set_pen(BLACK)
  display.clear()
  display.set_pen(MAGENTA)
  tufty.tick()
  tufty.draw_fps()

  matrix.draw()

  display.update()
#   time.sleep(0.025)  # this number is how frequently Tufty checks for button presses

# draw_ascii(0, 0, scale=2, fixed_width=True)