import microcontroller
from config import Config

CONF_VERSION = 0
CONF_REBOOT_BUTTON_CTR = 1
CONF_OP_MODE = 2
CONF_WS_MODE = 3
CONF_APPEND_MODE = 4
CONF_BRIGHTNESS = 5
CONF_IP_MODE = 6
CONF_KEYBOARD_MODE = 7



# run migrations here
if microcontroller.nvm[CONF_VERSION] == 1:
    # used to be stored from 0-255, reduced options from 0-10. Default to low-ish value.
    microcontroller.nvm[CONF_BRIGHTNESS] = 3
    print("migrating from persistance 1 -> 2")

# write this immediately after migrations
microcontroller.nvm[CONF_VERSION] = 2

def write_config(config):
    microcontroller.nvm[CONF_OP_MODE] = config.output_mode
    microcontroller.nvm[CONF_WS_MODE] = config.whitespace_mode
    microcontroller.nvm[CONF_APPEND_MODE] = config.append_key
    microcontroller.nvm[CONF_BRIGHTNESS] = config.brightness
    microcontroller.nvm[CONF_IP_MODE] = config.input_mode
    microcontroller.nvm[CONF_KEYBOARD_MODE] = config.keyboard_mode

def read_config():
    output_mode = microcontroller.nvm[CONF_OP_MODE]
    # indicates that config has never been persisted, so return all default values
    if output_mode == 0xFF:
        return Config()
    whitespace_mode = microcontroller.nvm[CONF_WS_MODE]
    append_key = microcontroller.nvm[CONF_APPEND_MODE]
    brightness = microcontroller.nvm[CONF_BRIGHTNESS]
    input_mode = microcontroller.nvm[CONF_IP_MODE]
    keyboard_mode = microcontroller.nvm[CONF_KEYBOARD_MODE]
    return Config(
        output_mode=output_mode, input_mode=input_mode, whitespace_mode=whitespace_mode, append_key=append_key, brightness=brightness, keyboard_mode=keyboard_mode
    )

def get_reboot_button_count():
    return microcontroller.nvm[CONF_REBOOT_BUTTON_CTR]

def set_reboot_button_count(count):
    microcontroller.nvm[CONF_REBOOT_BUTTON_CTR] = count
