# This example reads the voltage from a battery connected to Tufty 2040
# and uses this reading to calculate how much charge is left in the battery.

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import tuftyboard
import machine
from pimoroni import Button

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
tufty = tuftyboard.TuftyBoard(display)

button_c = Button(9, invert=False)

# set up some colours to draw with
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(190, 190, 190)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)

display.set_font("bitmap8")

while True:
    if button_c.read():
        machine.soft_reset()
    
    tufty.tick()
    (vbat, on_usb, low_battery) = tufty.get_battery()
    percentage = tufty.get_battery_percentage()

    # Print out the voltage
    print("Battery Voltage = ", vbat, "V", sep="")

    # draw the battery outline
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(GREY)
    display.rectangle(0, 0, 220, 135)
    display.rectangle(220, 40, 20, 55)
    display.set_pen(WHITE)
    display.rectangle(3, 3, 214, 129)

    # draw a green box for the battery level
    display.set_pen(GREEN)
    display.rectangle(5, 5, int((210 / 100) * percentage), 125)

    # add text
    display.set_pen(RED)
    if on_usb:         # if it's plugged into USB power...
        display.text("USB power!", 15, 90, 240, 4)

    display.text('{:.2f}'.format(vbat) + "v", 15, 10, 240, 5)
    display.text('{:.0f}%'.format(percentage), 15, 50, 240, 5)

    display.update()
    time.sleep(0.5)
