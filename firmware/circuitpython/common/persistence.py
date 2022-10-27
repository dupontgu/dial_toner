import microcontroller
from config import Config

CONF_VERSION = 0
CONF_REBOOT_BUTTON_CTR = 1
CONF_OP_MODE = 2
CONF_WS_MODE = 3
CONF_APPEND_MODE = 4
CONF_BRIGHTNESS = 5

# write this immediately
# migrations can go here, if necessary
microcontroller.nvm[CONF_VERSION] = 1

def write_config(config):
    microcontroller.nvm[CONF_OP_MODE] = config.output_mode
    microcontroller.nvm[CONF_WS_MODE] = config.whitespace_mode
    microcontroller.nvm[CONF_APPEND_MODE] = config.append_key
    microcontroller.nvm[CONF_BRIGHTNESS] = round(config.brightness * 255)


def read_config():
    output_mode = microcontroller.nvm[CONF_OP_MODE]
    if output_mode == 0xFF:
        return Config()
    whitespace_mode = microcontroller.nvm[CONF_WS_MODE]
    append_key = microcontroller.nvm[CONF_APPEND_MODE]
    brightness = microcontroller.nvm[CONF_BRIGHTNESS] / 255.0
    return Config(
        output_mode=output_mode, whitespace_mode=whitespace_mode, append_key=append_key, brightness=brightness
    )

def get_reboot_button_count():
    return microcontroller.nvm[CONF_REBOOT_BUTTON_CTR]

def set_reboot_button_count(count):
    microcontroller.nvm[CONF_REBOOT_BUTTON_CTR] = count
