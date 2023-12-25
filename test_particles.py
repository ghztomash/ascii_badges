import tuftyboard
import time
import colours
import random
from particles import Particle, Vector


from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

# board control
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

center = Vector(WIDTH/2, HEIGHT/2)

display.set_font(FONTS[0])
particle = Particle(display, center, Vector(random.uniform(-5, 5), random.uniform(-5, 5)))

while True:
    tufty.tick()
    fps = tufty.get_fps()
    
    # update particle
    particle.update()
    if particle.is_offscreen():
        particle.position = center
        particle.velocity = Vector(random.uniform(-5, 5), random.uniform(-5, 5))
        particle.acceleration = Vector(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
        particle.size = random.uniform(5, 20)

    # draw background
    display.set_pen(BLACK)
    display.clear()
    # draw text
    display.set_pen(MAGENTA)
    display.text(f"fps: {fps}", 0, 0)

    # draw particle
    display.set_pen(CYAN)
    display.circle(int(particle.position.x), int(particle.position.y), int(particle.size))

    # Once all the adjusting and drawing is done, update the display.
    display.update()