import tuftyboard
import time
import colours
import oscillator

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

WIDTH, HEIGHT = display.get_bounds()

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]

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

oscX = oscillator.Oscillator(oscillator.fps_to_sample_rate(20), 440.0)
oscY = oscillator.Oscillator(oscillator.fps_to_sample_rate(20), 330.0)

# Initialize the time of the last frame

while True:
    tufty.tick()
    fps = tufty.get_fps()
    # draw background
    display.set_pen(BLACK)
    display.clear()
    # draw text
    display.set_pen(MAGENTA)
    display.text(f"fps: {fps}", 0, 0)

    oscX.tick()
    oscY.tick()
    x = int(((oscX.get_sin_value()+1.0)/2.0) * WIDTH)
    y = int(((oscY.get_cos_value()+1.0)/2.0) * HEIGHT)
    display.set_pen(CYAN)
    display.circle(x, y, 10)
    x = int(((oscX.get_cos_value()+1.0)/2.0) * WIDTH)
    y = int(((oscY.get_sin_value()+1.0)/2.0) * HEIGHT)
    display.set_pen(VIOLET)
    display.circle(x, y, 10)

    # Once all the adjusting and drawing is done, update the display.
    display.update()
    # time.sleep(0.25)
    # break