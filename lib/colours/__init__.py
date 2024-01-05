from picographics import PicoGraphics, DISPLAY_TUFTY_2040

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

# convert rgb values to hsv in the range 0f 0.0 - 1.0
def rgb_to_hsv(r, g, b):
	r, g, b = r / 255.0, g / 255.0, b / 255.0

	cmax = max(r, g, b)
	cmin = min(r, g, b)
	diff = cmax - cmin

	if cmax == cmin:
		h = 0
	elif cmax == r:
		h = (60 * ((g - b) / diff) + 360) % 360
	elif cmax == g:
		h = (60 * ((b - r) / diff) + 120) % 360
	elif cmax == b:
		h = (60 * ((r - g) / diff) + 240) % 360
	else:
		h = 0

	if cmax == 0:
		s = 0
	else:
		s = (diff / cmax) * 100

	v = cmax * 100
	return h / 360.0, s / 100.0, v / 100.0

class Colour:
    def __init__(self, r, g, b):
        self.set_rgb(r, g, b)

    def set_rgb(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        hsv = rgb_to_hsv(r, g, b)
        self.h = hsv[0]
        self.s = hsv[1]
        self.v = hsv[2]
    
    def set_hue(self, hue):
        self.h = hue
        rgb = hsv_to_rgb(hue, self.s, self.v)
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
    
    def set_saturation(self, saturation):
        self.s = saturation
        rgb = hsv_to_rgb(self.h, saturation, self.v)
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
        return self
    
    def set_value(self, value):
        self.v = value
        rgb = hsv_to_rgb(self.h, self.s, value)
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

    def set_hsv(self, h, s, v):
        self.h = h
        self.s = s
        self.v = v
        rgb = hsv_to_rgb(h, s, v)
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

    def __str__(self):
        return "Colour({}, {}, {})".format(self.r, self.g, self.b)

    def create_pen(self, display, brightness=1.0):
        return display.create_pen_hsv(self.h, self.s, self.v * brightness)
    
    def create_fade(self, display, count=8):
        PENS = []
        for i in range(count):
            iv = 1.0 - (i / float(count))
            PENS.append(self.create_pen(display, iv))
        return PENS