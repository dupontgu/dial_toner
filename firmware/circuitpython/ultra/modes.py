from knobs import read_knob
from color_util import cmyk_to_rgb, four_bit_hex

class HexMode:
    def __init__(self):
        self.rgb = (0,0,0)
        pass

    def refresh(self):
        self.rgb = (
            round(read_knob(0) * 255), 
            round(read_knob(1) * 255), 
            round(read_knob(2) * 255)
            )

    def hex_sequence(self):
        hex_components = [four_bit_hex(n) for n in self.rgb]
        return "#" + "".join(hex_components).upper()

    @property
    def knob_led_colors(self):
        return [0xFF0000, 0x00FF00, 0x0000FF, 0x000000]

    @property
    def display(self):
        return [self.hex_sequence()]

    @property
    def as_rgb(self):
        return self.rgb

class RgbMode(HexMode):
    @property
    def display(self):
        return [
            "R: " + str(self.rgb[0]),
            "G: " + str(self.rgb[1]),
            "B: " + str(self.rgb[2]),
        ]

class CmykMode:
    def __init__(self):
        self.cmyk = (0,0,0,0)

    def refresh(self):
        self.cmyk = (
            read_knob(0), 
            read_knob(1), 
            read_knob(2),
            read_knob(3)
            )

    @property
    def knob_led_colors(self):
        return [0x00FFFF, 0xFF00FF, 0xFFFF00, 0x333333]

    @property
    def display(self):
        return [
            "C: " + ("%04.1f" % (self.cmyk[0] * 100)) + "%",
            "M: " + ("%04.1f" % (self.cmyk[1] * 100)) + "%",
            "Y: " + ("%04.1f" % (self.cmyk[2] * 100)) + "%",
            "K: " + ("%04.1f" % (self.cmyk[3] * 100)) + "%",
            ]

    @property
    def as_rgb(self):
        return cmyk_to_rgb(*self.cmyk)