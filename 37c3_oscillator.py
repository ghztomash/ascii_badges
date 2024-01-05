import tuftyboard
import time
import colours
import oscillator
from pimoroni import Button

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

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

# Change details here! Works best with a short, one word name
TEXT = "37c3"
# Change the colour of the text (swapping these works better on a light background)
TEXT_COLOUR = WHITE
DROP_SHADOW_COLOUR = GREY
# Set a starting scale for text size.
# This is intentionally bigger than will fit on the screen, we'll shrink it to fit.
text_size = 80
text_y = 0
AUTO_BRIGHTNESS = True

# generate a list of pens with varying brightness values
violet = colours.Colour(115, 41, 130).set_saturation(1.0)
cyan = colours.Colour(33, 177, 255).set_saturation(1.0)
indigo = colours.Colour(36, 64, 142).set_saturation(1.0)
blue = colours.Colour(116, 215, 238).set_saturation(1.0)
PENS_VIOLET = violet.create_fade(display, 8)
PENS_CYAN = cyan.create_fade(display, 8)
PENS_INDIGO = indigo.create_fade(display, 8)
PENS_BLUE = blue.create_fade(display, 8)

MAX_SIZE = 8
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

def resize_text():
    # These loops adjust the scale of the text until it fits on the screen
    global text_size, text_y, text_length
    text_size = 80
    text_y = 0
    while True:
        text_length = display.measure_text(TEXT, text_size)
        text_height = display.measure_text("A", text_size)
        text_y = int((HEIGHT - text_height) / 2.0) 

        if text_length >= WIDTH:
            text_size -= 1
        else:
            # center the text in the middle of the screen
            print(f"Height: {text_height}")
            print(f"y: {text_y} size: {text_size}")
            break

resize_text()

while True:
    if button_a.is_pressed:
        TEXT = ""
        resize_text()
    if button_b.is_pressed:
        TEXT = "37c3"
        resize_text()
    if button_c.is_pressed:
        TEXT = "@tomash.ghz"
        resize_text()
        text_y = 175
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

    # comment out this section if you hate drop shadow
    DROP_SHADOW_OFFSET = 5
    display.set_pen(DROP_SHADOW_COLOUR)
    display.text(TEXT, int((WIDTH - text_length) / 2 + 10) - DROP_SHADOW_OFFSET, text_y + DROP_SHADOW_OFFSET, WIDTH, text_size)

    # draw name and stop looping
    display.set_pen(TEXT_COLOUR)
    display.text(TEXT, int((WIDTH - text_length) / 2 + 10), text_y, WIDTH, text_size)
    # Once all the adjusting and drawing is done, update the display.
    display.update()
    # time.sleep(0.25)
    # break