from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from os import listdir
import time, gc, sys
import machine
from pimoroni import Button
import tuftyboard

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
tufty = tuftyboard.TuftyBoard(display)
tufty.tick()

debug_mode = False

@micropython.native
def get_applications():
    # fetch a list of the applications that are stored in the filesystem
    applications = []
    for file in listdir():
        if file.endswith(".py") and file != "main.py":
            # convert the filename from "something_or_other.py" to "Something Or Other"
            # via weird incantations and a sprinkling of voodoo
            title = " ".join([v[:1].upper() + v[1:] for v in file[:-3].split("_")])

            applications.append(
                {
                    "file": file,
                    "title": title
                }
            )
    # sort the application list alphabetically by title and return the list
    return sorted(applications, key=lambda x: x["title"])

@micropython.native
def launch_application(application):
    #wait_for_user_to_release_buttons()

    for k in locals().keys():
        if k not in ("gc", "file", "badger_os"):
            del locals()[k]

    gc.collect()
    __import__(application["file"])

applications = get_applications()

# Tufty constants
#A = 7
#B = 8
#C = 9
#UP = 22
#DOWN = 6
#LED = 25

button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_a = Button(7, invert=False)
button_c = Button(9, invert=False)

# display.set_backlight(1.0)

@micropython.native
def text(text, x, y, pen, s):
    display.set_pen(pen)
    display.text(text, x, y, -1, s)


selected_item = 2
scroll_position = 2
target_scroll_position = 2

selected_pen = display.create_pen(0xdb, 0x93, 0xf9)
unselected_pen = display.create_pen(0x44, 0x47, 0x5a)
background_pen = display.create_pen(0x00, 0x00, 0x00)
debug_pen = display.create_pen(0x50, 0xfa, 0x7b)

while True:
    t = time.ticks_ms() / 1000.0
        
    if button_up.read():
        target_scroll_position -= 1
        target_scroll_position = target_scroll_position if target_scroll_position >= 0 else len(applications) - 1

    if button_down.read():
        target_scroll_position += 1
        target_scroll_position = target_scroll_position if target_scroll_position < len(applications) else 0

    if button_a.read():
        launch_application(applications[selected_item])

    if button_c.read():
        debug_mode = not debug_mode

    display.set_pen(background_pen)
    display.clear()

    tufty.tick()

    scroll_position += (target_scroll_position - scroll_position) / 5
    
    # work out which item is selected (closest to the current scroll position)
    selected_item = round(target_scroll_position)
    
    for list_index, application in enumerate(applications):
        distance = list_index - scroll_position

        text_size = 4 if selected_item == list_index else 3

        # center text horixontally
        title_width = display.measure_text(application["title"], text_size)
        text_x = int(160 - title_width / 2)
        
        row_height = text_size * 5 + 20
        
        # center list items vertically
        text_y = int(120 + distance * row_height - (row_height / 2))
        
        text_pen = selected_pen if selected_item == list_index else unselected_pen
        text(application["title"], text_x, text_y, text_pen, text_size)

    if debug_mode:
        ly = 5
        text(f"FPS: {tufty.get_fps():.2f}", 5, ly, debug_pen, 2)
        ly += 15
        battery = tufty.get_battery()
        battery_level = str(tufty.get_battery_percentage()) + "% " if not battery[1] else "USB "
        text("Bat: " + battery_level + str(battery[0]) + "V", 5, ly, debug_pen, 2)
        ly += 15
        text(f"Temp: {tufty.get_temperature():.2f}C", 5, ly, debug_pen, 2)
        ly += 15
        text(f"Lux: {tufty.get_brightness()[0]:.0f}", 5, ly, debug_pen, 2)
        ly += 15
        text("Mem: " + str(gc.mem_free()), 5, ly, debug_pen, 2)
        ly += 15
        text("Cpu: " + str(machine.freq() / 1_000_000) + " MHz", 5, ly, debug_pen, 2)
        ly += 15
        version = sys.version.split(";")[1].split(",")[0].strip()
        text(str(version), 5, ly, debug_pen, 2)
        ly += 15

    display.update()
    gc.collect()
    time.sleep(0.025)
