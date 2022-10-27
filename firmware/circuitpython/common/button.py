import digitalio
import board

# Simple wrapper around default button for a cleaner API
# This also allows for alternate implementations where no physical button is actually present.
class Button():
    def __init__(self, pin_num = board.D0):
        self.pressed = False
        pin = digitalio.DigitalInOut(pin_num)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP  
        self.pin = pin

    def pin_active(self):
        return not self.pin.value

    def update(self):
        if self.pressed and not self.pin_active():
            self.pressed = False

    def newly_pressed(self):
        if not self.pressed and self.pin_active():
            self.pressed = True
            return True
        return False

    def deinit(self):
        self.pin.deinit()