import json
from knobs import read_knob
from color_util import cmyk_to_rgb, four_bit_hex, hsl_to_rgb

def format_percentage(percentage):
    adj_prcnt = percentage * 100
    if adj_prcnt == 100.0:
        return "100"
    return "%04.1f" % adj_prcnt

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

class HslMode:
    def __init__(self):
        self.hsl = (0,0,0)

    def refresh(self):
        self.hsl = (
            round(read_knob(0) * 359), 
            read_knob(1), 
            read_knob(2)
            )

    def __str__(self):
        return "HSL"

    @property
    def knob_led_colors(self):
        return [0x4455aa, 0x4455aa, 0x4455aa, 0x0]

    @property
    def display(self):
        return [
            "H: " + str(self.hsl[0]),
            "S: " + format_percentage(self.hsl[1]) + "%",
            "L: " + format_percentage(self.hsl[2]) + "%",
            ]

    @property
    def as_rgb(self):
        return hsl_to_rgb(*self.hsl)

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
            "C: " + format_percentage(self.cmyk[0]) + "%",
            "M: " + format_percentage(self.cmyk[1]) + "%",
            "Y: " + format_percentage(self.cmyk[2]) + "%",
            "K: " + format_percentage(self.cmyk[3]) + "%",
            ]

    @property
    def as_rgb(self):
        return cmyk_to_rgb(*self.cmyk)

class PToneMode:
    def __init__(self):
        self.rgb = (0,0,0)
        self.ptone_id = "0000"
        with open('ptone.json') as file:
            self.ptone_dict = json.load(file)

    def refresh(self):
        root_keys = list(self.ptone_dict.keys())
        root_keys.sort()
        dig_1 = round(read_knob(0) * (len(root_keys) - 1))
        dig_1_key = root_keys[dig_1]
        dig_2_root = self.ptone_dict[dig_1_key]
        
        dig_2_keys = list(dig_2_root.keys())
        dig_2_keys.sort()
        dig_2 = round(read_knob(1) * (len(dig_2_keys) - 1))
        dig_2_key = dig_2_keys[dig_2]
        dig_3_root = dig_2_root[dig_2_key]

        dig_3_keys = list(dig_3_root.keys())
        dig_3_keys.sort()
        dig_3 = round(read_knob(2) * (len(dig_3_keys) - 1))
        dig_3_key = dig_3_keys[dig_3]
        dig_4_root = dig_3_root[dig_3_key]

        dig_4_keys = list(dig_4_root.keys())
        dig_4_keys.sort()
        dig_4 = round(read_knob(3) * (len(dig_4_keys) - 1))
        dig_4_key = dig_4_keys[dig_4]
        self.rgb = tuple(dig_4_root[dig_4_key]["c"])

        self.ptone_id = dig_1_key + dig_2_key + dig_3_key + dig_4_key

    def __str__(self):
        return "P-Tone"

    @property
    def knob_led_colors(self):
        return [0x4400ff, 0x4400ff, 0x4400ff, 0x4400ff]

    @property
    def display(self):
        return [str(self.ptone_id)]

    @property
    def as_rgb(self):
        return self.rgb

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

    def read_knob_safe(self, index):
        return max(0, read_knob(index) - 0.01)

    def refresh(self):
        param_index = int(self.read_knob_safe(0) * len(self.params))
        active_param = self.params[param_index]
        self.param_name = active_param.name
        self.param_value = str(active_param.values[active_param.get(self.config)])
        value_index = int(self.read_knob_safe(1) * len(active_param.values))
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
        return [self.param_name + ":", self.param_value]

    @property
    def as_rgb(self):
        return (100, 140, 100)

ALL_INPUT_MODES = [
    HexMode(),
    RgbMode(),
    CmykMode(),
    PToneMode(),
    HslMode()
]