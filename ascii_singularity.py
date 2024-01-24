import tuftyboard
import time
import math
import colours
import oscillator
import _thread

from particles import Vector, AsciiChain, random_vector

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

WIDTH, HEIGHT = display.get_bounds()

FONTS = ["bitmap6", "bitmap8"]

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
violet = colours.Colour(0xff, 0x55, 0x55)
cyan = colours.Colour(0xff, 0x79, 0xc6)
indigo = colours.Colour(0x8b, 0xe9, 0xfd)
blue = colours.Colour(0xbd, 0x93, 0xf9)
PENS_VIOLET = violet.create_fade(display, 8)
PENS_CYAN = cyan.create_fade(display, 8)
PENS_INDIGO = indigo.create_fade(display, 8)
PENS_BLUE = blue.create_fade(display, 8)

MAX_SIZE = 2
SAMPLE_RATE = 50

center = Vector(WIDTH / 2, HEIGHT / 2)

chains = []
chains.append(AsciiChain(display, WHITE, PENS_BLUE, center, scale=16, length=1, char_rate=400))
chains.append(AsciiChain(display, WHITE, PENS_BLUE, center, scale=16, length=1, char_rate=800))

for chain in chains:
    chain.reset()
    chain.particles[0].position = center 
    chain.particles[0].velocity = Vector(0, 0)
    chain.particles[0].acceleration = Vector(0, 0)

display.set_font(FONTS[1])

lock = _thread.allocate_lock()

def core1_thread():
    print("core1 thread")
    while True:
        lock.acquire()
        for chain in chains:
            chain.update()
        lock.release()
        time.sleep_ms(10)

_thread.start_new_thread(core1_thread, ())

while True:
    tufty.tick()
    # draw background
    display.set_pen(BLACK)
    display.clear()
    # draw text
    display.set_pen(GREEN)
    tufty.draw_fps()

    lock.acquire()
    for chain in chains:
        chain.draw()
    lock.release()

    # Once all the adjusting and drawing is done, update the display.
    display.update()
    # time.sleep(0.25)
    # break