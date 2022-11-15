import rp2pio
import adafruit_pioasm
import time

button_input_asm = """
.program hc_output
.wrap_target
    in pins 1
    nop [10]
.wrap
"""

class ButtonState:
    __slots__ = ("pressed", "hold_time")
    def __init__(self, pressed, hold_time):
        self.pressed = pressed
        self.hold_time = hold_time

    def __str__(self):
        return "pressed={}, hold_count={}".format(self.pressed, self.hold_time)

# Reads input from onboard button by sampling pin via PIO
# Allows us to sample in the "background" into a buffer, and then process input events when we're unblocked
# Context - the "ultra" version of the DT has screen updates that block for upwards of ~0.5 seconds. This is plenty of time to miss a button press.
class PioButton:
    def __init__(self, pin, sample_frequency=5000):
        self.sm = rp2pio.StateMachine(
            program = adafruit_pioasm.assemble(button_input_asm),
            frequency = sample_frequency,
            first_in_pin=pin,
            in_pin_count=1,
            pull_in_pin_up=1,
            auto_push=True,
        )   
        self.sm.restart()
        self.short_buf = bytearray(1)
        self.long_buf = bytearray(8)
        self.hold_counter = 0

    @property
    def events(self):
        buf = self.long_buf if self.sm.in_waiting > 1 else self.short_buf
        self.sm.readinto(buf)
        events = []
        for b in buf:
            if b != 0xff:
                if self.hold_counter == 0:
                    events.append(ButtonState(True, 0))
                self.hold_counter += 1
            elif self.hold_counter > 0:
                events.append(ButtonState(False, self.hold_counter))
                self.hold_counter = 0
        if self.hold_counter > 0:
            events.append(ButtonState(True, self.hold_counter))
        return events

    def newly_pressed(self):
        for e in self.events:
            if e.hold_time == 0 and e.pressed:
                return True
        return False



