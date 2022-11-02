from color_util import *
from modes import ALL_INPUT_MODES
from dt_keyboard import ALL_KEYBOARD_MODES

# Input modes: Hex, RGB, CMYK, P-Tone, etc.
INPUT_VALS = ALL_INPUT_MODES

# Keyboard layouts: US, UK, INTL
KEYBOARD_VALS = ALL_KEYBOARD_MODES

OUTPUT_VALS = [
    # export a hex string representation of a color: #FF00FF
    "HEX", 
    # export 3 8-bit RGB ints: 255 0 255
    "RGB", 
    # export CMYK as float percentages: 0.333 0.444 0.555 0.666
    "CMYK", 
    # export HSL as hue value (int), then float percentages: 50 0.333 0.444
    "HSL"
]

WHITESPACE_VALS = [
    # add spaces between each discrete value in color: 255 0 255 (for R G B)
    "Spaces", 
    # add tabs between each discrete value in color: 255    0   255 (for R G B)
    "Tabs", 
    # add commas between each discrete value in color: 255,0,255 (for R G B)
    "Commas"
]

APPEND_VALS = [
    # export the color, followed by a return character
    "Enter", 
    # export only the color value when button pressed
    "None"
]

BRIGHTNESS_VALS = [x / 10 for x in range(11)]

class Config:
    def __init__(
        self,
        input_mode=0,
        output_mode=0,
        whitespace_mode=0,
        append_key=0,
        brightness=3,
        keyboard_mode=0
    ):
        self.input_mode = input_mode
        self.output_mode = output_mode
        self.whitespace_mode = whitespace_mode
        self.append_key = append_key
        self.brightness = brightness
        self.keyboard_mode = keyboard_mode

    def __str__(self):
        return "ip={}, op={}, ws={}, ak={}, bright={}, kbd={}".format(self._input_mode, self.output_mode, self.whitespace_mode, self.append_key, self.brightness, self.keyboard_mode)

    def set_whitespace_mode(self, value):
        if value >= len(WHITESPACE_VALS):
            value = 0
        self._whitespace_mode = value

    whitespace_mode = property(lambda s: s._whitespace_mode, set_whitespace_mode)

    def set_input_mode(self, value):
        if value >= len(INPUT_VALS):
            value = 0
        self._input_mode = value

    input_mode = property(lambda s: s._input_mode, set_input_mode)

    @property
    def input_mode_obj(self):
        return INPUT_VALS[self._input_mode]

    def set_keyboard_mode(self, value):
        if value >= len(KEYBOARD_VALS):
            value = 0
        self._keyboard_mode = value

    keyboard_mode = property(lambda s: s._keyboard_mode, set_keyboard_mode)

    @property
    def keyboard_mode_obj(self):
        return KEYBOARD_VALS[self._keyboard_mode]

    def set_output_mode(self, value):
        if value >= len(OUTPUT_VALS):
            value = 0
        self._output_mode = value

    output_mode = property(lambda s: s._output_mode, set_output_mode)

    def set_append_key(self, value):
        if value >= len(APPEND_VALS):
            value = 0
        self._append_key = value

    append_key = property(lambda s: s._append_key, set_append_key)

    def set_brightness(self, value):
        if value >= len(BRIGHTNESS_VALS):
            value = len(BRIGHTNESS_VALS) - 1
        self._brightness = value

    brightness = property(lambda s: s._brightness, set_brightness)

    @property
    def brightness_float(self):
        return BRIGHTNESS_VALS[self._brightness]

    # TODO - move all sequence logic into external classes like input mode/ keyboard modes

    def sequence_for_rgb(self, rgb):
        seq = ""
        if isinstance(rgb, int):
            rgb = rgb_tuple(rgb)
        op_mode = OUTPUT_VALS[self.output_mode]
        if op_mode == "HEX":
            seq = self.hex_sequence(rgb)
        elif op_mode == "RGB":
            seq = self.rgb_sequence(rgb)
        elif op_mode == "CMYK":
            seq = self.cmyk_sequence(rgb)
        elif op_mode == "HSL":
            seq = self.hsl_sequence(rgb)

        if APPEND_VALS[self.append_key] == "Enter":
            seq += "\n"
        return seq

    def delimeter(self):
        ws_mode = WHITESPACE_VALS[self.whitespace_mode]
        if ws_mode == "Spaces":
            return " "
        elif ws_mode == "Tabs":
            return "\t"
        elif ws_mode == "Commas":
            return ","
        return ""

    def hex_sequence(self, rgb):
        hex_components = [four_bit_hex(n) for n in rgb]
        return "#" + "".join(hex_components).upper()

    def rgb_sequence(self, rgb):
        rgb_str = [str(i) for i in rgb]
        return self.delimeter().join(rgb_str)

    def cmyk_sequence(self, rgb):
        cmyk = rgb_to_cmyk(*rgb)
        cmyk_str = [str(i) for i in cmyk]
        return self.delimeter().join(cmyk_str)

    def hsl_sequence(self, rgb):
        hsl = rgb_to_hsl(*rgb)
        hsl_str = [str(i) for i in hsl]
        return self.delimeter().join(hsl_str)
