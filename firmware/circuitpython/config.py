from color_util import *

# export a hex string representation of a color: #FF00FF
OUTPUT_HEX = 0
# export 3 8-bit RGB ints: 255 0 255
OUTPUT_RGB = 1
# export CMYK as float percentages: 0.333 0.444 0.555 0.666
OUTPUT_CMYK = 2
# export HSL as hue value (int), then float percentages: 50 0.333 0.444
OUTPUT_HSL = 3
DEFAULT_OUTPUT = OUTPUT_HEX

# add spaces between each discrete value in color: 255 0 255 (for R G B)
USE_SPACES = 0
# add tabs between each discrete value in color: 255    0   255 (for R G B)
USE_TABS = 1
# add commas between each discrete value in color: 255,0,255 (for R G B)
USE_COMMA = 2
DEFAULT_WS = USE_SPACES

# export only the color value when button pressed
APPEND_NONE = 0
# export the color, followed by a return character
APPEND_ENTER = 1
DEFAULT_APPEND = APPEND_ENTER

DEFAULT_BRIGHTNESS = 0.3

class Config:
    def __init__(
        self,
        output_mode=DEFAULT_OUTPUT,
        whitespace_mode=DEFAULT_WS,
        append_key=DEFAULT_APPEND,
        brightness=DEFAULT_BRIGHTNESS
    ):
        self._output_mode = output_mode
        self._whitespace_mode = whitespace_mode
        self._append_key = append_key
        self._brightness = brightness

    def __str__(self):
        return "mode={}, ws={}, ak={}, bright={}".format(self.output_mode, self.whitespace_mode, self.append_key, self.brightness)

    def whitespace_mode(self, value):
        if value > USE_COMMA:
            value = DEFAULT_WS
        self._whitespace_mode = value

    whitespace_mode = property(lambda s: s._whitespace_mode, whitespace_mode)

    def output_mode(self, value):
        if value > OUTPUT_HSL:
            value = DEFAULT_OUTPUT
        self._output_mode = value

    output_mode = property(lambda s: s._output_mode, output_mode)

    def append_key(self, value):
        if value > APPEND_ENTER:
            value = DEFAULT_APPEND
        self._append_key = value

    append_key = property(lambda s: s._append_key, append_key)

    def brightness(self, value):
        if value > 1:
            value = 1
        self._brightness = value

    brightness = property(lambda s: s._brightness, brightness)

    def sequence_for_rgb(self, rgb_int):
        seq = ""
        if self.output_mode == OUTPUT_HEX:
            seq = self.hex_sequence(rgb_int)
        elif self.output_mode == OUTPUT_RGB:
            seq = self.rgb_sequence(rgb_int)
        elif self.output_mode == OUTPUT_CMYK:
            seq = self.cmyk_sequence(rgb_int)
        elif self.output_mode == OUTPUT_HSL:
            seq = self.hsl_sequence(rgb_int)

        if self.append_key == APPEND_ENTER:
            seq += "\n"
        return seq

    def delimeter(self):
        if self.whitespace_mode == USE_SPACES:
            return " "
        elif self.whitespace_mode == USE_TABS:
            return "\t"
        elif self.whitespace_mode == USE_COMMA:
            return ","
        return ""

    def hex_sequence(self, rgb_int):
        hex_components = [four_bit_hex(n) for n in rgb_tuple(rgb_int)]
        return "#" + "".join(hex_components).upper()

    def rgb_sequence(self, rgb_int):
        rgb_str = [str(i) for i in rgb_tuple(rgb_int)]
        return self.delimeter().join(rgb_str)

    def cmyk_sequence(self, rgb_int):
        cmyk = rgb_to_cmyk(*rgb_tuple(rgb_int))
        cmyk_str = [str(i) for i in cmyk]
        return self.delimeter().join(cmyk_str)

    def hsl_sequence(self, rgb_int):
        hsl = rgb_to_hsl(*rgb_tuple(rgb_int))
        hsl_str = [str(i) for i in hsl]
        return self.delimeter().join(hsl_str)
