import tuftyboard
import time
import noise
import perlin_noise
import random

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

WIDTH, HEIGHT = display.get_bounds()

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]

# List of available pen colours, add more if necessary
RED = display.create_pen(209, 34, 41)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(33, 177, 255)

display.set_font(FONTS[1])

grid_size = 20*20
# grid 1d array of values 
grid = [0] * grid_size


def calculate_grid_random(index):
    g = grid
    for i in range(0, grid_size):
        g[i] = random.randint(0 , 255) + index


def calculate_grid_simplex(index):
    g = grid
    for i in range(0, grid_size):
        g[i] = noise.noise(i+index)

def calculate_grid_perlin(index):
    g = grid
    for i in range(0, grid_size):
        g[i] = perlin_noise.NoiseFloat(i+index)

def calculate_grid_perlinI(index):
    g = grid
    for i in range(0, grid_size):
        g[i] = perlin_noise.NoiseInt(i+index)


while True:
    tufty.tick()

    # draw background
    display.set_pen(BLACK)
    display.clear()
    # draw text
    display.set_pen(CYAN)
    tufty.draw_fps(scale=2)

    before = time.ticks_ms()
    calculate_grid_random(0)
    after = time.ticks_ms()
    ly = 20
    display.text("Random: " + str(after - before), 0, ly)

    before = time.ticks_ms()
    calculate_grid_simplex(0)
    after = time.ticks_ms()
    ly += 20
    display.text("Simplex: " + str(after - before), 0, ly)

    before = time.ticks_ms()
    calculate_grid_perlin(0)
    after = time.ticks_ms()
    ly += 20
    display.text("PerlinF: " + str(after - before), 0, ly)

    before = time.ticks_ms()
    calculate_grid_perlinI(0)
    after = time.ticks_ms()
    ly += 20
    display.text("PerlinI: " + str(after - before), 0, ly)

    # Once all the adjusting and drawing is done, update the display.
    display.update()