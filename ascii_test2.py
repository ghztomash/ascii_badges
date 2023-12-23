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
COLOUR_ORDER = [BLACK] 
# COLOUR_ORDER = [VIOLET, BLACK] 
# COLOUR_ORDER = [RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET]  # traditional pride flag
# COLOUR_ORDER = [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET]  # Philadelphia pride flag
# COLOUR_ORDER = [BLUE, PINK, WHITE, PINK, BLUE]  # trans flag
# COLOUR_ORDER = [MAGENTA, YELLOW, CYAN]  # pan flag
# COLOUR_ORDER = [MAGENTA, VIOLET, INDIGO]  # bi flag

FONTS = ["bitmap6", "bitmap8", "bitmap14_outline", "sans", "gothic", "cursive", "serif", "serif_italic"]
ASCII = "!#$%&'()*+,-./0123456789:;<=>?@ABCD EFGHIJKLMNOPQRSTUVWXYZ[]^_`abcde fghijklmnopqrstuvwxyz{|}~ "
BLOCK_ELEMENTS = "▀▁▂▃▄▅▆▇█ ▌▐▖▗▘▙▚▛▜▝▞▟"
BOX_ELEMENTS = "─│┌┐└┘├┤┬┴┼ ╔╗╚╝╠╣╦╩╬"
DOS_ELEMENTS = "☺☻♥♦♣♠•◘○◙ ♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼"

FIGLET1 = """
 __________    _____ 
|___ /___  |__|___ / 
  |_ \  / / __| |_ \ 
 ___) |/ / (__ ___) |
|____//_/ \___|____/ 
"""

FIGLET2 = """
      :::::::: ::::::::::: ::::::::  :::::::: 
    :+:    :+::+:     :+::+:    :+::+:    :+: 
          +:+       +:+ +:+              +:+  
      +#++:       +#+  +#+           +#++:    
        +#+     +#+   +#+              +#+    
#+#    #+#    #+#    #+#    #+##+#    #+#     
########     ###     ########  ########       
"""

FIGLET3 = """
:'#######::'########::'######:::'#######::
'##.... ##: ##..  ##:'##... ##:'##.... ##:
..::::: ##:..:: ##::: ##:::..::..::::: ##:
:'#######::::: ##:::: ##::::::::'#######::
:...... ##::: ##::::: ##::::::::...... ##:
'##:::: ##::: ##::::: ##::: ##:'##:::: ##:
. #######:::: ##:::::. ######::. #######::
:.......:::::..:::::::......::::.......:::
"""

FIGLET4 = """
_|_|_|    _|_|_|_|_|            _|_|_|    
      _|          _|    _|_|_|        _|  
  _|_|          _|    _|          _|_|    
      _|      _|      _|              _|  
_|_|_|      _|          _|_|_|  _|_|_|    
"""

FIGLET5 = """
 .::.  ...:::::  .,-::::: .::.    
;'`';;,'''``;;',;;;'````';'`';;,  
   .n[[    .[' [[[          .n[[  
  ``"$$$.,$$'  $$$         ``"$$$.
  ,,o888"888   `88bo,__,o, ,,o888"
  YMMP"  MMM     "YUMMMMMP"YMMP"  
"""

# function to draw all decimal ascii characters
def draw_ascii(x, y, scale=1, fixed_width=False):
    for i in range(32, 127):
    # for i in range(127, 160):
        #display.text(chr(i), x, y, scale=scale)
        display.character(i, x, y, scale=scale)
        x += 9 * scale
        if x > WIDTH:
            x = 0
            y += 9 * scale

CHARACTER_SETS = [ASCII, BLOCK_ELEMENTS, BOX_ELEMENTS, DOS_ELEMENTS, FIGLET1, FIGLET2, FIGLET3]

# Change details here! Works best with a short, one word name
TEXT = "37c3"

# Change the colour of the text (swapping these works better on a light background)
TEXT_COLOUR = WHITE
DROP_SHADOW_COLOUR = GREY

display.clear()

# Draw the flag
stripe_width = round(HEIGHT / len(COLOUR_ORDER))
for x in range(len(COLOUR_ORDER)):
    display.set_pen(COLOUR_ORDER[x])
    display.rectangle(0, stripe_width * x, WIDTH, stripe_width)

# Set a starting scale for text size.
# This is intentionally bigger than will fit on the screen, we'll shrink it to fit.
text_size = 80
text_y = 0


display.set_font(FONTS[1])

display.set_thickness(3)

# draw background
display.set_pen(MAGENTA)
# display.text(FIGLET3, 0, 0, scale=1, fixed_width=True)

draw_ascii(0, 0, scale=2, fixed_width=True)

# Once all the adjusting and drawing is done, update the display.
display.update()

