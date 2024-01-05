import tuftyboard
import time
import noise
import perlin_noise
import random
import colours
import _thread

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332, PEN_RGB565
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB565)

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
PENS = white.create_fade(display, count=32)

display.set_font(FONTS[1])

BOX = 20

GRID_W = WIDTH // BOX
GRID_H = HEIGHT // BOX
GRID_SIZE = GRID_W * GRID_H 
# grid 2d array of values 
grid = []
buffer_size = 4
for _ in range(0, buffer_size):
    grid.append([0] * GRID_SIZE)

read_index = 0
write_index = 0

# 11ms
def calculate_grid_random(index):
    g = grid
    for i in range(0, GRID_SIZE):
        g[write_index][i] = random.randint(0 , 255)

# 494ms
def calculate_grid_simplex(index):
    g = grid
    x = 0
    y = 0
    z = index
    for i in range(0, GRID_SIZE):
        x = i % GRID_W
        y = i // GRID_W
        g[write_index][i] = int((noise.noise(x * 0.1 + index, y * 0.1) + 1.0 ) / 2.0 * 255)

# 534ms
def calculate_grid_perlin(index):
    g = grid
    x = 0
    y = 0
    z = index
    for i in range(0, GRID_SIZE):
        x = i % GRID_W
        y = i // GRID_W
        g[write_index][i] = int((perlin_noise.NoiseFloat(x * 0.1, y * 0.1, z) + 1.0) / 2.0 * 255)

# 437ms
def calculate_grid_perlinInt(index):
    g = grid
    x = 0
    y = 0
    z = index << 13
    for i in range(0, GRID_SIZE):
        x = i % GRID_W
        y = i // GRID_W
        g[write_index][i] = (perlin_noise.NoiseInt(x << 13, y << 13, z) + 65536) >> 9

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
    grid[write_index] = g

def calculate_grid(index):
    calculate_grid_perlinInt(index)

lock = _thread.allocate_lock()

t = 0
core_benchmark = 0

def core1_thread():
    print("core1 thread")
    global t, write_index, read_index, grid, core_benchmark
    lock.acquire()
    for i in range(0, buffer_size):
        write_index = i
        calculate_grid(0)
    write_index = 1
    lock.release()

    noise_func = perlin_noise.NoiseInt
    grid_w = GRID_W
    grid_size = GRID_SIZE

    while True:
        before = time.ticks_ms()
        z = t << 10
        g = [
            (noise_func((i % grid_w) << 12, (i // grid_w) << 12, z) + 65536) >> 9
            for i in range(grid_size)
        ]

        lock.acquire()
        grid[write_index] = g.copy()
        write_index = (write_index + 1) % buffer_size
        read_index = (read_index + 1) % buffer_size
        lock.release()

        del g
        t += 1
        after = time.ticks_ms()

        core_benchmark = after - before
        # print(f"core1: {core_benchmark}")
        # print(f"read_index: {read_index} write_index: {write_index}")
        time.sleep_ms(1)


_thread.start_new_thread(core1_thread, ())

while True:
    tufty.tick()

    # draw background
    display.set_pen(BLACK)
    display.clear()
    ly = 0

    before = time.ticks_ms()
    
    lock.acquire()
    g = grid[read_index].copy()
    lock.release()

    after = time.ticks_ms()
    grid_benchmark = after - before

    before = time.ticks_ms()
    for y in range(0, GRID_H):
        for x in range(0, GRID_W):
            index = (y * GRID_W) + x
            value = g[index] >> 3
            pen = PENS[value]
            display.set_pen(pen)
            display.rectangle(x * BOX, y * BOX, BOX, BOX)
    after = time.ticks_ms()
    draw_benchmark = after - before

    g.clear()
    del g

    # draw text
    display.set_pen(RED)
    tufty.draw_fps(scale=2)
    ly += 20
    display.text("Grid: " + str(grid_benchmark), 0, ly)
    ly += 20
    display.text("Draw: " + str(draw_benchmark), 0, ly)
    ly += 20
    display.text("Core1: " + str(core_benchmark), 0, ly)
    ly += 20
    display.text(f"{GRID_W}x{GRID_H} grid of {GRID_SIZE} pixels", 0, ly)

    # Once all the adjusting and drawing is done, update the display.
    display.update()