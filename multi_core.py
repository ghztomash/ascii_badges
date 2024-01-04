import tuftyboard
import time
import colours
import machine
import utime
import micropython
import _thread

from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = micropython.const(PicoGraphics(display=DISPLAY_TUFTY_2040))

# board control
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

WIDTH, HEIGHT = display.get_bounds()

FONTS = [
    "bitmap6",
    "bitmap8",
    "bitmap14_outline",
    "sans",
    "gothic",
    "cursive",
    "serif",
    "serif_italic",
]

# List of available pen colours, add more if necessary
RED = display.create_pen(255, 0, 0)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

display.set_font(FONTS[1])

led = machine.PWM(machine.Pin(25))
led.freq(1000)
led.duty_u16(0)

led_value = 1
led_increment = 20

lock = _thread.allocate_lock()


def core1_thread():
    lock.acquire()
    global led_value, led_increment
    lock.release()
    while True:
        lock.acquire()
        if led_value > 65534 or led_value < 1:
            led_increment *= -1
        led_value += led_increment
        led.duty_u16(led_value)
        lock.release()
        utime.sleep_ms(1)


def core2_thread():
    while True:
        print("core2")
        utime.sleep_ms(1000)


def core0_thread():
    while True:
        tufty.tick()
        # draw background
        display.set_pen(BLACK)
        display.clear()
        # draw text
        display.set_pen(RED)
        tufty.draw_fps(2)
        # lock.acquire()
        # display.text(f"led value: {led_value}", 2, 40, scale=1)
        # lock.release()
        # Once all the adjusting and drawing is done, update the display.
        display.update()


_thread.start_new_thread(core1_thread, ())
# _thread.start_new_thread(core2_thread, ())
core0_thread()
