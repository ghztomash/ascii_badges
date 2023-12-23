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