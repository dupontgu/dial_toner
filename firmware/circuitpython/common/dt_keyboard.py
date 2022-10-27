from adafruit_hid.keyboard import Keyboard as AdaKeyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid

class Keyboard():
    def __init__(self):
        keyboard = AdaKeyboard(usb_hid.devices)
        self.keyboard_layout = KeyboardLayoutUS(keyboard)

    def write_string(self, str):
        self.keyboard_layout.write(str)