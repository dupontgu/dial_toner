# CircuitPython firmware for The Dial Toner
- Tested with CircuitPython version 7.2.x and 7.3.x
- Designed to run on the Seeeduino XIAO RP2040, but _should_ run on any of the Seeeduino XIAO series of dev boards.
- You will need to include the following Adafruit CircuitPython libraries in order for this code to run:
  - `adafruit_hid`
  - `adafruit_pixelbuf.mpy`
  - `neopixel.mpy`
- Note that there is a variable called `DEBUG` in boot.py. I have it defaulting to True, but if you flip it, the XIAO will stop showing up as a storage device.
- //TODO link to usage instructions