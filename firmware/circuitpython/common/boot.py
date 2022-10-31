from pio_button import PioButton
from persistence import get_reboot_button_count, set_reboot_button_count
import storage
import board

DEBUG = True

if not DEBUG:
    storage.disable_usb_drive()

btn = PioButton(board.D0)
if btn.newly_pressed():
    print("button pressed during boot...")
    button_count = get_reboot_button_count() + 1
    set_reboot_button_count(button_count)
    if button_count == 2:
        storage.enable_usb_drive()
    print("button count: ", button_count)
else:
    print("button NOT pressed during boot.")
    set_reboot_button_count(0)

print("boot complete!")