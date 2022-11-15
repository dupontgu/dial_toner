from adafruit_hid.keyboard import Keyboard as AdaKeyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid
import time

class Keyboard():
    def __init__(self):
        self.ada_keyboard = AdaKeyboard(usb_hid.devices)
        self.keyboard_layout = KeyboardLayoutUS(self.ada_keyboard)

    def write_string(self, str, mode):
        mode.write(str, self.ada_keyboard, self.keyboard_layout)

class UsKeyboardMode:
    def write(self, str, ada_keyboard, keyboard_layout):
        # since underlying adafruit keyboard_layout is US based, we don't need to change anything here
        keyboard_layout.write(str)

    def __str__(self):
        return "US"

# compared to US mode, this reverses the '#' and '£' symbols.
class BritishKeyboardMode:
    def write(self, str, ada_keyboard, keyboard_layout):
        if str[0] == '#':
            str = str[1:]
            ada_keyboard.press(Keycode.LEFT_ALT)
            ada_keyboard.press(Keycode.THREE) 
            time.sleep(.02)
            ada_keyboard.release_all()
            time.sleep(.02)
        keyboard_layout.write(str)

    def __str__(self):
        return "UK"

class IntlKeyboardMode:
    def write(self, str, ada_keyboard, keyboard_layout):
        if str[0] == '#':
            str = str[1:]
            ada_keyboard.press(Keycode.POUND)
            time.sleep(.02)
            ada_keyboard.release_all()
            time.sleep(.02)
        keyboard_layout.write(str)

    def __str__(self):
        return "INTL"


ALL_KEYBOARD_MODES = [
    UsKeyboardMode(),
    BritishKeyboardMode(),
    IntlKeyboardMode()
]