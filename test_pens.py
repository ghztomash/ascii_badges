import tuftyboard
import time
import colours

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332, PEN_RGB565
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB565)

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

WIDTH, HEIGHT = display.get_bounds()

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]

# List of available pen colours, add more if necessary
RED = display.create_pen(255, 0, 0)
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

display.set_font(FONTS[0])

# generate a list of pens with varying brightness values
# blue resolution only 4 shades, green 8, red 8
white = colours.Colour(255, 255, 255)
PENS = white.create_fade(display, count=128)
print(f"pens: {PENS}")

BOX = 20
W = WIDTH // BOX

# draw background
display.set_pen(BLACK)
display.clear()

for i in range(0, len(PENS)):
    display.set_pen(PENS[i])
    x = i % W
    y = i // W
    display.rectangle(x * BOX, y * BOX, BOX, BOX)
    
    # draw text
    display.set_pen(RED)
    display.text(f"{i}", x * BOX + 2, y * BOX + 2, 0, 0, 0)

# Once all the adjusting and drawing is done, update the display.
display.update()