import tuftyboard
import time
import noise
import perlin_noise
import random
import colours

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

# generate a list of pens with varying brightness values
white = colours.Colour(255, 255, 255)
PENS = white.create_fade(display, 32)

display.set_font(FONTS[1])

GRID_W = WIDTH // 10
GRID_H = HEIGHT // 10
GRID_SIZE = GRID_W * GRID_H 
# grid 1d array of values 
grid = [0] * GRID_SIZE


def calculate_grid_random(index):
    g = grid
    for i in range(0, GRID_SIZE):
        g[i] = random.randint(0 , 255) + index


def calculate_grid_simplex(index):
    g = grid
    for i in range(0, GRID_SIZE):
        g[i] = noise.noise(i+index)

def calculate_grid_perlin(index):
    g = grid
    for i in range(0, GRID_SIZE):
        g[i] = perlin_noise.NoiseFloat(i+index)

def calculate_grid_perlinI(index):
    g = grid
    for i in range(0, GRID_SIZE):
        g[i] = perlin_noise.NoiseInt(i+index)

def calculate_grid(index):
    calculate_grid_random(index)

while True:
    tufty.tick()

    # draw background
    display.set_pen(BLACK)
    display.clear()
    ly = 0

    before = time.ticks_ms()
    calculate_grid(0)
    after = time.ticks_ms()
    grid_benchmark = after - before
    

    before = time.ticks_ms()
    for y in range(0, GRID_H):
        for x in range(0, GRID_W):
            index = (y * GRID_W) + x
            value = grid[index] >> 3
            pen = PENS[value]
            display.set_pen(pen)
            display.rectangle(x*10, y*10, 10, 10)
    after = time.ticks_ms()
    draw_benchmark = after - before

    # draw text
    display.set_pen(RED)
    tufty.draw_fps(scale=2)
    ly += 20
    display.text("Grid: " + str(grid_benchmark), 0, ly)
    ly += 20
    display.text("Draw: " + str(draw_benchmark), 0, ly)

    # Once all the adjusting and drawing is done, update the display.
    display.update()