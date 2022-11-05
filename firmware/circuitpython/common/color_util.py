
RGB_SCALE = 255
CMYK_SCALE = 1

def rgb_tuple(rgb_int):
    r = (rgb_int >> 16) & 0xFF
    g = (rgb_int >> 8) & 0xFF
    b = rgb_int & 0xFF
    return (r, g, b)

# returns a 2 character string, representing the least significant nibble
# 0 -> "00"
# 255 -> "FF"
def four_bit_hex(n):
    h = hex(n)
    if len(h) != 3:
        return h[-2:]
    else:
        return "0" + h[2:]

# yoinked from https://stackoverflow.com/questions/39118528/rgb-to-hsl-conversion
def rgb_to_hsl(r, g, b):
    r = r / RGB_SCALE
    g = g / RGB_SCALE
    b = b / RGB_SCALE

    cmin = min(r, g, b)
    cmax = max(r, g, b)
    delta = cmax - cmin
    h = 0
    s = 0
    l = 0

    if delta == 0:
        h = 0
    elif cmax == r:
        h = ((g - b) / delta) % 6
    elif cmax == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4

    h = round(h * 60)

    if h < 0:
        h += 360

    l = (cmax + cmin) / 2

    s = 0 if delta == 0 else delta / (1 - abs(2 * l - 1))

    s = round(abs(s * 100), 2)
    l = round(abs(l * 100), 2)

    return (h, s, l)

def hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    r = 0
    g = 0
    b = 0

    if (0 <= h and h < 60):
        r = c; g = x; b = 0;  
    elif (60 <= h and h < 120):
        r = x; g = c; b = 0
    elif (120 <= h and h < 180):
        r = 0; g = c; b = x
    elif (180 <= h and h < 240):
        r = 0; g = x; b = c
    elif (240 <= h and h < 300):
        r = x; g = 0; b = c
    elif (300 <= h and h < 360):
        r = c; g = 0; b = x
  
    r = round((r + m) * 255);
    g = round((g + m) * 255);
    b = round((b + m) * 255);

    return (r, g, b)


# yoinked from https://stackoverflow.com/a/14088415
def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE

def cmyk_to_rgb(c, m, y, k):
    r = RGB_SCALE * (1.0 - c / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
    g = RGB_SCALE * (1.0 - m / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
    b = RGB_SCALE * (1.0 - y / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
    return round(r), round(g), round(b)

def use_dark_text(rgb_tuple):
    (r, g, b) = rgb_tuple
    sum = ((r * 0.299) + (g * 0.587) + (b * 0.114))
    return sum > 140

# yoinked from https://learn.adafruit.com/led-tricks-gamma-correction/the-quick-fix
gamma_correction = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]
