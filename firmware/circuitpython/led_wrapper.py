import neopixel
import board

# Control multiple neopixel chains at once.
# This also allows for alternate implementations where no physical pixels are actually present.
class LedWrapper():
    def __init__(self):
        self.pixels = []
        self._brightness = 0
        # use both included NEOPIXEL on the Xiao and the one we have connected to D1
        self.pixels.append(neopixel.NeoPixel(board.D1, 1, brightness=self._brightness, auto_write=False))
        self.pixels.append(neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=self._brightness, auto_write=False))

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        for p in self.pixels:
            p.brightness = self._brightness
            p.show()
    
    def show(self):
        for p in self.pixels:
            p.show()
    
    def fill(self, color):
        for p in self.pixels:
            p.fill(color)
            p.show()