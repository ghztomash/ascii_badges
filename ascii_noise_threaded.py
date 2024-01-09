import tuftyboard
import time
import noise
import perlin_noise
import random
import colours
import _thread
from pimoroni import Button

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB565
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False, repeat_time = 1000, hold_time = 0 )
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
AUTO_BRIGHTNESS = True

WIDTH, HEIGHT = display.get_bounds()

# List of available pen colours, add more if necessary
RED = display.create_pen(0xff, 0x55, 0x55)
GREEN = display.create_pen(0x50, 0xfa, 0x7b)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

# generate a list of pens with varying brightness values
magenta = colours.Colour(0xff, 0x79, 0xc6).set_saturation(1.0)
PENS = magenta.create_fade(display, 8)

ascii_chars = "$@B%8&MW#*hokbdpqwmZO0QLJCJYXzcvunxrjft/\\|)(1}{][?-_+~i!lI;:,\"^`"

display.set_font("bitmap8")

debug_mode = False

def setup(scale: int = 3):
    global GRID_W, GRID_H, GRID_SIZE, grid, read_index, write_index, SCALE, BOX, buffer_size
    SCALE = scale
    BOX = SCALE * 8

    GRID_W= (WIDTH // (8 * SCALE)) + 1
    GRID_H= HEIGHT // (8 * SCALE)
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

def calculate_grid(index):
    calculate_grid_perlinInt(index)

lock = _thread.allocate_lock()

core_benchmark = 0

def core1_thread():
    print("core1 thread")
    global write_index, read_index, grid, core_benchmark
    t = 0
    lock.acquire()
    for i in range(0, buffer_size):
        write_index = i
        calculate_grid(0)
    write_index = 1
    lock.release()

    noise_func = perlin_noise.NoiseInt
    grid_w = GRID_W
    grid_size = GRID_SIZE

    g = [0] * grid_size
    while True:
        before = time.ticks_ms()
        z = t << 10

        for i in range(grid_size):
            g[i] = (noise_func((i % grid_w) << 11, (i // grid_w) << 11, z) + 65536) >> 9

        lock.acquire()
        grid[write_index] = g
        write_index = (write_index + 1) % buffer_size
        read_index = (read_index + 1) % buffer_size
        lock.release()

        t += 1
        after = time.ticks_ms()

        core_benchmark = after - before
        # print(f"core1: {core_benchmark}")
        # print(f"read_index: {read_index} write_index: {write_index}")
        time.sleep_ms(1)

def draw_grid():
    global grid_benchmark, draw_benchmark
    before = time.ticks_ms()
    
    lock.acquire()
    g = grid[read_index]
    lock.release()

    after = time.ticks_ms()
    grid_benchmark = after - before

    before = time.ticks_ms()
    for y in range(0, GRID_H):
        for x in range(0, GRID_W):
            index = (y * GRID_W) + x
            value = g[index] >> 5
            pen = PENS[value]
            display.set_pen(pen)
            # display.rectangle(x * BOX, y * BOX, BOX, BOX)
            value = g[index] >> 2
            char = ascii_chars[value]
            # display.set_pen(WHITE)
            display.text(char, x * BOX, y * BOX, scale=SCALE)
    after = time.ticks_ms()
    draw_benchmark = after - before

def draw_debug():
    # draw text
    ly = 0
    display.set_pen(GREEN)
    tufty.draw_fps(scale=2)
    ly += 20
    display.text("Grid: " + str(grid_benchmark), 0, ly)
    ly += 20
    display.text("Draw: " + str(draw_benchmark), 0, ly)
    ly += 20
    display.text("Core1: " + str(core_benchmark), 0, ly)
    ly += 20
    display.text(f"{GRID_W}x{GRID_H} grid of {GRID_SIZE} pixels", 0, ly)

setup(scale=2)
_thread.start_new_thread(core1_thread, ())

while True:
    if button_c.is_pressed:
        debug_mode = not debug_mode
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

    draw_grid()
    if debug_mode:
        draw_debug()

    # Once all the adjusting and drawing is done, update the display.
    display.update()