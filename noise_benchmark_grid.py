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
PENS = white.create_fade(display, 8)

display.set_font(FONTS[1])

GRID_W = WIDTH // 10
GRID_H = HEIGHT // 10
GRID_SIZE = GRID_W * GRID_H 
# grid 1d array of values 
grid = [0] * GRID_SIZE

# 11ms
def calculate_grid_random(index):
    g = grid
    for i in range(0, GRID_SIZE):
        g[i] = random.randint(0 , 255)

# 494ms
def calculate_grid_simplex(index):
    g = grid
    x = 0
    y = 0
    z = index
    for i in range(0, GRID_SIZE):
        x = i % GRID_W
        y = i // GRID_W
        g[i] = int((noise.noise(x * 0.1 + index, y * 0.1) + 1.0 ) / 2.0 * 255)

# 534ms
def calculate_grid_perlin(index):
    g = grid
    x = 0
    y = 0
    z = index
    for i in range(0, GRID_SIZE):
        x = i % GRID_W
        y = i // GRID_W
        g[i] = int((perlin_noise.NoiseFloat(x * 0.1, y * 0.1, z) + 1.0) / 2.0 * 255)

# 437ms
def calculate_grid_perlinInt(index):
    g = grid
    x = 0
    y = 0
    z = index << 13
    for i in range(0, GRID_SIZE):
        x = i % GRID_W
        y = i // GRID_W
        g[i] = (perlin_noise.NoiseInt(x << 13, y << 13, z) + 65536) >> 9

# 428ms
def calculate_grid_noise(index=0):
    z = index << 13
    noise_func = perlin_noise.NoiseInt
    grid_w = GRID_W
    grid_size = GRID_SIZE

    g = [
        (noise_func((i % grid_w) << 13, (i // grid_w) << 13, z) + 65536) >> 9
        for i in range(grid_size)
    ]

    global grid
    grid = g

def calculate_grid(index):
    calculate_grid_perlinInt(index)

i = 0
while True:
    tufty.tick()

    # draw background
    display.set_pen(BLACK)
    display.clear()
    ly = 0

    before = time.ticks_ms()
    calculate_grid(i)
    after = time.ticks_ms()
    grid_benchmark = after - before
    i += 1

    before = time.ticks_ms()
    for y in range(0, GRID_H):
        for x in range(0, GRID_W):
            index = (y * GRID_W) + x
            value = grid[index] >> 5
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
    ly += 20
    display.text(f"{GRID_W}x{GRID_H} grid of {GRID_SIZE} pixels", 0, ly)

    # Once all the adjusting and drawing is done, update the display.
    display.update()