import adafruit_imageload
from color_util import use_dark_text
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from adafruit_bitmap_font import bitmap_font
import board
import time

color_text_y_map = {
    1 : 112,
    2 : 90,
    3 : 60,
    4 : 30 
}

class DialTonerDisplay:
    def __init__(self):
        displayio.release_displays()
        font = bitmap_font.load_font("3Dventure-48.pcf", displayio.Bitmap)
        spi = board.SPI()
        while not spi.try_lock():
            pass
        spi.unlock()
        tft_cs = board.D7
        tft_dc = board.D6

        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D5, baudrate=24000000)
        self.display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=270)
        self.display.auto_refresh = False
        self.display_group = displayio.Group()
        self.display.show(self.display_group)

        color_bitmap = displayio.Bitmap(240, 240, 1)
        self.bg_palette = displayio.Palette(1)
        self.bg_palette[0] = 0x000000
        bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=self.bg_palette,
                               x=0, y=0)
        self.display_group.append(bg_sprite)
        self.color_text_label = label.Label(font, text="", color=0xffffff, scale=1)
        self.color_text_label.x = 16
        self.display_group.append(self.color_text_label)
        

        logo_bitmap, self.logo_palette = adafruit_imageload.load("/tdt_logo_240.bmp",
                                          bitmap=displayio.Bitmap,
                                          palette=displayio.Palette)
        self.logo_palette.make_transparent(0)
        self.logo = displayio.TileGrid(logo_bitmap, pixel_shader=self.logo_palette)
        self.logo_showing = False
        self.last_color_update = 0

    def update_bg_color(self, bg_color):
        now = time.monotonic()
        if now - self.last_color_update > 0.5:
            self.bg_palette[0] = bg_color
            self.last_color_update = now
            return True
        return False

    def show_logo(self):
        self.color_text_label.text = ""
        self.display.refresh()
        self.display_group.append(self.logo)
        self.logo_showing = True

    def hide_logo(self):
        self.display_group.pop()
        self.logo_showing = False

    def update_text_color(self, bg_color):
        c = (0,0,0) if use_dark_text(bg_color) else (255,255,255)
        self.logo_palette[1] = c
        self.color_text_label.color = c

    def update_with(self, mode):
        print(mode.as_rgb)
        c = mode.as_rgb
        if self.update_bg_color(c):
            self.update_text_color(c)
        display = mode.display
        self.color_text_label.y = color_text_y_map[len(display)]
        max_line = max([len(l) for l in display])
        self.color_text_label.x = 5 + ((8 - max_line) * 13)
        self.color_text_label.text = "\n".join(display)

    def refresh(self):
        self.display.refresh()