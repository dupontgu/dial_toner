from config import Config, INPUT_VALS, BRIGHTNESS_VALS, OUTPUT_VALS, KEYBOARD_VALS

class ConfigParam:
    def __init__(self, name, setter, getter, values):
        self.name = name
        self.setter = setter
        self.getter = getter
        self.values = values

    def set(self, instance, value):
        self.setter(instance, value)

    def get(self, instance):
        return self.getter(instance)

all_params = [
    ConfigParam("MODE", Config.set_input_mode, lambda p: p.input_mode,  INPUT_VALS),
    ConfigParam("BTN BRT", Config.set_brightness, lambda p: p.brightness, BRIGHTNESS_VALS),
    ConfigParam("OUTPUT", Config.set_output_mode, lambda p: p.output_mode,  OUTPUT_VALS),
    ConfigParam("KEYBRD", Config.set_keyboard_mode, lambda p: p.keyboard_mode,  KEYBOARD_VALS)
]