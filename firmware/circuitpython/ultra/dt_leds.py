import neopixel
import board

BUTTON_BRIGHTNESS = 0.1

pixels = neopixel.NeoPixel(board.D4, 5, brightness=0.8, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

def set_led_bg_color(rgb_tuple):
    pixels[0] = tuple(round(BUTTON_BRIGHTNESS * c) for c in rgb_tuple)
    pixels.show()

def set_knob_leds(colors):
    for i in range(4):
        pixels[4 - i] = colors[i]
    pixels.show()
