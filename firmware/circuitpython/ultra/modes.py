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

    def __str__(self):
        return "HEX"

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
    
    def __str__(self):
        return "RGB"

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
    
    def __str__(self):
        return "CMYK"

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

class SettingsMode:
    colors = [
        0xff00ff,
        0xff5555,
        0x55bb55,
        0x33ff55,
        0x11ff22,
        0x00ff88,
        0x118888,
        0x226666,
        0x442266,
        0x881144,
        0xee4400,
    ]

    def __init__(self, config, params):
        self.current_param_index = None
        self.current_value_index = None
        self.params = params
        self.config = config
        self.param_name = ""
        self.param_value = ""

    def refresh(self):
        param_index = int(read_knob(0) * len(self.params))
        active_param = self.params[param_index]
        self.param_name = active_param.name
        self.param_value = str(active_param.values[active_param.get(self.config)])
        value_index = int(read_knob(1) * len(active_param.values))
        if self.current_param_index != param_index:
            self.current_value_index = value_index
            self.current_param_index = param_index
        elif value_index != self.current_value_index:
            self.current_value_index = value_index
            active_param.set(self.config, value_index)
            self.param_value = str(active_param.values[active_param.get(self.config)])

    @property
    def knob_led_colors(self):
        param_color = 0 if self.current_param_index is None else SettingsMode.colors[self.current_param_index]
        value_color = 0 if self.current_value_index is None else SettingsMode.colors[self.current_value_index]
        return [param_color, value_color, 0, 0]

    @property
    def display(self):
        return [self.param_name, self.param_value]

    @property
    def as_rgb(self):
        return (100, 140, 100)

ALL_INPUT_MODES = [
    HexMode(),
    RgbMode(),
    CmykMode()
]