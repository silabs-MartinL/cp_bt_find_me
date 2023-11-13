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

    # Read function
    def read(self):
        changed = False
        on = self.dio.value
        if self.invert:
            on = not on
        if self.on != on:
            changed = True
            self.on = on
        if self.debug and changed: print(f'Button.read({self.pin}) = {self.on}, {changed}')
        return self.on, changed

# Button class (END)




