# Automatic brightness example.

import time
from machine import ADC, Pin
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import micropython
import tuftyboard

# Hold button A to pretend the LUX sensor is seeing maximally bright light.
# (To test darkness, put your finger over the sensor! :D )
button_a = Button(7, invert=False)
# Hold button B to pretend the system is on battery, and the battery is low.
button_b = Button(8, invert=False)
# Pins and analogue-digital converters we need to set up to measure sensors.
lux_vref_pwr = Pin(27, Pin.OUT)
lux = ADC(26)
vbat_adc = ADC(29)
vref_adc = ADC(28)
usb_power = Pin(24, Pin.IN)

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
display.set_backlight(1.0)
display.set_font("bitmap8")
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
WIDTH, HEIGHT = display.get_bounds()

tufty = tuftyboard.TuftyBoard(display)
while True:
    tufty.tick()
    (vbat, on_usb, low_battery) = tufty.get_battery()
    (luminance, backlight) = tufty.get_brightness()
    percentage = tufty.get_battery_percentage()

    # Show our measurements.
    display.set_pen(WHITE)
    display.clear()
    display.set_pen(BLACK)
    display.text(f"Backlight: {backlight * 100:03.0f}%", 8, 8, WIDTH - 8, 4)

    if low_battery:
        display.text("Luminance: Ignored, low battery!", 8, 48 + (20 * 1), WIDTH - 8, 2)
    else:
        display.text(f"Luminance: {luminance:05.0f} (of 65535)", 8, 48 + (20 * 1), WIDTH - 8, 2)
    if on_usb:
        display.text("Battery: Ignored, on USB.", 8, 48 + (20 * 2), WIDTH - 8, 2)
    else:
        display.text(f"Battery: {vbat:.2f}v, {percentage}%", 8, 48 + (20 * 2), WIDTH - 8, 2)

    display.text("Hold A to pretend the room is bright.", 8, HEIGHT - (20 * 4), WIDTH - 8, 2)
    display.text("Hold B to pretend the battery is low.", 8, HEIGHT - (20 * 2), WIDTH - 8, 2)
    display.update()

    time.sleep(0.1)
