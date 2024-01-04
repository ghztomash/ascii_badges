# This example shows you a simple, non-interrupt way of reading Tufty 2040's buttons with a loop that checks to see if buttons are pressed.

import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from machine import ADC, Pin, PWM

led = PWM(Pin(25))
led.freq(1000)
led.duty_u16(32768)

led_value = 0
led_increment = 0.025

lux_pwr = Pin(27, Pin.OUT)
lux_pwr.value(1)

lux = ADC(26)
vbat = ADC(29)
vref = ADC(28)

display = PicoGraphics(display=DISPLAY_TUFTY_2040)

brightness = 1.0

display.set_backlight(brightness)
display.set_font("bitmap8")

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
TEAL = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
RED = display.create_pen(255, 0, 0)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)
DARK_BLUE = display.create_pen(0, 0, 127)

WIDTH, HEIGHT = display.get_bounds()

button = ""
is_pressed = False
time_pressed = time.ticks_ms()
color = BLACK

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def press_button(b, c):
    global button
    button = b
    global is_pressed
    is_pressed = True
    global time_pressed
    time_pressed = time.ticks_ms()
    global color
    color = c

while True:
    if button_a.is_pressed:                               # if a button press is detected then...
        press_button("a", WHITE)
    elif button_b.is_pressed:
        press_button("b", TEAL)
    elif button_c.is_pressed:
        press_button("c", MAGENTA)
    elif button_up.is_pressed:
        press_button("up", YELLOW)
        brightness = clamp(brightness + 0.1, 0.4, 1)
        display.set_backlight(brightness)
    elif button_down.is_pressed:
        display.set_pen(GREEN)
        press_button("down", GREEN)
        brightness = clamp(brightness - 0.1, 0.4, 1)
        display.set_backlight(brightness)
        print(brightness)


    display.set_pen(BLACK)
    display.clear()
    display.set_pen(RED)
    display.text("Press any button!", 10, 10, WIDTH, 3)
    
    if is_pressed:
        display.set_pen(color)
        display.text(f"Button {button} pressed", 10, 50, WIDTH - 10, 3)
        if time.ticks_diff(time.ticks_ms(), time_pressed) > 1000:
            is_pressed = False
    # display.text(f"{is_pressed} {button} {color}", 10, 80, WIDTH - 10, 3)
    
    lux_reading = lux.read_u16()
    vbat_reading = (vbat.read_u16() / 65535) * 3.3
    vref_reading = (vref.read_u16() / 65535) * 3.3
    
    display.set_pen(DARK_BLUE)
    display.text(f"led= {led_value:.2f}\nlux= {lux_reading}\nvref= {vref_reading:.3f}v\nvbat= {vbat_reading:.3f}v", 10, HEIGHT-120, WIDTH, 3)
    display.update()
    
    if led_value >= 1.0 or led_value <= 0.0:
        led_increment *= -1.0
    led_value += led_increment
    led_value = clamp(led_value,0,1)
    led.duty_u16(int(led_value*65535.0))

    time.sleep(0.05)  # this number is how frequently Tufty checks for button presses
