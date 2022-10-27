import board
import time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

KNOB_COUNT = 4
KNOB_UPDATE_THRESHOLD = 500

analog_in = AnalogIn(board.A0)
addr_0 = DigitalInOut(board.D1)
addr_0.direction = Direction.OUTPUT
addr_1 = DigitalInOut(board.D2)
addr_1.direction = Direction.OUTPUT

cached_knob_values = [-KNOB_UPDATE_THRESHOLD] * KNOB_COUNT
knob_update_times = [0] * KNOB_COUNT

def read_knob(index):
    set_mux_addr(index)
    reading = analog_in.value
    # If the knob's value is far enough away from the last reading, mark it's last-updated-time as now
    if (abs(reading - cached_knob_values[index])) >= KNOB_UPDATE_THRESHOLD:
        cached_knob_values[index] = reading
        knob_update_times[index] = time.monotonic()
    else: 
        reading = cached_knob_values[index]
    return (65536 - reading) / 65536

def any_knob_has_turned_within(threshold_sec):
    thresh_time = time.monotonic() - threshold_sec
    for i in range(KNOB_COUNT):
        if knob_update_times[i] > thresh_time:
            return True
    return False

def set_mux_addr(addr):
    addr_0.value = (addr & 0b0001) > 0
    addr_1.value = (addr & 0b0010) > 0
