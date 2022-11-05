import neopixel
import board

DEFAULT_BRIGHTNESS = 0.8

pixels = neopixel.NeoPixel(board.D4, 5, brightness=DEFAULT_BRIGHTNESS, auto_write=False)
built_in = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=DEFAULT_BRIGHTNESS, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

def set_led_bg_color(rgb_tuple, brightness):
    adj_c = tuple(round(brightness * c) for c in rgb_tuple)
    pixels[0] = adj_c
    built_in[0] = adj_c
    pixels.show()
    built_in.show()

def set_knob_leds(colors):
    for i in range(4):
        pixels[4 - i] = colors[i]
    pixels.show()

def set_all_led_brightness(brightness):
    pixels.brightness = brightness
    built_in.brightness = brightness
    built_in.show()
    pixels.show()
