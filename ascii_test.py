# A name badge with customisable flag background.

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

WIDTH, HEIGHT = display.get_bounds()

# List of available pen colours, add more if necessary
RED = display.create_pen(209, 34, 41)
ORANGE = display.create_pen(246, 138, 30)
YELLOW = display.create_pen(255, 216, 0)
GREEN = display.create_pen(0, 121, 64)
INDIGO = display.create_pen(36, 64, 142)
VIOLET = display.create_pen(115, 41, 130)
WHITE = display.create_pen(255, 255, 255)
PINK = display.create_pen(255, 175, 200)
BLUE = display.create_pen(116, 215, 238)
BROWN = display.create_pen(97, 57, 21)
BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(32, 32, 32)
MAGENTA = display.create_pen(255, 33, 140)
CYAN = display.create_pen(33, 177, 255)

# Uncomment one of these to change flag
# If adding your own, colour order is left to right (or top to bottom)
#COLOUR_ORDER = [BLACK] 
COLOUR_ORDER = [VIOLET, BLACK] 
# COLOUR_ORDER = [RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET]  # traditional pride flag
# COLOUR_ORDER = [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET]  # Philadelphia pride flag
# COLOUR_ORDER = [BLUE, PINK, WHITE, PINK, BLUE]  # trans flag
# COLOUR_ORDER = [MAGENTA, YELLOW, CYAN]  # pan flag
# COLOUR_ORDER = [MAGENTA, VIOLET, INDIGO]  # bi flag

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]

# Change details here! Works best with a short, one word name
TEXT = "37c3"

# Change the colour of the text (swapping these works better on a light background)
TEXT_COLOUR = WHITE
DROP_SHADOW_COLOUR = GREY

# Draw the flag
stripe_width = round(HEIGHT / len(COLOUR_ORDER))
for x in range(len(COLOUR_ORDER)):
    display.set_pen(COLOUR_ORDER[x])
    display.rectangle(0, stripe_width * x, WIDTH, stripe_width)

# Set a starting scale for text size.
# This is intentionally bigger than will fit on the screen, we'll shrink it to fit.
text_size = 80
text_y = 0


display.set_font("bitmap6")
# display.set_font("bitmap8")
# display.set_font("bitmap14_outline")
# display.set_font("sans")
# display.set_font("gothic")
# display.set_font("cursive")
# display.set_font("serif")

display.set_thickness(2)

# These loops adjust the scale of the text until it fits on the screen
while True:
    text_length = display.measure_text(TEXT, text_size)
    text_height = display.measure_text("A", text_size)
    text_y = int((HEIGHT - text_height) / 2.0) 

    if text_length >= WIDTH:
        text_size -= 1
    else:
        # center the text in the middle of the screen
        print(f"Height: {text_height}")
        print(f"y: {text_y} size: {text_size}")

        # comment out this section if you hate drop shadow
        DROP_SHADOW_OFFSET = 5
        display.set_pen(DROP_SHADOW_COLOUR)
        display.text(TEXT, int((WIDTH - text_length) / 2 + 10) - DROP_SHADOW_OFFSET, text_y + DROP_SHADOW_OFFSET, WIDTH, text_size)

        # draw name and stop looping
        display.set_pen(TEXT_COLOUR)
        display.text(TEXT, int((WIDTH - text_length) / 2 + 10), text_y, WIDTH, text_size)
        break

# Once all the adjusting and drawing is done, update the display.
display.update()