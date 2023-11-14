# Import core modules
import board
from digitalio import DigitalInOut, Direction

# Button class
class Button():

    # Initialisation
    def __init__(self, pin, invert, debug):
        print(f'Button.init({pin}, {invert}, {debug})')
        # Initialise
        self.debug = debug        
        self.pin = pin
        self.dio = DigitalInOut(pin)
        self.dio.direction = Direction.INPUT
        self.invert = invert
        self.on = False

    # Main function, call to update on value, returns:
    # 0 = off, unchanged
    # 1 = on,  unchanged
    # 2 = off, changed
    # 3 = on,  changed
    def main(self):
        result = 0b0
        on = self.dio.value
        if self.invert:
            on = not on
        if self.on != on:
            result |= 0b10
            if on:
                result |= 0b1
            self.on = on
        if self.debug and changed: print(f'Button.read({self.pin}) = {result}')
        return result

# Button class (END)




