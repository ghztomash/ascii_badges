import tuftyboard
import time
import colours
import _thread
import oscillator
from particles import Vector, AsciiChain, random_vector

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

WIDTH, HEIGHT = display.get_bounds()

FONTS = [
    "bitmap6",
    "bitmap8",
]

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
pink = colours.Colour(255, 175, 200).set_saturation(1.0)
violet = colours.Colour(115, 41, 130).set_saturation(1.0)
PENS_MAGENTA = magenta.create_fade(display, 8)
PENS_PINK = pink.create_fade(display, 8)
PENS_VIOLET = violet.create_fade(display, 8)


osc = oscillator.Oscillator(oscillator.fps_to_sample_rate(20), 80.0)
center = Vector(WIDTH / 2, HEIGHT / 2)

MAX_SIZE = 10
chains = []
for i in range(MAX_SIZE):
    if i % 3 == 0:
        pens = PENS_MAGENTA
    elif i % 3 == 1:
        pens = PENS_PINK
    else:
        pens = PENS_VIOLET
    chains.append(AsciiChain(display, WHITE, pens, center, random_vector(5), length=4))


lock = _thread.allocate_lock()

def core1_thread():
    print("core1 thread")
    while True:
        osc.tick()
        x = int(osc.get_sin_value() * 40)
        y = int(osc.get_cos_value() * 40)

        lock.acquire()
        for chain in chains:
        # update particle
            chain.update()
            if chain.is_offscreen():
                offset = Vector(x, y)
                chain.source = center + offset
                chain.reset()
        lock.release()
        time.sleep_ms(10)

_thread.start_new_thread(core1_thread, ())

display.set_font(FONTS[1])
while True:
    tufty.tick()

    # draw background
    display.set_pen(BLACK)
    display.clear()

    # draw text
    display.set_pen(MAGENTA)
    tufty.draw_fps()

    lock.acquire()
    for chain in chains:
        # draw particle
        chain.draw()
    lock.release()
    # Once all the adjusting and drawing is done, update the display.
    display.update()
