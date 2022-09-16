
import time
from persistence import get_reboot_button_count, read_config, set_reboot_button_count, write_config
from button import Button
from rainbowio import colorwheel
import hex_input
from dt_keyboard import Keyboard
from led_wrapper import LedWrapper
from color_util import gamma_correction

btn = Button()
keyboard = Keyboard()
pixel = LedWrapper()

colorwheel_count =  0

config = read_config()
write_config(config)

def colorwheel_color():
    global colorwheel_count
    colorwheel_count += 0.2
    if colorwheel_count > 255:
        colorwheel_count = 0
    return colorwheel(colorwheel_count)

def read_bytes_as_rgb_int():
    (r, g, b) = hex_input.read_bytes()
    return r << 16 | g << 8 | b

def gamma_corrected_rgb_int(rgb_int):
    r = rgb_int >> 16
    g = (rgb_int >> 8) & 0xFF
    b = rgb_int & 0xFF
    return gamma_correction[r] << 16 | gamma_correction[g] << 8 | gamma_correction[b]

def get_brightness_from_bytes(bytes):
    # divisor scales the brightness down, should be at least 16
    return ((bytes[1] & 0x0F) / 32)

def commit_config_selection(bytes):
    config.output_mode = bytes[0] >> 4
    config.whitespace_mode = bytes[0] & 0x0F
    config.append_key = bytes[1] >> 4
    config.brightness = get_brightness_from_bytes(bytes)
    write_config(config)
    print(config)

def config_mode_selection_made():
    while True:
        reading = hex_input.read_bytes()
        if btn.newly_pressed():
            return commit_config_selection(reading)
        btn.update()
        pixel.fill(colorwheel_color())
        # blink at selected brightness
        pixel.brightness = 0 if int(time.monotonic() * 4) % 2 == 0 else get_brightness_from_bytes(reading)
        pixel.show()
        time.sleep(0.001)

def config_mode():
    pixel.brightness = config.brightness
    starting_bytes = hex_input.read_bytes()
    while True:
        reading = hex_input.read_bytes()
        if reading != starting_bytes:
            return config_mode_selection_made()
        elif btn.newly_pressed():
            return None
        btn.update()
        # slow pulse
        pixel.fill(colorwheel_color())
        pixel.show()
        time.sleep(0.001)

if btn.newly_pressed():
    button_count = get_reboot_button_count() + 1
    if button_count == 1:
        set_reboot_button_count(1)
        # this will block until user exits config mode  
        config_mode()
        set_reboot_button_count(0)
else:
    set_reboot_button_count(0)

print("config: ", config)

rgb = None

while True:
    new_rgb = read_bytes_as_rgb_int()
    if new_rgb != rgb:
        rgb = new_rgb
        print(hex(rgb))
        pixel.fill(gamma_corrected_rgb_int(rgb))
        pixel.brightness = config.brightness
        pixel.show()
    btn.update()
    time.sleep(0.01)
    if btn.newly_pressed():
        str_value = config.sequence_for_rgb(rgb)
        print("btn pressed:", rgb, str_value)
        keyboard.write_string(str_value)

    





