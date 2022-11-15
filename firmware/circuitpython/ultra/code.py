
from dt_display import DialTonerDisplay
from knobs import any_knob_has_turned_within
from dt_keyboard import Keyboard
from modes import SettingsMode
from dt_leds import set_all_led_brightness, set_led_bg_color, set_knob_leds, DEFAULT_BRIGHTNESS
import board
import time
from persistence import read_config, write_config
from config_params import all_params
from pio_button import PioButton

IDLE_TIME_THRESHOLD = 1200

display = DialTonerDisplay()
keyboard = Keyboard()
button = PioButton(board.D3)
config = read_config()
idle_time = 0

def settings_mode():
    display.hide_logo()
    display.refresh()
    settings_mode = SettingsMode(read_config(), all_params)
    led_color = (100, 100, 100)
    hold_released = False
    while True:
        settings_mode.refresh()
        set_led_bg_color(led_color, settings_mode.config.brightness_float)
        # flash LEDs while in settings mode
        set_all_led_brightness(0 if round(time.monotonic() * 1.5) % 2 == 0 else DEFAULT_BRIGHTNESS)
        for button_status in button.events:
            if not button_status.pressed:
                # make sure we're not reacting to the release from the initial hold that got us into settings mode
                if not hold_released:
                    hold_released = True
                    continue
                # button newly pressed, save config and exit settings mode
                write_config(settings_mode.config)
                set_all_led_brightness(DEFAULT_BRIGHTNESS)
                time.sleep(0.2)
                return
        display.update_with(settings_mode)
        set_knob_leds(settings_mode.knob_led_colors)
        display.refresh()

    
while True:
    for button_status in button.events:
        if button_status.hold_time >= 30 and button_status.pressed:
            settings_mode()
            config = read_config()
        elif button_status.hold_time < 30 and not button_status.pressed:
            str_value = config.sequence_for_rgb(mode.as_rgb)
            print("btn pressed:", mode.as_rgb, str_value)
            keyboard.write_string(str_value, config.keyboard_mode_obj)
    mode = config.input_mode_obj
    mode.refresh()
    actively_turning = any_knob_has_turned_within(3)
    logo_showing = display.logo_showing
    if actively_turning:
        # device was idle, but now user is turning knobs - bring everything back to default brightness
        if idle_time >= IDLE_TIME_THRESHOLD:
            set_all_led_brightness(DEFAULT_BRIGHTNESS)
        idle_time = 0
        if logo_showing:
            display.hide_logo()
        display.update_with(mode)
        set_led_bg_color(mode.as_rgb, config.brightness_float)
    # done turning knobs, go back to displaying logo
    elif not logo_showing and idle_time < IDLE_TIME_THRESHOLD:
        display.show_logo()
    else:
        idle_time += 1
        # device is idle - dim the lights and hide everying from screen to prevent burn in
        if idle_time == IDLE_TIME_THRESHOLD:
            set_all_led_brightness(0.1)
            display.hide_logo()
            display.update_bg_color(0x000)
            display.refresh(force=True)
    set_knob_leds(mode.knob_led_colors)
    display.refresh()
