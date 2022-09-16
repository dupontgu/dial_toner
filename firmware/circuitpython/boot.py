from button import Button
from persistence import get_reboot_button_count
import storage

DEBUG = True

if not DEBUG:
    storage.disable_usb_drive()

btn = Button()
if btn.newly_pressed():
    print("button pressed during boot...")
    button_count = get_reboot_button_count() + 1
    if button_count == 2:
        storage.enable_usb_drive()
    print("button count: ", button_count)

btn.deinit()
print("boot complete!")