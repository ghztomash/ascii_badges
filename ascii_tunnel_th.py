import tuftyboard
import time
import random
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
magenta = colours.Colour(0xff, 0x55, 0x55)
pink = colours.Colour(0xff, 0x79, 0xc6)
violet = colours.Colour(0xbd, 0x93, 0xf9)
PENS_MAGENTA = magenta.create_fade(display, 8)
PENS_PINK = pink.create_fade(display, 8)
PENS_VIOLET = violet.create_fade(display, 8)


osc = oscillator.Oscillator(oscillator.fps_to_sample_rate(20), 80.0)
center = Vector(WIDTH / 2, HEIGHT / 2)

MAX_SIZE = 1
chains = []
for i in range(MAX_SIZE):
    if i % 3 == 0:
        pens = PENS_MAGENTA
    elif i % 3 == 1:
        pens = PENS_PINK
    else:
        pens = PENS_VIOLET
    chains.append(AsciiChain(display, WHITE, pens, center, 
                             random_vector(5),
                             scale=random.uniform(1, 3),
                             length=random.randint(5, 10)))


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
    display.set_pen(GREEN)
    tufty.draw_fps()

    lock.acquire()
    source = chains[0].source
    for chain in chains:
        # draw particle
        chain.draw()
    lock.release()

    display.set_pen(GREEN)
    display.circle(int(source.x), int(source.y), 8)
    # Once all the adjusting and drawing is done, update the display.
    display.update()
