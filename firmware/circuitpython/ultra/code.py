
from color_util import rgb_tuple
from dt_display import DialTonerDisplay
from knobs import any_knob_has_turned_within, read_knob
from modes import CmykMode, HexMode, RgbMode
from dt_leds import set_led_bg_color, set_knob_leds

mode = HexMode()
display = DialTonerDisplay()

while True:
    mode.refresh()
    actively_turning = any_knob_has_turned_within(3)
    logo_showing = display.logo_showing
    if actively_turning:
        if logo_showing:
            display.hide_logo()
        display.update_with(mode)
        set_led_bg_color(mode.as_rgb)
    elif not logo_showing:
        display.show_logo()
    display.refresh()
    set_knob_leds(mode.knob_led_colors)
