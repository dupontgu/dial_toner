import board
import digitalio

address_pins = [board.D9, board.D8, board.D7]
input_pins = [board.D4, board.D5, board.D6]

for i, p in enumerate(input_pins):
    ip = digitalio.DigitalInOut(p)
    ip.direction = digitalio.Direction.INPUT
    # dont think we these need pullups since they are connected to output of logic chip?
    ip.pull = digitalio.Pull.UP
    input_pins[i] = ip

for i, p in enumerate(address_pins):
    op = digitalio.DigitalInOut(p)
    op.direction = digitalio.Direction.OUTPUT
    address_pins[i] = op

# sets the address of the bit we want to read from each byte
# all of the mux ic's are wired to the same adress pins so we can read a given bit
# from each of them at the "same time"
def write_three_bit_addr(addr):
    for i in range(3):
        address_pins[i].value = True if ((1 << i) & addr > 0) else False

# reads byte from each of the 3 mux ic's, one bit at a time from lsb to msb
def read_bytes():
    (r, g, b) = (0, 0, 0)
    # loop through bit positions in a byte
    for i in range(8):
        write_three_bit_addr(i)
        mask = 1 << i
        # read 1 bit from each mux output
        r |= mask if not input_pins[0].value else 0
        g |= mask if not input_pins[1].value else 0
        b |= mask if not input_pins[2].value else 0
    return (r, g, b)