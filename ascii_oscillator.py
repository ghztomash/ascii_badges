import tuftyboard
import time
import colours
import oscillator

from particles import Particle, Vector, AsciiChain, random_vector

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332, PEN_RGB565
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB565)
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

# generate a list of pens with varying brightness values
violet = colours.Colour(115, 41, 130).set_saturation(1.0)
cyan = colours.Colour(33, 177, 255).set_saturation(1.0)
indigo = colours.Colour(36, 64, 142).set_saturation(1.0)
blue = colours.Colour(116, 215, 238).set_saturation(1.0)
PENS_VIOLET = violet.create_fade(display, 8)
PENS_CYAN = cyan.create_fade(display, 8)
PENS_INDIGO = indigo.create_fade(display, 8)
PENS_BLUE = blue.create_fade(display, 8)

MAX_SIZE = 5
SAMPLE_RATE = 40

osc = []
for i in range(MAX_SIZE):
    osc.append(oscillator.Oscillator(oscillator.fps_to_sample_rate(SAMPLE_RATE), 110.0*(i+1)))

oscFm = oscillator.Oscillator(oscillator.fps_to_sample_rate(SAMPLE_RATE), 11.0)

center = Vector(WIDTH / 2, HEIGHT / 2)

chains = []

for i in range(MAX_SIZE):
    if i % 4 == 0:
        pens = PENS_VIOLET
    elif i % 4 == 1:
        pens = PENS_CYAN
    elif i % 4 == 2:
        pens = PENS_INDIGO
    else:
        pens = PENS_BLUE
    chains.append(AsciiChain(display, WHITE, pens, center, length=8))

for chain in chains:
    chain.reset()
    chain.particles[0].position = center
    chain.particles[0].velocity = Vector(0, 0)
    chain.particles[0].acceleration = Vector(0, 0)

display.set_font(FONTS[1])
while True:
    tufty.tick()
    # draw background
    display.set_pen(BLACK)
    display.clear()
    # draw text
    display.set_pen(MAGENTA)
    tufty.draw_fps()
    oscFm.tick()

    for i, c in enumerate(osc):
        c.set_frequency(110.0*(i+1) + oscFm.get_sin_value()*10.0)
        c.tick()
        x = int(((osc[(i+1)%len(osc)].get_sin_value()+1.0)/2.0) * WIDTH)
        y = int(((osc[(i*3)%len(osc)].get_cos_value()+1.0)/2.0) * HEIGHT)
        chains[i].particles[0].position = Vector(x, y)

    for chain in chains:
        chain.update()
        chain.draw()

    # Once all the adjusting and drawing is done, update the display.
    display.update()
    # time.sleep(0.25)
    # break