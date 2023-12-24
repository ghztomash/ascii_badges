from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import math, time
from colours import hsv_to_rgb

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)

WIDTH, HEIGHT = display.get_bounds()

display.set_backlight(1.0)
display.set_font('bitmap8')

message = "DEAD C0DE CAFE!"
text_size = 10
message_width = display.measure_text(message, text_size)

x_scroll = 0

while 1:
    t = time.ticks_ms() / 1000.0
    display.set_pen(display.create_pen(50, 50, 50))
    display.clear()

    x_scroll -= 10
    if x_scroll < -(message_width + 100):
        x_scroll = WIDTH - 10
    
    # for each character we'll calculate a position and colour, then draw it
    for i in range(0, len(message)):
        cx = int(x_scroll + (i * text_size * 5.5))
        cy = int(80 + math.sin(t * 10 + i) * 10)
        
        # to speed things up we only bother doing the hardware if the character will be visible on screen
        if cx > -50 and cx < 320:
            # draw a shadow for the character
            display.set_pen(display.create_pen(0, 0, 0))
            display.text(message[i], cx + 15, cy + 15, -1, text_size)
            
            # generate a rainbow colour that cycles with time
            r, g, b = hsv_to_rgb(i / 10 + t / 5, 1, 1)        
            display.set_pen(display.create_pen(r, g, b))
            display.text(message[i], cx, cy, -1, text_size)

    display.update()
